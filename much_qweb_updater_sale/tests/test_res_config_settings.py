# -*- coding: utf-8 -*-
"""
Tests for res.config.settings sales configuration interface.

This module tests the configuration settings interface for
sales-specific company settings.
"""

from odoo.tests import tagged

from .common import MuchQwebSaleTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_sale",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsSalesFields(MuchQwebSaleTestCommon):
    """
    Test cases for sales-related configuration settings.

    Tests the related fields that expose company sales settings
    through the res.config.settings interface.
    """

    def test_so_print_sale_person_related(self):
        """Test so_print_sale_person is properly related to company."""
        self.env["res.config.settings"].create(
            {
                "so_print_sale_person": True,
            }
        )
        self.company.invalidate_recordset()
        self.assertTrue(self.company.so_print_sale_person)

    def test_so_print_datev_identifier_customer_related(self):
        """Test so_print_datev_identifier_customer is related to company."""
        self.env["res.config.settings"].create(
            {
                "so_print_datev_identifier_customer": True,
            }
        )
        self.company.invalidate_recordset()
        self.assertTrue(self.company.so_print_datev_identifier_customer)

    def test_taxes_on_line_related(self):
        """Test taxes_on_line is properly related to company."""
        self.env["res.config.settings"].create(
            {
                "taxes_on_line": True,
            }
        )
        self.company.invalidate_recordset()
        self.assertTrue(self.company.taxes_on_line)

    def test_description_quotation_related(self):
        """Test description_quotation is properly related to company."""
        self.env["res.config.settings"].create(
            {
                "description_quotation": "<p>Settings Quotation</p>",
            }
        )
        self.company.invalidate_recordset()
        self.assertEqual(
            self.company.description_quotation, "<p>Settings Quotation</p>"
        )

    def test_description_order_related(self):
        """Test description_order is properly related to company."""
        self.env["res.config.settings"].create(
            {
                "description_order": "<p>Settings Order</p>",
            }
        )
        self.company.invalidate_recordset()
        self.assertEqual(self.company.description_order, "<p>Settings Order</p>")


@tagged(
    "much_unit",
    "much_qweb_updater_sale",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsReadFromCompany(MuchQwebSaleTestCommon):
    """
    Test cases for reading sales settings from company.
    """

    def test_settings_reflect_company_sales_values(self):
        """Test settings fields reflect current company configuration."""
        self.company.write(
            {
                "so_print_sale_person": True,
                "so_print_datev_identifier_customer": False,
                "taxes_on_line": True,
                "description_quotation": "<p>Company Quotation</p>",
                "description_order": "<p>Company Order</p>",
            }
        )

        settings = self.env["res.config.settings"].create({})

        self.assertTrue(settings.so_print_sale_person)
        self.assertFalse(settings.so_print_datev_identifier_customer)
        self.assertTrue(settings.taxes_on_line)
        self.assertEqual(settings.description_quotation, "<p>Company Quotation</p>")
        self.assertEqual(settings.description_order, "<p>Company Order</p>")


@tagged(
    "much_unit",
    "much_qweb_updater_sale",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsSalesFieldStorage(MuchQwebSaleTestCommon):
    """
    Test cases for verifying field storage attribute behavior.
    """

    def test_boolean_fields_are_stored(self):
        """Test that stored boolean fields persist to company."""
        self.env["res.config.settings"].create(
            {
                "so_print_sale_person": True,
                "so_print_datev_identifier_customer": True,
                "taxes_on_line": True,
            }
        )

        self.company.invalidate_recordset()

        self.assertTrue(self.company.so_print_sale_person)
        self.assertTrue(self.company.so_print_datev_identifier_customer)
        self.assertTrue(self.company.taxes_on_line)
