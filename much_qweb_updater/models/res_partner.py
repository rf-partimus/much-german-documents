# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vendor_ref = fields.Char(
        string="Our Vendor Reference", help="Our Vendor Reference at a Customer"
    )
    customer_ref = fields.Char(
        string="Our Customer Reference", help="Our Customer Reference at a Vendor"
    )

    def _get_complete_name(self):
        """Return the complete name of the partner.

        When context contains 'report_address_format=True', separates company
        and contact names with a newline instead of a comma. This enables
        proper line separation in report address blocks.
        """
        if not self.env.context.get("report_address_format"):
            return super()._get_complete_name()

        name = self.name or ""
        if self.company_name or self.parent_id:
            if not name and self.type in ["invoice", "delivery", "other", "private"]:
                name = dict(self._fields["type"]._description_selection(self.env)).get(
                    self.type, ""
                )
            if not self.is_company:
                self = self.sudo()
                name = f"{self.commercial_company_name or self.parent_id.name}\n{name}"
        return name.strip()
