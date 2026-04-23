# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    print_sale_person = fields.Boolean("Print Sales Person Info Invoice")
    block_condition = fields.Boolean(
        string="Block Terms and Condition Transfer from Order"
    )
    print_payment_ref = fields.Boolean(string="Print Payment Reference")
    print_time_frame = fields.Boolean(string="Print Delivery Time Frame")
    print_shipping_address = fields.Boolean(
        string="Print Shipping Address on Invoices/Credit Notes"
    )
    print_shipping_address_display_name = fields.Boolean(
        string="Print Shipping Address with Company name"
    )
    print_incoterm = fields.Boolean(string="Print Incoterm")
    ac_print_coo = fields.Boolean(string="Print Country of Origin Invoice")
    ac_print_hs_code = fields.Boolean(string="Print HS Code Invoice")
    description_inv = fields.Html(
        string="Default Description before Table Invoice", translate=True
    )
    description_credit_note = fields.Html(
        string="Default Description before Table Credit Note", translate=True
    )
    invoice_print_datev_identifier_customer = fields.Boolean(
        string="Print Datev Identifier Customer Invoice"
    )

    def write(self, vals):
        result = super().write(vals)
        if "description_inv" in vals or "description_credit_note" in vals:
            self._update_account_move_report_header_texts()
        return result

    def _update_account_move_report_header_texts(self):
        self._update_report_header_text_bulk(
            table_name="account_move",
            field_mapping={
                "out_invoice": "description_inv",
                "out_refund": "description_credit_note",
            },
            state_conditions={
                "out_invoice": "t.move_type = 'out_invoice' AND"
                " t.report_header_text_manual is not True",
                "out_refund": "t.move_type = 'out_refund' AND"
                " t.report_header_text_manual is not True",
            },
        )
