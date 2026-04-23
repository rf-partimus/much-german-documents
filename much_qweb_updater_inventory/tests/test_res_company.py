# -*- coding: utf-8 -*-
"""
Tests for res.company inventory-specific configuration fields.

This module tests the company fields added for delivery document
customization, including print settings and description fields.
"""

from odoo.tests import tagged

from .common import MuchQwebInventoryTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_inventory",
    "res_company",
    "post_install",
    "-at_install",
)
class TestResCompanyInventoryFields(MuchQwebInventoryTestCommon):
    """
    Test cases for inventory configuration fields on res.company.

    Tests boolean flags, description field, and persistence.
    """

    def test_inventory_fields_crud_and_persistence(self):
        """Test all inventory fields can be set, cleared, and persist."""
        boolean_fields = [
            "inventory_print_coo",
            "inventory_print_hs_code",
            "print_weight",
        ]

        self.company.write({field: True for field in boolean_fields})
        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should be True")

        self.company.write({field: False for field in boolean_fields})
        for field in boolean_fields:
            self.assertFalse(getattr(self.company, field), f"{field} should be False")

        html_content = "<p>Delivery Description</p>"
        self.company.write({"description_delivery": html_content})
        self.assertEqual(self.company.description_delivery, html_content)

        self.company.write({"description_delivery": False})
        self.assertFalse(self.company.description_delivery)

        self.company.write(
            {
                **{field: True for field in boolean_fields},
                "description_delivery": "<p>Persistent Delivery</p>",
            }
        )
        self.company.invalidate_recordset()

        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should persist")
        self.assertEqual(
            self.company.description_delivery, "<p>Persistent Delivery</p>"
        )

    def test_description_delivery_translation(self):
        """Test description_delivery field supports translation."""
        self.company.write({"description_delivery": "<p>English Delivery</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_delivery": "<p>Deutsche Lieferung</p>"}
        )

        german_desc = self.company.with_context(lang="de_DE").description_delivery

        self.assertIn("Lieferung", german_desc)
