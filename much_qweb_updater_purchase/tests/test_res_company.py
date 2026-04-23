# -*- coding: utf-8 -*-
"""
Tests for res.company purchase-specific configuration fields.

This module tests the company fields added for RFQ and purchase order
customization, including print settings and description fields.
"""

from odoo.tests import tagged

from .common import MuchQwebPurchaseTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_purchase",
    "res_company",
    "post_install",
    "-at_install",
)
class TestResCompanyPurchaseFields(MuchQwebPurchaseTestCommon):
    """
    Test cases for purchase configuration fields on res.company.

    Tests boolean flags, description fields, and persistence.
    """

    def test_purchase_fields_crud_and_persistence(self):
        """Test all purchase fields can be set, cleared, and persist."""
        boolean_fields = [
            "print_buyer_info",
            "purchase_print_datev_identifier",
        ]

        self.company.write({field: True for field in boolean_fields})
        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should be True")

        self.company.write({field: False for field in boolean_fields})
        for field in boolean_fields:
            self.assertFalse(getattr(self.company, field), f"{field} should be False")

        self.company.write(
            {
                "description_rfq": "<p>RFQ Description</p>",
                "description_purchase": "<p>PO Description</p>",
            }
        )
        self.assertEqual(self.company.description_rfq, "<p>RFQ Description</p>")
        self.assertEqual(self.company.description_purchase, "<p>PO Description</p>")

        self.company.write(
            {
                "description_rfq": False,
                "description_purchase": False,
            }
        )
        self.assertFalse(self.company.description_rfq)
        self.assertFalse(self.company.description_purchase)

        self.company.write(
            {
                **{field: True for field in boolean_fields},
                "description_rfq": "<p>RFQ</p>",
                "description_purchase": "<p>PO</p>",
            }
        )
        self.company.invalidate_recordset()

        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should persist")
        self.assertEqual(self.company.description_rfq, "<p>RFQ</p>")
        self.assertEqual(self.company.description_purchase, "<p>PO</p>")

    def test_description_fields_translation(self):
        """Test description fields support translation."""
        self.company.write({"description_rfq": "<p>English RFQ</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_rfq": "<p>Deutsche Anfrage</p>"}
        )
        self.assertIn(
            "Anfrage", self.company.with_context(lang="de_DE").description_rfq
        )

        self.company.write({"description_purchase": "<p>English PO</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_purchase": "<p>Deutsche Bestellung</p>"}
        )
        self.assertIn(
            "Bestellung", self.company.with_context(lang="de_DE").description_purchase
        )
