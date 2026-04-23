# -*- coding: utf-8 -*-
"""
Tests for purchase.requisition blanket order customization.

This module tests report header text computation, template data generation,
and dynamic field validation for purchase requisitions.
"""

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import MuchQwebPurchaseRequisitionTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_purchase_requisitions",
    "purchase_requisition",
    "post_install",
    "-at_install",
)
class TestPurchaseRequisitionReportHeaderText(MuchQwebPurchaseRequisitionTestCommon):
    """
    Test cases for report_header_text computed field and constraints.
    """

    def test_header_text_computation_and_language_handling(self):
        """Test header text defaults, language handling, and fallbacks."""
        requisition = self.create_purchase_requisition()
        self.assertEqual(
            requisition.report_header_text, "<p>Default Requisition Description</p>"
        )

        self.company.write({"description_requisition": False})
        requisition2 = self.create_purchase_requisition()
        requisition2._compute_report_header_text()
        self.assertFalse(requisition2.report_header_text)

        self.company.write(
            {"description_requisition": "<p>Default Requisition Description</p>"}
        )
        self.company.with_context(lang="de_DE").write(
            {"description_requisition": "<p>Deutsche Rahmenvereinbarung</p>"}
        )
        german_vendor = self.env["res.partner"].create(
            {
                "name": "German Vendor",
                "lang": "de_DE",
                "supplier_rank": 1,
            }
        )
        requisition3 = self.create_purchase_requisition(vendor=german_vendor)
        self.assertIsNotNone(requisition3.report_header_text)

        no_lang_vendor = self.env["res.partner"].create(
            {
                "name": "No Language Vendor",
                "lang": False,
                "supplier_rank": 1,
            }
        )
        requisition4 = self.create_purchase_requisition(vendor=no_lang_vendor)
        self.assertIsNotNone(requisition4.report_header_text)

    def test_header_text_constraint_and_order_title(self):
        """Test dynamic field validation and order_title field."""
        requisition = self.create_purchase_requisition()
        requisition.report_header_text = "<p>Vendor: ${object.name}</p>"

        with self.assertRaises(ValidationError):
            requisition.report_header_text = "<p>${object.nonexistent_field}</p>"

        requisition2 = self.create_purchase_requisition(
            order_title="Custom Requisition Title"
        )
        self.assertEqual(requisition2.order_title, "Custom Requisition Title")

        requisition2.write({"order_title": "Updated Title"})
        self.assertEqual(requisition2.order_title, "Updated Title")
