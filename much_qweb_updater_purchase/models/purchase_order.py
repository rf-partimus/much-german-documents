# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

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
    order_title = fields.Char(string="Title of the order")

    @api.constrains("report_header_text", "notes")
    def _check_report_header_text(self):
        """
        Method to check the dynamic field exists or not.
        """
        for record in self:
            if record.report_header_text:
                self.env.user.get_evaluated_val(
                    record, record.report_header_text, check=True
                )
            if record.note:
                self.env.user.get_evaluated_val(record, record.note, check=True)

    @api.depends(
        "state",
        "company_id",
        "partner_id.lang",
    )
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
                translation_cache[(company.id, lang, "description_rfq")] = (
                    company.with_context(lang=lang).description_rfq
                )
                translation_cache[(company.id, lang, "description_purchase")] = (
                    company.with_context(lang=lang).description_purchase
                )

        value_to_records = {}

        for rec in to_compute:
            lang = rec.partner_id.lang or self.env.user.lang

            if rec.state in ["draft", "sent"]:
                value = translation_cache.get(
                    (rec.company_id.id, lang, "description_rfq"), False
                )
            elif rec.state == "purchase":
                value = translation_cache.get(
                    (rec.company_id.id, lang, "description_purchase"), False
                )
            else:
                value = False

            key = value or False
            value_to_records.setdefault(key, self.env["purchase.order"])
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

    def button_confirm(self):
        """
        Override to reset manual flag on confirmation so state-based compute
        applies the correct company default for the confirmed state.
        """
        # Reset manual flag so compute method includes this record
        self.write({"report_header_text_manual": False})
        return super(PurchaseOrder, self).button_confirm()
