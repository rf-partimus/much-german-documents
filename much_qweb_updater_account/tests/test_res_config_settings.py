# -*- coding: utf-8 -*-
"""
Tests for res.config.settings accounting configuration interface.

This module tests the configuration settings interface for
accounting-specific company settings.
"""

from odoo.tests import tagged

from .common import MuchQwebAccountTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsAccountingFields(MuchQwebAccountTestCommon):
    """
    Test cases for accounting-related configuration settings.

    Tests the related fields that expose company accounting settings
    through the res.config.settings interface.
    """

    def test_settings_fields_related_to_company(self):
        """Test all settings fields are properly related to company and persist."""
        boolean_fields = [
            "print_sale_person",
            "block_condition",
            "print_payment_ref",
            "print_time_frame",
            "print_incoterm",
            "ac_print_coo",
            "ac_print_hs_code",
            "invoice_print_datev_identifier_customer",
        ]

        self.env["res.config.settings"].create(
            {
                **{field: True for field in boolean_fields},
                "description_inv": "<p>Settings Invoice Description</p>",
                "description_credit_note": "<p>Settings Credit Note</p>",
            }
        )
        self.company.invalidate_recordset()

        for field in boolean_fields:
            self.assertTrue(
                getattr(self.company, field), f"{field} should be True on company"
            )
        self.assertEqual(
            self.company.description_inv, "<p>Settings Invoice Description</p>"
        )
        self.assertEqual(
            self.company.description_credit_note, "<p>Settings Credit Note</p>"
        )

    def test_settings_reflect_company_values(self):
        """Test settings fields reflect current company configuration."""
        self.company.write(
            {
                "print_sale_person": True,
                "block_condition": True,
                "print_payment_ref": False,
                "print_time_frame": True,
                "print_incoterm": True,
                "ac_print_coo": False,
                "ac_print_hs_code": True,
                "description_inv": "<p>Company Invoice</p>",
                "description_credit_note": "<p>Company Credit Note</p>",
                "invoice_print_datev_identifier_customer": True,
            }
        )

        settings = self.env["res.config.settings"].create({})

        self.assertTrue(settings.print_sale_person)
        self.assertTrue(settings.block_condition)
        self.assertFalse(settings.print_payment_ref)
        self.assertTrue(settings.print_time_frame)
        self.assertTrue(settings.print_incoterm)
        self.assertFalse(settings.ac_print_coo)
        self.assertTrue(settings.ac_print_hs_code)
        self.assertEqual(settings.description_inv, "<p>Company Invoice</p>")
        self.assertEqual(settings.description_credit_note, "<p>Company Credit Note</p>")
        self.assertTrue(settings.invoice_print_datev_identifier_customer)
