# -*- coding: utf-8 -*-
"""
Tests for res.config.settings purchase requisition configuration interface.

This module tests the configuration settings interface for
purchase requisition-specific company settings.
"""

from odoo.tests import tagged

from .common import MuchQwebPurchaseRequisitionTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_purchase_requisitions",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsRequisitionFields(MuchQwebPurchaseRequisitionTestCommon):
    """
    Test cases for requisition-related configuration settings.

    Tests the related fields that expose company requisition settings
    through the res.config.settings interface.
    """

    def test_requisition_print_buyer_info_related(self):
        """Test requisition_print_buyer_info is properly related to company."""
        self.env["res.config.settings"].create(
            {
                "requisition_print_buyer_info": True,
            }
        )
        self.company.invalidate_recordset()
        self.assertTrue(self.company.requisition_print_buyer_info)

    def test_print_existing_rfqs_related(self):
        """Test print_existing_rfqs is properly related to company."""
        self.env["res.config.settings"].create(
            {
                "print_existing_rfqs": True,
            }
        )
        self.company.invalidate_recordset()
        self.assertTrue(self.company.print_existing_rfqs)

    def test_description_requisition_related(self):
        """Test description_requisition is properly related to company."""
        self.env["res.config.settings"].create(
            {
                "description_requisition": "<p>Settings Requisition</p>",
            }
        )
        self.company.invalidate_recordset()
        self.assertEqual(
            self.company.description_requisition, "<p>Settings Requisition</p>"
        )


@tagged(
    "much_unit",
    "much_qweb_updater_purchase_requisitions",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsReadFromCompany(MuchQwebPurchaseRequisitionTestCommon):
    """
    Test cases for reading requisition settings from company.
    """

    def test_settings_reflect_company_requisition_values(self):
        """Test settings fields reflect current company configuration."""
        self.company.write(
            {
                "requisition_print_buyer_info": True,
                "print_existing_rfqs": False,
                "description_requisition": "<p>Company Requisition</p>",
            }
        )

        settings = self.env["res.config.settings"].create({})

        self.assertTrue(settings.requisition_print_buyer_info)
        self.assertFalse(settings.print_existing_rfqs)
        self.assertEqual(settings.description_requisition, "<p>Company Requisition</p>")


@tagged(
    "much_unit",
    "much_qweb_updater_purchase_requisitions",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsRequisitionFieldStorage(
    MuchQwebPurchaseRequisitionTestCommon
):
    """
    Test cases for verifying field storage attribute behavior.
    """

    def test_boolean_fields_are_stored(self):
        """Test that stored boolean fields persist to company."""
        self.env["res.config.settings"].create(
            {
                "requisition_print_buyer_info": True,
                "print_existing_rfqs": True,
            }
        )

        self.company.invalidate_recordset()

        self.assertTrue(self.company.requisition_print_buyer_info)
        self.assertTrue(self.company.print_existing_rfqs)
