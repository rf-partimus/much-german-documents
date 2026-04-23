# -*- coding: utf-8 -*-
"""
Tests for purchase.order RFQ and purchase order customization.

This module tests report header text computation, template data generation,
dynamic field validation, and state-dependent behavior.
"""

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import MuchQwebPurchaseTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_purchase",
    "purchase_order",
    "post_install",
    "-at_install",
)
class TestPurchaseOrderReportHeaderText(MuchQwebPurchaseTestCommon):
    """
    Test cases for report_header_text computed field and constraints.
    """

    def test_header_text_state_dependent_defaults(self):
        """Test header text uses correct company description based on state."""
        draft_order = self.create_purchase_order(state="draft")
        self.assertEqual(
            draft_order.report_header_text, "<p>Default RFQ Description</p>"
        )

        sent_order = self.create_purchase_order(state="sent")
        self.assertEqual(
            sent_order.report_header_text, "<p>Default RFQ Description</p>"
        )

        confirmed_order = self.create_purchase_order_with_lines(state="purchase")
        confirmed_order._compute_report_header_text()
        self.assertEqual(
            confirmed_order.report_header_text,
            "<p>Default Purchase Order Description</p>",
        )

        self.company.write(
            {
                "description_rfq": False,
                "description_purchase": False,
            }
        )
        empty_order = self.create_purchase_order()
        empty_order._compute_report_header_text()
        self.assertFalse(empty_order.report_header_text)

        self.company.write({"description_rfq": "<p>Default RFQ Description</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_rfq": "<p>Deutsche Anfrage</p>"}
        )
        german_vendor = self.env["res.partner"].create(
            {
                "name": "German Vendor",
                "lang": "de_DE",
                "supplier_rank": 1,
            }
        )
        german_order = self.create_purchase_order(partner=german_vendor)
        self.assertIsNotNone(german_order.report_header_text)

    def test_header_text_constraints(self):
        """Test dynamic field validation for header and notes fields."""
        order = self.create_purchase_order()
        order.report_header_text = "<p>Vendor: ${object.name}</p>"

        with self.assertRaises(ValidationError):
            order.report_header_text = "<p>${object.nonexistent_field}</p>"

    def test_order_title_field(self):
        """Test order_title field can be set and updated."""
        order = self.create_purchase_order(order_title="Custom PO Title")
        self.assertEqual(order.order_title, "Custom PO Title")

        order.write({"order_title": "Updated Title"})
        self.assertEqual(order.order_title, "Updated Title")
