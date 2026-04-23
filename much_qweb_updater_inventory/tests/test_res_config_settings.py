# -*- coding: utf-8 -*-
"""
Tests for res.config.settings inventory configuration interface.

This module tests the configuration settings interface for
inventory-specific company settings.
"""

from odoo.tests import tagged

from .common import MuchQwebInventoryTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_inventory",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsInventoryFields(MuchQwebInventoryTestCommon):
    """
    Test cases for inventory-related configuration settings.

    Tests the related fields that expose company inventory settings
    through the res.config.settings interface.
    """

    def test_settings_fields_related_to_company(self):
        """Test all settings fields are properly related to company and persist."""
        boolean_fields = [
            "inventory_print_coo",
            "inventory_print_hs_code",
            "print_weight",
        ]

        self.env["res.config.settings"].create(
            {
                **{field: True for field in boolean_fields},
                "description_delivery": "<p>Settings Delivery</p>",
            }
        )
        self.company.invalidate_recordset()

        for field in boolean_fields:
            self.assertTrue(
                getattr(self.company, field), f"{field} should be True on company"
            )
        self.assertEqual(self.company.description_delivery, "<p>Settings Delivery</p>")

    def test_settings_reflect_company_values(self):
        """Test settings fields reflect current company configuration."""
        self.company.write(
            {
                "inventory_print_coo": True,
                "inventory_print_hs_code": False,
                "print_weight": True,
                "description_delivery": "<p>Company Delivery</p>",
            }
        )

        settings = self.env["res.config.settings"].create({})

        self.assertTrue(settings.inventory_print_coo)
        self.assertFalse(settings.inventory_print_hs_code)
        self.assertTrue(settings.print_weight)
        self.assertEqual(settings.description_delivery, "<p>Company Delivery</p>")
