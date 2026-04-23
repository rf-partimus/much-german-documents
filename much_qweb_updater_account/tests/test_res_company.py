# -*- coding: utf-8 -*-
"""
Tests for res.company accounting-specific configuration fields.

This module tests the company fields added for invoice and credit note
customization, including print settings and description fields.
"""

from odoo.tests import tagged

from .common import MuchQwebAccountTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "res_company",
    "post_install",
    "-at_install",
)
class TestResCompanyAccountingFields(MuchQwebAccountTestCommon):
    """Test cases for res.company accounting configuration fields."""

    def test_boolean_and_description_fields_crud(self):
        """Test all boolean and description fields can be set, cleared, and persist."""
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

        self.company.write({field: True for field in boolean_fields})
        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should be True")

        self.company.write({field: False for field in boolean_fields})
        for field in boolean_fields:
            self.assertFalse(getattr(self.company, field), f"{field} should be False")

        self.company.write(
            {
                "description_inv": "<p>Invoice Description</p>",
                "description_credit_note": "<p>Credit Note Description</p>",
            }
        )
        self.assertEqual(self.company.description_inv, "<p>Invoice Description</p>")
        self.assertEqual(
            self.company.description_credit_note, "<p>Credit Note Description</p>"
        )

        self.company.write(
            {
                "description_inv": False,
                "description_credit_note": False,
            }
        )
        self.assertFalse(self.company.description_inv)
        self.assertFalse(self.company.description_credit_note)

        self.company.write(
            {
                **{field: True for field in boolean_fields},
                "description_inv": "<p>Persistent Invoice</p>",
                "description_credit_note": "<p>Persistent Credit Note</p>",
            }
        )
        self.company.invalidate_recordset()

        for field in boolean_fields:
            self.assertTrue(getattr(self.company, field), f"{field} should persist")
        self.assertEqual(self.company.description_inv, "<p>Persistent Invoice</p>")
        self.assertEqual(
            self.company.description_credit_note, "<p>Persistent Credit Note</p>"
        )

    def test_description_fields_translation(self):
        """Test description fields support translation."""
        self.company.write({"description_inv": "<p>English Invoice</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_inv": "<p>Deutsche Rechnung</p>"}
        )

        self.company.write({"description_credit_note": "<p>English Credit Note</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_credit_note": "<p>Deutsche Gutschrift</p>"}
        )

        self.assertIn(
            "Rechnung", self.company.with_context(lang="de_DE").description_inv
        )
        self.assertIn(
            "Gutschrift",
            self.company.with_context(lang="de_DE").description_credit_note,
        )
