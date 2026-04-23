# -*- coding: utf-8 -*-
"""
Tests for res.config.settings purchase configuration interface.

This module tests the configuration settings interface for
purchase-specific company settings.
"""

from odoo.tests import tagged

from .common import MuchQwebPurchaseTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_purchase",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsPurchaseFields(MuchQwebPurchaseTestCommon):
    """
    Test cases for purchase-related configuration settings.

    Tests the related fields that expose company purchase settings
    through the res.config.settings interface.
    """

    def test_settings_fields_related_to_company(self):
        """Test all settings fields are properly related to company and persist."""
        boolean_fields = [
            "print_buyer_info",
            "purchase_print_datev_identifier",
        ]

        self.env["res.config.settings"].create(
            {
                **{field: True for field in boolean_fields},
                "description_rfq": "<p>Settings RFQ</p>",
                "description_purchase": "<p>Settings PO</p>",
            }
        )
        self.company.invalidate_recordset()

        for field in boolean_fields:
            self.assertTrue(
                getattr(self.company, field), f"{field} should be True on company"
            )
        self.assertEqual(self.company.description_rfq, "<p>Settings RFQ</p>")
        self.assertEqual(self.company.description_purchase, "<p>Settings PO</p>")

    def test_settings_reflect_company_values(self):
        """Test settings fields reflect current company configuration."""
        self.company.write(
            {
                "print_buyer_info": True,
                "purchase_print_datev_identifier": False,
                "description_rfq": "<p>Company RFQ</p>",
                "description_purchase": "<p>Company PO</p>",
            }
        )

        settings = self.env["res.config.settings"].create({})

        self.assertTrue(settings.print_buyer_info)
        self.assertFalse(settings.purchase_print_datev_identifier)
        self.assertEqual(settings.description_rfq, "<p>Company RFQ</p>")
        self.assertEqual(settings.description_purchase, "<p>Company PO</p>")
