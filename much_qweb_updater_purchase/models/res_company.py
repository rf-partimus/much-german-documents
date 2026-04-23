# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    print_buyer_info = fields.Boolean()
    purchase_print_datev_identifier = fields.Boolean(
        string="Print Datev Identifier Supplier"
    )
    description_rfq = fields.Html(
        string="Default Description before Table RFQ", translate=True
    )
    description_purchase = fields.Html(
        string="Default Description before Table Purchase Order", translate=True
    )

    def write(self, vals):
        result = super().write(vals)
        if "description_rfq" in vals or "description_purchase" in vals:
            self._update_purchase_order_report_header_texts()
        return result

    def _update_purchase_order_report_header_texts(self):
        self._update_report_header_text_bulk(
            table_name="purchase_order",
            field_mapping={
                "rfq": "description_rfq",
                "purchase": "description_purchase",
            },
            state_conditions={
                "rfq": (
                    "t.state IN ('draft', 'sent') "
                    "AND t.report_header_text_manual is not True"
                ),
                "purchase": (
                    "t.state = 'purchase' "
                    "AND t.report_header_text_manual is not True"
                ),
            },
        )
