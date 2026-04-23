from odoo import models
from lxml import html
import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_html(self, report_ref, docids, data=None):
        """
        This method is used to remove the VAT div from the invoice report (New revision)
        """
        result = super()._render_qweb_html(report_ref, docids, data)
        html_content = result[0]

        if (
            report_ref == "account.report_invoice"
            and b"information_block" in html_content
        ):
            try:
                tree = html.fromstring(html_content)

                for div in tree.xpath(
                    '//div[@class="row din_company_info"]'
                    '//div[@class="information_block"]//table//div[.//td[text()="VAT"]]'
                ):
                    parent = div.getparent()
                    parent.remove(div)
                    _logger.info("Removed VAT div from invoice report")

                html_content = html.tostring(tree, encoding="unicode").encode("utf-8")
                result = (html_content,) + result[1:]

            except Exception as e:
                _logger.error("Failed to remove VAT div: %s", str(e), exc_info=True)
                raise

        return result
