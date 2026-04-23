# -*- coding: utf-8 -*-
"""
Tests for res.partner reference fields.

This module tests the vendor_ref and customer_ref fields added
to partners for cross-company reference tracking, as well as
the _get_complete_name override for report formatting.
"""

from odoo.tests import tagged

from .common import MuchQwebTestCommon


@tagged("much_unit", "much_qweb_updater", "res_partner", "post_install", "-at_install")
class TestResPartnerReferenceFields(MuchQwebTestCommon):
    """
    Test cases for vendor_ref and customer_ref fields on res.partner.
    """

    def test_ref_fields_crud_and_search(self):
        """Test create, read, update, clear, and search for both reference fields."""
        partner = self.create_partner_with_refs(
            name="Ref Test Partner",
            vendor_ref="VND/2026-001&TEST",
            customer_ref="CUST/2026-001&TEST",
        )
        self.assertEqual(partner.vendor_ref, "VND/2026-001&TEST")
        self.assertEqual(partner.customer_ref, "CUST/2026-001&TEST")

        partner.write({"vendor_ref": "VND-UPDATED"})
        self.assertEqual(partner.vendor_ref, "VND-UPDATED")
        self.assertEqual(partner.customer_ref, "CUST/2026-001&TEST")

        partner.write({"vendor_ref": False, "customer_ref": False})
        self.assertFalse(partner.vendor_ref)
        self.assertFalse(partner.customer_ref)

        self.partner_contact.write({"vendor_ref": "CONTACT-VND"})
        self.assertEqual(self.partner_contact.vendor_ref, "CONTACT-VND")
        self.assertEqual(self.partner_customer.vendor_ref, "VENDOR-001")

        self.assertIn(
            self.partner_customer,
            self.env["res.partner"].search([("vendor_ref", "=", "VENDOR-001")]),
        )
        self.assertIn(
            self.partner_vendor,
            self.env["res.partner"].search([("customer_ref", "=", "CUSTOMER-002")]),
        )
        self.assertTrue(
            self.env["res.partner"].search([("vendor_ref", "ilike", "VENDOR")])
        )
        self.assertTrue(
            self.env["res.partner"].search([("customer_ref", "ilike", "CUSTOMER")])
        )

        partner_empty = self.create_partner_with_refs(
            name="Empty Refs Partner", vendor_ref=False, customer_ref=False
        )
        self.assertIn(
            partner_empty,
            self.env["res.partner"].search(
                [("vendor_ref", "=", False), ("id", "=", partner_empty.id)]
            ),
        )

    def test_ref_fields_edge_cases(self):
        """Test ref fields with special chars, long values, copy, and isolation."""
        special_partner = self.create_partner_with_refs(
            name="Special Chars Partner",
            vendor_ref="VND/2026/001-äöü",
            customer_ref="CUST#2026@TEST",
        )
        self.assertEqual(special_partner.vendor_ref, "VND/2026/001-äöü")
        self.assertEqual(special_partner.customer_ref, "CUST#2026@TEST")

        long_ref = "A" * 255
        long_partner = self.create_partner_with_refs(
            name="Long Ref Partner",
            vendor_ref=long_ref,
            customer_ref=long_ref,
        )
        self.assertEqual(long_partner.vendor_ref, long_ref)
        self.assertEqual(long_partner.customer_ref, long_ref)

        empty_partner = self.create_partner_with_refs(
            name="Empty String Partner",
            vendor_ref="",
            customer_ref="",
        )
        self.assertFalse(empty_partner.vendor_ref)
        self.assertFalse(empty_partner.customer_ref)

        partner1 = self.create_partner_with_refs(
            name="Partner 1", vendor_ref="REF-001", customer_ref="CUST-001"
        )
        partner2 = self.create_partner_with_refs(
            name="Partner 2", vendor_ref="REF-002", customer_ref="CUST-002"
        )
        partner1.write({"vendor_ref": "REF-001-UPDATED"})
        self.assertEqual(partner1.vendor_ref, "REF-001-UPDATED")
        self.assertEqual(partner2.vendor_ref, "REF-002")

        original = self.create_partner_with_refs(
            name="Original Partner", vendor_ref="ORIG-VND", customer_ref="ORIG-CUST"
        )
        copied = original.copy()
        self.assertEqual(copied.vendor_ref, "ORIG-VND")
        self.assertEqual(copied.customer_ref, "ORIG-CUST")
        self.assertNotEqual(copied.id, original.id)


@tagged("much_unit", "much_qweb_updater", "res_partner", "post_install", "-at_install")
class TestResPartnerCompleteName(MuchQwebTestCommon):
    """
    Test cases for _get_complete_name method override.

    Tests the report_address_format context behavior for proper
    address formatting in reports.
    """

    def test_complete_name_without_and_with_report_context(self):
        """Test _get_complete_name with and without report_address_format context."""
        result_no_ctx = self.partner_contact._get_complete_name()
        self.assertIn(self.partner_contact.name, result_no_ctx)
        self.assertNotIn("\n", result_no_ctx)

        result_contact = self.partner_contact.with_context(
            report_address_format=True
        )._get_complete_name()
        self.assertIn(self.partner_customer.name, result_contact)
        self.assertIn(self.partner_contact.name, result_contact)
        self.assertIn("\n", result_contact)

        result_company = self.partner_customer.with_context(
            report_address_format=True
        )._get_complete_name()
        self.assertEqual(result_company, self.partner_customer.name)

    def test_complete_name_contact_variations(self):
        """Test _get_complete_name for various contact configurations."""
        standalone_contact = self.env["res.partner"].create(
            {
                "name": "Standalone Contact",
                "company_type": "person",
                "is_company": False,
            }
        )
        result = standalone_contact.with_context(
            report_address_format=True
        )._get_complete_name()
        self.assertEqual(result, "Standalone Contact")

        partner_with_company = self.env["res.partner"].create(
            {
                "name": "John Doe",
                "company_name": "ACME Corporation",
                "company_type": "person",
                "is_company": False,
            }
        )
        result = partner_with_company.with_context(
            report_address_format=True
        )._get_complete_name()
        self.assertIn("ACME Corporation", result)
        self.assertIn("John Doe", result)
        self.assertIn("\n", result)

    def test_complete_name_edge_cases(self):
        """Test _get_complete_name with empty names, address types, and whitespace."""
        partner_no_name = self.env["res.partner"].create(
            {
                "name": "",
                "email": "noname@test.com",
            }
        )
        result = partner_no_name.with_context(
            report_address_format=True
        )._get_complete_name()
        self.assertEqual(result, "")

        for addr_type in ["invoice", "delivery"]:
            address = self.env["res.partner"].create(
                {
                    "name": "",
                    "type": addr_type,
                    "parent_id": self.partner_customer.id,
                }
            )
            result = address.with_context(
                report_address_format=True
            )._get_complete_name()
            self.assertIn(self.partner_customer.name, result)

        partner_whitespace = self.env["res.partner"].create(
            {
                "name": "  Whitespace Partner  ",
                "company_type": "company",
            }
        )
        result = partner_whitespace.with_context(
            report_address_format=True
        )._get_complete_name()
        self.assertFalse(result.startswith(" "))
        self.assertFalse(result.endswith(" "))
