from odoo import api, models
from markupsafe import Markup, escape


class ContactWidget(models.AbstractModel):
    """Contact widget override for proper name separation in addresses.

    Renders addresses with company name and contact name on separate lines.
    For German (DE) addresses, the country name is hidden.
    """

    _inherit = "ir.qweb.field.contact"

    def _render_address(self, value, options, hide_country=False):
        """Render address with company and contact names on separate lines.

        Uses report_address_format context to get company and contact names
        on separate lines via _get_complete_name().
        """
        if not value:
            if options.get("null_text"):
                val = {
                    "options": options,
                }
                template_options = options.get("template_options", {})
                return self.env["ir.qweb"]._render(
                    "base.no_contact", val, **template_options
                )
            return ""
        opf = options.get("fields") or ["name", "address", "phone", "mobile", "email"]

        value = value.sudo()

        if value._name == "res.users":
            value = value.partner_id

        if not value:
            return False

        name_part = value.with_context(report_address_format=True)._get_complete_name()
        name_lines = [line for line in name_part.split("\n") if line.strip()]
        name_html = Markup("<br/>").join(escape(line) for line in name_lines)

        sep = options.get("separator")
        if sep:
            opsep = escape(sep)
        elif options.get("no_tag_br"):
            opsep = escape(", ")
        else:
            opsep = Markup("<br/>")

        address_lines = [
            line.strip()
            for line in value._display_address(without_company=True).split("\n")
            if line.strip()
        ]
        address = opsep.join(address_lines) if address_lines else ""

        val = {
            "name": name_html,
            "address": address,
            "phone": value.phone,
            "city": value.city,
            "country_id": "" if hide_country else value.country_id.display_name,
            "website": value.website,
            "email": value.email,
            "vat": value.vat,
            "vat_label": value.country_id.vat_label or "VAT",
            "fields": opf,
            "object": value,
            "options": options,
        }

        return self.env["ir.qweb"]._render("base.contact", val, minimal_qcontext=True)

    @api.model
    def record_to_html(self, record, field_name, options):
        """Render contact with proper name separation for all addresses."""
        value = record[field_name]

        if not value:
            return super().record_to_html(record, field_name, options)

        hide_country = value.sudo().country_id.code == "DE"
        return self._render_address(value, options, hide_country=hide_country)

    @api.model
    def value_to_html(self, value, options):
        """Render contact with proper name separation for all addresses."""
        if not value:
            return super().value_to_html(value, options)

        hide_country = value.sudo().country_id.code == "DE"
        return self._render_address(value, options, hide_country=hide_country)
