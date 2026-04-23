# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    report_header_text = fields.Html(string="Description before Table")
    order_title = fields.Char(string="Title of the order")
