# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    so_print_sale_person = fields.Boolean(
        string="Print Sales Person Info",
        related="company_id.so_print_sale_person",
        readonly=False,
        store=True,
    )
    so_print_datev_identifier_customer = fields.Boolean(
        string="Print Datev Identifier Customer",
        related="company_id.so_print_datev_identifier_customer",
        readonly=False,
        store=True,
    )
    taxes_on_line = fields.Boolean(
        string="Taxes on Line Level",
        related="company_id.taxes_on_line",
        readonly=False,
        store=True,
    )
    description_quotation = fields.Html(
        string="Default Description before Table Quotation",
        related="company_id.description_quotation",
        readonly=False,
    )
    description_order = fields.Html(
        string="Default Description before Table Order",
        related="company_id.description_order",
        readonly=False,
    )
    so_print_invoice_shipping_address = fields.Boolean(
        string="Print Invoice & Shipping Address",
        related="company_id.so_print_invoice_shipping_address",
        readonly=False,
        store=True,
    )
