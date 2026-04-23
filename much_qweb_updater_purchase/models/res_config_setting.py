# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    print_buyer_info = fields.Boolean(
        string="Print Buyer Info",
        related="company_id.print_buyer_info",
        readonly=False,
        store=True,
    )
    purchase_print_datev_identifier = fields.Boolean(
        string="Print Datev Identifier Supplier",
        related="company_id.purchase_print_datev_identifier",
        readonly=False,
        store=True,
    )
    description_rfq = fields.Html(
        string="Default Description before Table RFQ",
        related="company_id.description_rfq",
        readonly=False,
    )
    description_purchase = fields.Html(
        string="Default Description before Table Purchase Order",
        related="company_id.description_purchase",
        readonly=False,
    )
