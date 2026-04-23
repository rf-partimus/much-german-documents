# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    requisition_print_buyer_info = fields.Boolean(string="Print Buyer Info Agreement")
    print_existing_rfqs = fields.Boolean(string="Print existing RFQs")
    description_requisition = fields.Html(
        string="Default Description Blanket Order", translate=True
    )

    def write(self, vals):
        result = super().write(vals)
        if "description_requisition" in vals:
            self._update_purchase_requisition_report_header_texts()
        return result

    def _update_purchase_requisition_report_header_texts(self):
        """
        Update report header texts for purchase requisitions when company
        descriptions change.
        """
        self._update_report_header_text_bulk(
            table_name="purchase_requisition",
            partner_field="vendor_id",
            field_mapping={None: "description_requisition"},
            state_conditions={
                None: "t.report_header_text_manual is not True",
            },
        )
