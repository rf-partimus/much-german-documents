# -*- coding: utf-8 -*-

from odoo import models, fields

LOGO_UNITS = [("px", "px"), ("in", "in"), ("%", "%")]


class Settings(models.Model):
    _inherit = "res.company"

    free_text_footer = fields.Boolean(default=False)
    column_1 = fields.Html()
    column_2 = fields.Html()
    column_3 = fields.Html()
    column_4 = fields.Html()
    footer_font_size = fields.Integer(default=10)
    logo_width_unit = fields.Selection(LOGO_UNITS, default="px")
    logo_width = fields.Integer(string="Width")
    logo_height_unit = fields.Selection(LOGO_UNITS, default="px")
    logo_height = fields.Integer(string="Height")
    print_company = fields.Boolean(default=True, string="Print Company Country")
    adjust_logo = fields.Boolean(default=False)
    report_primary_color = fields.Char(
        string="Report Primary Color", related="primary_color"
    )
    report_secondary_color = fields.Char(
        string="Report Secondary Color", related="secondary_color"
    )

    def _update_report_header_text_bulk(
        self,
        table_name,
        partner_field="partner_id",
        field_mapping=None,
        state_conditions=None,
    ):
        """
        Generic helper to update report_header_text fields via SQL when company
        descriptions change.

        :param table_name: Database table name (e.g., 'account_move', 'sale_order')
        :param partner_field: Name of the partner field for language lookup
            (default: 'partner_id')
        :param field_mapping: Dict mapping state/condition to company field name
                             e.g., {'out_invoice': 'description_inv',
                                    'out_refund': 'description_credit_note'}
                             or {None: 'description_delivery'} for simple mapping
        :param state_conditions: Dict mapping state/condition to SQL WHERE clause
                                e.g., {'out_invoice': "move_type = 'out_invoice'"}
        """
        for company in self:
            cr = self.env.cr

            langs_query = f"""
                SELECT DISTINCT COALESCE(rp.lang, %s) as lang
                FROM {table_name} t
                LEFT JOIN res_partner rp ON t.{partner_field} = rp.id
                WHERE t.company_id = %s
            """  # nosec
            cr.execute(langs_query, (self.env.user.lang, company.id))
            unique_langs = [row[0] for row in cr.fetchall()]

            translation_cache = {}
            for lang in unique_langs:
                for field_name in set(field_mapping.values()):
                    translation_cache[(field_name, lang)] = company.with_context(
                        lang=lang
                    )[field_name]

            for condition_key, company_field in field_mapping.items():
                for lang in unique_langs:
                    value = translation_cache[(company_field, lang)] or ""

                    where_clause = (
                        state_conditions.get(condition_key, "")
                        if state_conditions
                        else ""
                    )

                    query = f"""
                        UPDATE {table_name} t
                        SET report_header_text = %s
                        FROM res_partner rp
                        WHERE t.company_id = %s
                        AND t.{partner_field} = rp.id
                        AND COALESCE(rp.lang, %s) = %s
                        {f"AND {where_clause}" if where_clause else ""}
                    """  # nosec
                    cr.execute(query, (value, company.id, self.env.user.lang, lang))
