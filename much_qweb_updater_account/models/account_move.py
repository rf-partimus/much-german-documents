# -*- coding: utf-8 -*-
from calendar import monthrange
from datetime import datetime
from odoo import models, fields, _, api


class AccountMove(models.Model):
    _inherit = "account.move"

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
    delivery_start_date = fields.Date(
        "Delivery Start date", default=lambda self: self.invoice_date or datetime.now()
    )
    delivery_end_date = fields.Date(
        "Delivery End date", default=lambda self: self.invoice_date or datetime.now()
    )
    print_time_frame = fields.Boolean(
        string="Print Delivery Time Frame",
        related="company_id.print_time_frame",
    )
    delivery_date_error_message = fields.Char(
        string="Delivery Date Message Error",
        compute="_compute_validate_invoice_dates",
    )

    def write(self, vals):
        """Overwrites write, to propagate delivery dates."""
        for res in self:
            res._copy_delivery_date_fields_into_lines(vals)

        result = super().write(vals)

        for res in self:
            res._propagate_delivery_date_changes(vals)

        return result

    @api.model_create_multi
    def create(self, vals_list):
        """Overwrites create, to propagate delivery dates."""
        for res in self:
            res._copy_move_delivery_date_to_lines(vals_list)
        account_move_ids = super().create(vals_list)
        for move, values in zip(account_move_ids, vals_list):
            move._propagate_delivery_date_changes(values)
        return account_move_ids

    @staticmethod
    def _copy_move_delivery_date_to_lines(vals_list: list):
        """Copies delivery date from invoice_line id into delivery lines,
        before create() gets called."""
        for vals in vals_list if isinstance(vals_list, list) else [vals_list]:
            # Set on create, if not set.
            if "delivery_start_date" in vals_list:
                for line in vals.get("line_ids") or []:
                    if not line[2].get("delivery_start_date"):
                        line[2]["delivery_start_date"] = vals["delivery_start_date"]
            if "delivery_end_date" in vals_list:
                for line in vals.get("line_ids") or []:
                    if not line[2].get("delivery_end_date"):
                        line[2]["delivery_end_date"] = vals["delivery_end_date"]

    @api.depends(
        "invoice_line_ids.delivery_start_date", "invoice_line_ids.delivery_end_date"
    )
    def _compute_validate_invoice_dates(self):
        """Checks whether the dates in the invoice line ids are a month apart
         and start is before end.

        Sets delivery_date_error_message to:
        - False, if everything is fine
        - The warning message, if there are problems.
        """
        for line_id in self.invoice_line_ids:
            if line_id.delivery_start_date and line_id.delivery_end_date:
                if line_id.delivery_start_date > line_id.delivery_end_date:
                    self.delivery_date_error_message = _(
                        "Invoice delivery start date is after end date."
                    )
                    return
                elif not self.validate_dates_are_months_apart(line_id):
                    self.delivery_date_error_message = _(
                        "Invoice line delivery dates are not exact months apart."
                    )
                    return
        self.delivery_date_error_message = False

    @staticmethod
    def validate_dates_are_months_apart(obj):
        """Checks for the passed object,
           that there are exact months between start and end.

        E.g.
        25.8 -> 24.9 = OK
        25.8 -> 23.10 = NOT OK
        1.2 -> 31.12 = OK

        If start day is 31th of January, this is always False.
         (Cause there's no 30th of February).
        What would 31th of January + 1 Month even be?
        """
        if not obj.delivery_end_date or not obj.delivery_start_date:
            return True

        # Both dates are the same day, difference = 0
        if obj.delivery_start_date == obj.delivery_end_date:
            return True

        start_day = obj.delivery_start_date.day
        previous_day = start_day - 1
        end_day = obj.delivery_end_date.day
        if (
            end_day
            == monthrange(obj.delivery_end_date.year, obj.delivery_end_date.month)[1]
        ):
            end_day = 0

        if previous_day != end_day:
            return False
        return True

    @staticmethod
    def _copy_delivery_date_fields_into_lines(vals):
        """Copies changes to invoice_line_ids into line_ids.

        :param vals: The array of values passed to the write() function.
        """
        if vals.get("invoice_line_ids"):

            def copy_field_over(field, invoice_line):
                # first value in the list indicated the operation
                # 2 is delete, 0 is create, 1 is write
                if (
                    invoice_line[0] != 2
                    and invoice_line[2]
                    and field in invoice_line[2]
                    and vals.get("line_ids")
                ):
                    line = [
                        line_id
                        for line_id in vals["line_ids"] or []
                        if line_id[1] == invoice_line[1]
                    ]
                    if len(line) >= 1:
                        line = line[0]
                        line[2][field] = invoice_line[2][field]

            for invoice_line in vals["invoice_line_ids"]:
                copy_field_over("delivery_start_date", invoice_line)
                copy_field_over("delivery_end_date", invoice_line)

    def _propagate_delivery_date_changes(self, vals):
        """Propagates changes in the invoice delivery date to its
         lines and the other way around.

        This part sets the following logic:
        * If any delivery date in the move is set, all lines get the same date.
        * If a delivery date in a line is set, such as that it is outside the
         delivery time frame of the move
          the delivery frame of the move gets changed to fit the line.
        * Check context to avoid case where line changes propagate to move
         changes, which then overwrite lines again.

        :param vals: Vals passed to create() or write()
        """
        if not self.env.context.get("disable_set_line_date"):
            if vals.get("delivery_start_date"):
                for line_id in self.invoice_line_ids:
                    line_id.delivery_start_date = self.delivery_start_date

            if vals.get("delivery_end_date") and not self.env.context.get(
                "disable_set_line_date"
            ):
                for line_id in self.invoice_line_ids:
                    line_id.delivery_end_date = self.delivery_end_date

        if vals.get("line_ids"):
            start_dates = [
                line_id.delivery_start_date
                for line_id in self.invoice_line_ids
                if line_id.delivery_start_date
            ]
            end_dates = [
                line_id.delivery_end_date
                for line_id in self.invoice_line_ids
                if line_id.delivery_end_date
            ]

            min_start_date = min(start_dates) if start_dates else None
            max_end_date = max(end_dates) if end_dates else None
            if min_start_date and min_start_date != self.delivery_start_date:
                self.with_context(disable_set_line_date=True).delivery_start_date = (
                    min_start_date
                )
            if max_end_date and max_end_date != self.delivery_end_date:
                self.with_context(disable_set_line_date=True).delivery_end_date = (
                    max_end_date
                )

        for line_id in self.line_ids:
            if not line_id.delivery_start_date and self.delivery_start_date:
                line_id.delivery_start_date = self.delivery_start_date
            if not line_id.delivery_end_date and self.delivery_end_date:
                line_id.delivery_end_date = self.delivery_end_date

    @api.constrains("report_header_text", "narration")
    def _check_report_header_text(self):
        """
        Method to check the dynamic field exists or not.
        """
        for record in self:
            if record.report_header_text:
                self.env.user.get_evaluated_val(
                    record, record.report_header_text, check=True
                )
            if record.narration:
                self.env.user.get_evaluated_val(record, record.narration, check=True)

    @api.depends(
        "company_id",
        "move_type",
        "partner_id.lang",
    )
    def _compute_report_header_text(self):
        """
        Computes default report header text based on company settings and partner
        language. Only sets default values when field has not been manually
        modified. Preserves manually entered text when partner or other
        dependencies change.
        """
        self = self.with_context(disable_set_report_header_text_manual=True)
        to_compute = self.filtered(lambda r: not r.report_header_text_manual)
        if not to_compute:
            return

        unique_companies = to_compute.mapped("company_id")
        unique_langs = set(
            (to_compute.mapped("partner_id.lang") or []) + [self.env.user.lang]
        )

        translation_cache = {}
        for company in unique_companies:
            for lang in unique_langs:
                if not lang:
                    continue
                key_inv = (company.id, lang, "description_inv")
                key_credit = (company.id, lang, "description_credit_note")
                translation_cache[key_inv] = company.with_context(
                    lang=lang
                ).description_inv
                translation_cache[key_credit] = company.with_context(
                    lang=lang
                ).description_credit_note

        value_to_records = {}

        for rec in to_compute:
            lang = rec.partner_id.lang or self.env.user.lang

            if rec.move_type == "out_invoice":
                value = translation_cache.get(
                    (rec.company_id.id, lang, "description_inv"), False
                )
            elif rec.move_type == "out_refund":
                value = translation_cache.get(
                    (rec.company_id.id, lang, "description_credit_note"), False
                )
            else:
                value = False

            key = value or False
            value_to_records.setdefault(key, self.env["account.move"])
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
