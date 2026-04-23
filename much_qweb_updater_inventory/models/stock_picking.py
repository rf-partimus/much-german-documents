# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    order_title = fields.Char(string="Delivery Title")
    report_header_text = fields.Html(
        string="Description before Table",
        compute="_compute_report_header_text",
        inverse="_inverse_report_header_text",
        store=True,
        readonly=False,
    )
    report_header_text_manual = fields.Boolean(
        string="Manual Report Header Text",
        default=False,
        help="Indicates if the report header text was manually set by user",
    )
    l10n_din5008_template_data = fields.Binary(
        compute="_compute_l10n_din5008_template_data"
    )
    document_address_id = fields.Many2one(
        "res.partner",
        string="Document Address",
        compute="_compute_document_address_id",
        help="The document address from the related sales order.",
    )

    @api.depends("sale_id", "sale_id.partner_invoice_id")
    def _compute_document_address_id(self):
        for picking in self:
            if picking.sale_id and picking.sale_id.partner_invoice_id:
                picking.document_address_id = picking.sale_id.partner_invoice_id
            else:
                picking.document_address_id = False

    @api.constrains("report_header_text")
    def _check_report_header_text(self):
        """
        Method to check the dynamic field exists or not.
        """
        for record in self:
            self.env.user.get_evaluated_val(
                record, record.report_header_text, check=True
            )

    @api.depends("company_id", "partner_id.lang")
    def _compute_report_header_text(self):
        """
        Computes default report header text based on company settings and partner
        language. Only sets default values when field has not been manually
        modified. Preserves manually entered text when partner or other
        dependencies change.
        """
        if not self:
            return

        # Protection pattern starts here
        self = self.with_context(disable_set_report_header_text_manual=True)
        to_compute = self.filtered(lambda r: not r.report_header_text_manual)
        if not to_compute:
            return
        # Protection pattern ends here

        unique_companies = to_compute.mapped("company_id")
        unique_langs = set(
            (to_compute.mapped("partner_id.lang") or []) + [self.env.user.lang]
        )

        translation_cache = {}
        for company in unique_companies:
            for lang in unique_langs:
                if not lang:
                    continue
                translation_cache[(company.id, lang)] = company.with_context(
                    lang=lang
                ).description_delivery

        value_to_records = {}

        for rec in to_compute:
            lang = rec.partner_id.lang or self.env.user.lang
            value = translation_cache.get((rec.company_id.id, lang), False)

            key = value or False
            value_to_records.setdefault(key, self.env["stock.picking"])
            value_to_records[key] |= rec

        for value, records in value_to_records.items():
            records.update({"report_header_text": value})

    def _inverse_report_header_text(self):
        """
        Inverse method that sets the manual flag when the report header text is
        modified by user. This prevents the compute method from overwriting
        manually entered text.
        """
        if self.env.context.get("disable_set_report_header_text_manual"):
            return
        for rec in self:
            rec.report_header_text_manual = bool(rec.report_header_text)

    def format_date_by_lang(self, date):
        """
        Formats a given date according to the language of the picking partner.

        This method retrieves the language code from the partner's record and uses it
        to fetch the corresponding date and time format from the `res.lang` model. If a
        matching language is found, the date is formatted according to the retrieved
        formats. If no matching language is found or if the date is not provided, the
        original date is returned.
        """
        if not date:
            return date
        lang_code = self.partner_id.lang
        user_lang = self.env["res.lang"].search([("code", "=", lang_code)], limit=1)
        if user_lang:
            date_format = user_lang.date_format
            time_format = user_lang.time_format
            formatted_date = date.strftime(f"{date_format} {time_format}")
            return formatted_date
        return date

    def _compute_l10n_din5008_template_data(self):
        for record in self:
            record.l10n_din5008_template_data = record.get_l10n_din5008_template_data()

    def get_l10n_din5008_template_data(self):
        self.ensure_one()
        data = []
        if self.origin:
            data.append((_("Order:"), self.origin, "origin"))
        if self.state:
            shipping_date = (
                self.date_done if self.state == "done" else self.scheduled_date
            )
            formatted_date = self.format_date_by_lang(shipping_date)
            data.append((_("Shipping Date:"), formatted_date, "shipping_date"))
        if self.sale_id.client_order_ref:
            data.append(
                (
                    _("Customer Reference:"),
                    self.sale_id.client_order_ref,
                    "customer_reference",
                )
            )
        if self.sale_id.incoterm:
            if self.sale_id.incoterm_location:
                data.append(
                    (
                        _("Incoterm:"),
                        "%s %s"
                        % (
                            self.sale_id.incoterm.code,
                            self.sale_id.incoterm_location,
                        ),
                        "incoterm",
                    )
                )
            else:
                data.append(
                    (_("Incoterm:"), self.sale_id.incoterm.display_name, "incoterm")
                )

        return data
