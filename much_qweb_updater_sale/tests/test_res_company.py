# -*- coding: utf-8 -*-
"""
Tests for res.company sales-specific configuration fields.

This module tests the company fields added for quotation and order
customization, including print settings and description fields.
"""

from odoo.tests import tagged

from .common import MuchQwebSaleTestCommon


@tagged(
    "much_unit", "much_qweb_updater_sale", "res_company", "post_install", "-at_install"
)
class TestResCompanySalesFields(MuchQwebSaleTestCommon):
    """
    Test cases for sales configuration fields on res.company.

    Tests boolean flags, description fields, and persistence.
    """

    def test_sales_fields_crud_and_persistence(self):
        """Test all sales fields can be set, cleared, and persist."""
        boolean_fields = [
            "so_print_sale_person",
            "so_print_datev_identifier_customer",
            "taxes_on_line",
        ]

        self.company.write({field: True for field in boolean_fields})
        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should be True")

        self.company.write({field: False for field in boolean_fields})
        for field in boolean_fields:
            self.assertFalse(getattr(self.company, field), f"{field} should be False")

        self.company.write(
            {
                "description_quotation": "<p>Quotation Description</p>",
                "description_order": "<p>Order Description</p>",
            }
        )
        self.assertEqual(
            self.company.description_quotation, "<p>Quotation Description</p>"
        )
        self.assertEqual(self.company.description_order, "<p>Order Description</p>")

        self.company.write(
            {
                "description_quotation": False,
                "description_order": False,
            }
        )
        self.assertFalse(self.company.description_quotation)
        self.assertFalse(self.company.description_order)

        self.company.write(
            {
                **{field: True for field in boolean_fields},
                "description_quotation": "<p>Quotation</p>",
                "description_order": "<p>Order</p>",
            }
        )
        self.company.invalidate_recordset()

        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should persist")
        self.assertEqual(self.company.description_quotation, "<p>Quotation</p>")
        self.assertEqual(self.company.description_order, "<p>Order</p>")

    def test_description_fields_translation(self):
        """Test description fields support translation."""
        self.company.write({"description_quotation": "<p>English Quotation</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_quotation": "<p>Deutsches Angebot</p>"}
        )
        self.assertIn(
            "Angebot", self.company.with_context(lang="de_DE").description_quotation
        )

        self.company.write({"description_order": "<p>English Order</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_order": "<p>Deutsche Bestellung</p>"}
        )
        self.assertIn(
            "Bestellung", self.company.with_context(lang="de_DE").description_order
        )
