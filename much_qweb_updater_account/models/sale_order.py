# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"
    delivery_start_date = fields.Date("Delivery Start date")
    delivery_end_date = fields.Date("Delivery End date")

    def _prepare_invoice(self):
        invoice_data = super()._prepare_invoice()
        lang = self.partner_id.lang or self.env.user.lang
        invoice_data["delivery_start_date"] = self.delivery_start_date
        invoice_data["delivery_end_date"] = self.delivery_end_date
        use_invoice_terms = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("account.use_invoice_terms")
        )
        if self.company_id.block_condition and use_invoice_terms:
            invoice_data["narration"] = (
                self.company_id.with_context(lang=lang).invoice_terms or ""
            )
        return invoice_data
