# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    free_text_footer = fields.Boolean(
        related="company_id.free_text_footer", readonly=False, store=True
    )
    column_1 = fields.Html(related="company_id.column_1", readonly=False, store=True)
    column_2 = fields.Html(related="company_id.column_2", readonly=False, store=True)
    column_3 = fields.Html(related="company_id.column_3", readonly=False, store=True)
    column_4 = fields.Html(related="company_id.column_4", readonly=False, store=True)
    footer_font_size = fields.Integer(
        related="company_id.footer_font_size", readonly=False, store=True
    )
    print_company = fields.Boolean(
        related="company_id.print_company",
        string="Print Company Country",
        readonly=False,
        store=True,
    )
    adjust_logo = fields.Boolean(
        related="company_id.adjust_logo", readonly=False, store=True
    )
    logo_width_unit = fields.Selection(
        related="company_id.logo_width_unit", readonly=False, store=True
    )
    logo_width = fields.Integer(
        string="Width", related="company_id.logo_width", readonly=False, store=True
    )
    logo_height_unit = fields.Selection(
        related="company_id.logo_height_unit", readonly=False, store=True
    )
    logo_height = fields.Integer(
        string="Height", related="company_id.logo_height", readonly=False, store=True
    )

    def edit_paper_format(self):
        paperformat_id = self.env.company.paperformat_id
        return {
            "type": "ir.actions.act_window",
            "res_model": "report.paperformat",
            "view_mode": "form",
            "res_id": paperformat_id.id,
        }
