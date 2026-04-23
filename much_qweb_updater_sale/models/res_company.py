# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    so_print_sale_person = fields.Boolean(string="Print Sales Person Info")
    so_print_datev_identifier_customer = fields.Boolean(
        string="Print Datev Identifier Customer"
    )
    taxes_on_line = fields.Boolean(string="Taxes on Line Level")
    description_quotation = fields.Html(
        string="Default Description before Table Quotation", translate=True
    )
    description_order = fields.Html(
        string="Default Description before Table Order", translate=True
    )
    so_print_invoice_shipping_address = fields.Boolean(
        string="Print Invoice & Shipping Address"
    )

    def write(self, vals):
        result = super().write(vals)
        if "description_quotation" in vals or "description_order" in vals:
            self._update_sale_order_report_header_texts()
        return result

    def _update_sale_order_report_header_texts(self):
        self._update_report_header_text_bulk(
            table_name="sale_order",
            field_mapping={
                "quotation": "description_quotation",
                "order": "description_order",
            },
            state_conditions={
                "quotation": (
                    "t.state IN ('draft', 'sent') "
                    "AND t.report_header_text_manual is not True"
                ),
                "order": (
                    "t.state = 'sale' " "AND t.report_header_text_manual is not True"
                ),
            },
        )
