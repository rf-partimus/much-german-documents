# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    inventory_print_coo = fields.Boolean(string="Print Country of Origin")
    inventory_print_hs_code = fields.Boolean(string="Print HS Code")
    print_weight = fields.Boolean()
    description_delivery = fields.Html(
        string="Default Description before Table Delivery", translate=True
    )
    show_document_address = fields.Boolean(
        string="Show Document Address on Delivery Slip",
        default=False,
        help="If enabled, an additional Document Address block will be displayed on"
        "the delivery slip when connected to a sales order.",
    )

    def write(self, vals):
        result = super().write(vals)
        if "description_delivery" in vals:
            self._update_stock_picking_report_header_texts()
        return result

    def _update_stock_picking_report_header_texts(self):
        """
        Update report header texts for stock pickings when company
        descriptions change.
        """
        self._update_report_header_text_bulk(
            table_name="stock_picking",
            field_mapping={None: "description_delivery"},
            state_conditions={
                None: "t.report_header_text_manual is not True",
            },
        )
