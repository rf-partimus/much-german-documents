# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    print_sale_person = fields.Boolean(
        string="Print Sales Person Info Invoice",
        related="company_id.print_sale_person",
        readonly=False,
        store=True,
    )
    block_condition = fields.Boolean(
        string="Block Terms and Condition Transfer from Order",
        related="company_id.block_condition",
        readonly=False,
        store=True,
    )
    print_payment_ref = fields.Boolean(
        string="Print Payment Reference",
        related="company_id.print_payment_ref",
        readonly=False,
        store=True,
    )
    print_time_frame = fields.Boolean(
        string="Print Delivery Time Frame",
        related="company_id.print_time_frame",
        readonly=False,
        store=True,
    )
    print_shipping_address = fields.Boolean(
        string="Print Shipping Address on Invoices/Credit Notes",
        related="company_id.print_shipping_address",
        readonly=False,
        store=True,
    )
    print_shipping_address_display_name = fields.Boolean(
        string="Print Shipping Address with Company name",
        related="company_id.print_shipping_address_display_name",
        readonly=False,
        store=True,
    )
    print_incoterm = fields.Boolean(
        string="Print Incoterm",
        related="company_id.print_incoterm",
        readonly=False,
        store=True,
    )
    ac_print_coo = fields.Boolean(
        string="Print Country of Origin Invoice",
        related="company_id.ac_print_coo",
        readonly=False,
        store=True,
    )
    ac_print_hs_code = fields.Boolean(
        string="Print HS Code Invoice",
        related="company_id.ac_print_hs_code",
        readonly=False,
        store=True,
    )
    description_inv = fields.Html(
        string="Default Description before Table Invoice",
        related="company_id.description_inv",
        readonly=False,
    )
    description_credit_note = fields.Html(
        string="Default Description before Table Credit Note",
        related="company_id.description_credit_note",
        readonly=False,
    )
    invoice_print_datev_identifier_customer = fields.Boolean(
        string="Print Datev Identifier Customer Invoice",
        related="company_id.invoice_print_datev_identifier_customer",
        readonly=False,
        store=True,
    )
