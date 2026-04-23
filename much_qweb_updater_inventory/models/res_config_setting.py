# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    inventory_print_coo = fields.Boolean(
        string="Print Country of Origin",
        related="company_id.inventory_print_coo",
        readonly=False,
        store=True,
    )
    inventory_print_hs_code = fields.Boolean(
        string="Print HS Code",
        related="company_id.inventory_print_hs_code",
        readonly=False,
        store=True,
    )
    print_weight = fields.Boolean(
        string="Print Weight",
        related="company_id.print_weight",
        readonly=False,
        store=True,
    )
    description_delivery = fields.Html(
        string="Default Description before Table Delivery",
        related="company_id.description_delivery",
        readonly=False,
    )
    show_document_address = fields.Boolean(
        string="Show Document Address on Delivery Slip",
        related="company_id.show_document_address",
        readonly=False,
        store=True,
        help="If enabled, an additional Document Address block will be "
        "displayed on the delivery slip when connected to a sales order.",
    )
