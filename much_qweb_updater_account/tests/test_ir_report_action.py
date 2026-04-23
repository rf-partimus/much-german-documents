# -*- coding: utf-8 -*-
"""
Tests for ir.actions.report VAT removal functionality.
"""

from unittest.mock import patch
from odoo.tests import tagged
from .common import MuchQwebAccountTestCommon


def _patch_parent_render(report, return_value):
    """Patch the actual parent method resolved by super() in Odoo."""
    parent = report.__class__.__mro__[1]
    return patch.object(parent, "_render_qweb_html", return_value=return_value)


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "ir_actions_report",
    "post_install",
    "-at_install",
)
class TestIrActionsReportVatRemoval(MuchQwebAccountTestCommon):
    """Test cases for ir.actions.report VAT removal functionality."""

    def test_non_invoice_report_unchanged(self):
        """Non-invoice reports remain unchanged and tuple size preserved."""
        report = self.env["ir.actions.report"].create(
            {
                "name": "Test Report",
                "model": "res.partner",
                "report_type": "qweb-html",
                "report_name": "test.report_partner",
            }
        )

        test_html = b"<html><body><div>VAT: 123456</div></body></html>"

        with _patch_parent_render(report, (test_html, "html")):
            result = report._render_qweb_html("test.report_partner", [1], data=None)

        self.assertEqual(result[0], test_html)
        self.assertEqual(len(result), 2)

        extra_data = {"key": "value"}
        with _patch_parent_render(report, (test_html, "html", extra_data)):
            result = report._render_qweb_html("some.other_report", [1], data=None)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[2], extra_data)

    def test_invoice_without_vat_in_information_block(self):
        """Invoice HTML without information_block or without VAT is unchanged."""
        report = self.env.ref("account.account_invoices")

        html_without_block = b"""
        <html>
            <body>
                <div class="invoice_content">
                    <p>Invoice</p>
                </div>
            </body>
        </html>
        """

        with _patch_parent_render(report, (html_without_block, "html")):
            result = report._render_qweb_html("account.report_invoice", [1], data=None)

        self.assertIn(b"Invoice", result[0])
        self.assertNotIn(b"information_block", result[0])

        html_no_vat = b"""
        <html>
            <body>
                <div class="row din_company_info">
                    <div class="information_block">
                        <table>
                            <tr>
                                <td>Name</td>
                                <td>Test</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </body>
        </html>
        """

        with _patch_parent_render(report, (html_no_vat, "html")):
            result = report._render_qweb_html("account.report_invoice", [1], data=None)

        self.assertIn(b"information_block", result[0])
        self.assertIn(b"Test", result[0])

    def test_invoice_vat_removal_preserves_tuple_structure(self):
        """VAT removal preserves the result tuple structure."""
        report = self.env.ref("account.account_invoices")

        html_with_vat = b"""<html><body>
            <div class="row din_company_info">
                <div class="information_block">
                    <table>
                        <div>
                            <td>VAT</td>
                            <td>DE123456789</td>
                        </div>
                    </table>
                </div>
            </div>
        </body></html>"""

        extra_data = {"key": "value"}
        with _patch_parent_render(report, (html_with_vat, "html", extra_data)):
            result = report._render_qweb_html("account.report_invoice", [1], data=None)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1], "html")
        self.assertEqual(result[2], extra_data)
