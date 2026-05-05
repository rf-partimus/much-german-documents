import re

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """
        Extend the method to compute the report header text for the active model
        and strip Odoo promotional portal_connect links from PDF output.
        """
        data = data or {}
        model = data.get("context", {}).get("active_model", False) or False
        if model and res_ids:
            records = self.env[model].browse(res_ids)
            compute_method = getattr(records, "_compute_report_header_text", None)
            if callable(compute_method):
                compute_method()
        result = super()._render_qweb_pdf(report_ref, res_ids, data)
        if result and result[0]:
            content = result[0]
            if isinstance(content, bytes):
                html_str = content.decode('utf-8')
            else:
                html_str = content
            html_str = re.sub(
                r'<div[^>]*class="text-center"[^>]*>\s*<a[^>]*portal_connect_software_modal_btn[^>]*>.*?</a>[^<]*</div>',
                '',
                html_str,
                flags=re.DOTALL,
            )
            content = html_str.encode('utf-8') if isinstance(result[0], bytes) else html_str
            result = (content, *result[1:])
        return result
