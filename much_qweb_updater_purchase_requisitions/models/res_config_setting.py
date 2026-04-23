# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    requisition_print_buyer_info = fields.Boolean(
        string="Print Buyer Info Agreement",
        related="company_id.requisition_print_buyer_info",
        readonly=False,
        store=True,
    )
    print_existing_rfqs = fields.Boolean(
        string="Print existing RFQs",
        related="company_id.print_existing_rfqs",
        readonly=False,
        store=True,
    )
    description_requisition = fields.Html(
        string="Default Description Blanket Order",
        related="company_id.description_requisition",
        readonly=False,
    )
