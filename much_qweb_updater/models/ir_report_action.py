from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """
        Extend the method to compute the report header text for the active model.
        """
        data = data or {}
        model = data.get("context", {}).get("active_model", False) or False
        if model and res_ids:
            records = self.env[model].browse(res_ids)
            compute_method = getattr(records, "_compute_report_header_text", None)
            if callable(compute_method):
                compute_method()
        result = super()._render_qweb_pdf(report_ref, res_ids, data)
        return result
