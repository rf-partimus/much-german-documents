# -*- coding: utf-8 -*-
"""
Tests for ir.qweb.field.contact widget override.

This module tests the contact widget that renders addresses with
company and contact names on separate lines, with special handling
for German (DE) addresses.
"""

from markupsafe import Markup
from odoo.tests import tagged

from .common import MuchQwebTestCommon


@tagged(
    "much_unit", "much_qweb_updater", "contact_widget", "post_install", "-at_install"
)
class TestContactWidgetRenderAddress(MuchQwebTestCommon):
    """
    Test cases for _render_address method on ir.qweb.field.contact.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for contact widget tests."""
        super().setUpClass()
        cls.contact_widget = cls.env["ir.qweb.field.contact"]
        cls.country_de = cls.env.ref("base.de")
        cls.country_us = cls.env.ref("base.us")

        cls.partner_de = cls.env["res.partner"].create(
            {
                "name": "Test Company GmbH",
                "company_type": "company",
                "street": "Hauptstraße 123",
                "city": "Berlin",
                "zip": "10115",
                "country_id": cls.country_de.id,
                "phone": "+49 30 1234567",
                "email": "info@testcompany.de",
                "website": "https://www.testcompany.de",
                "vat": "DE123456788",
            }
        )

        cls.partner_us = cls.env["res.partner"].create(
            {
                "name": "US Corporation Inc",
                "company_type": "company",
                "street": "123 Main Street",
                "city": "New York",
                "zip": "10001",
                "country_id": cls.country_us.id,
                "phone": "+1 212 5551234",
                "email": "info@uscorp.com",
            }
        )

        cls.contact_with_parent = cls.env["res.partner"].create(
            {
                "name": "John Doe",
                "company_type": "person",
                "parent_id": cls.partner_de.id,
                "email": "john.doe@testcompany.de",
            }
        )

    def test_render_address_basic_fields_and_options(self):
        """Test basic address rendering with various field combinations."""
        result = self.contact_widget._render_address(
            self.partner_de, {}, hide_country=False
        )
        self.assertIsInstance(result, (str, Markup))
        self.assertIn("Test Company GmbH", result)

        options = {"fields": ["name", "address", "phone", "mobile", "email"]}
        result = self.contact_widget._render_address(
            self.partner_de, options, hide_country=False
        )
        self.assertIn("Test Company GmbH", result)
        self.assertIn("+49 30 1234567", result)
        self.assertIn("info@testcompany.de", result)

        result = self.contact_widget._render_address(
            self.partner_de, {"fields": ["name", "email"]}, hide_country=False
        )
        self.assertIn("Test Company GmbH", result)
        self.assertIn("info@testcompany.de", result)

        result_vat = self.contact_widget._render_address(
            self.partner_de, {"fields": ["name", "vat"]}, hide_country=False
        )
        self.assertIn("DE123456788", result_vat)

    def test_render_address_hide_country_and_separators(self):
        """Test hide_country flag and various separator options."""
        options = {"fields": ["name", "address", "country_id"]}

        result_hidden = self.contact_widget._render_address(
            self.partner_de, options, hide_country=True
        )
        self.assertIn("Test Company GmbH", result_hidden)
        self.assertIsInstance(result_hidden, (str, Markup))

        result_shown = self.contact_widget._render_address(
            self.partner_us, options, hide_country=False
        )
        self.assertIn("US Corporation Inc", result_shown)
        self.assertIn("United States", result_shown)

        result_custom = self.contact_widget._render_address(
            self.partner_de,
            {"fields": ["name", "address"], "separator": " | "},
            hide_country=False,
        )
        self.assertIsInstance(result_custom, (str, Markup))

        result_comma = self.contact_widget._render_address(
            self.partner_de,
            {"fields": ["name", "address"], "no_tag_br": True},
            hide_country=False,
        )
        self.assertIsInstance(result_comma, (str, Markup))

    def test_render_address_contact_with_parent(self):
        """Test rendering for contact with parent company."""
        options = {"fields": ["name", "address"]}
        result = self.contact_widget._render_address(
            self.contact_with_parent, options, hide_country=False
        )
        self.assertIn("John Doe", result)
        self.assertIn("Test Company GmbH", result)


@tagged(
    "much_unit", "much_qweb_updater", "contact_widget", "post_install", "-at_install"
)
class TestContactWidgetRecordAndValueToHtml(MuchQwebTestCommon):
    """
    Test cases for record_to_html and value_to_html methods.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()
        cls.contact_widget = cls.env["ir.qweb.field.contact"]
        cls.country_de = cls.env.ref("base.de")
        cls.country_us = cls.env.ref("base.us")
        cls.country_fr = cls.env.ref("base.fr")

        cls.partner_de = cls.env["res.partner"].create(
            {
                "name": "German Partner",
                "street": "Berliner Str. 1",
                "city": "Munich",
                "country_id": cls.country_de.id,
                "phone": "+49 711 123456",
            }
        )

        cls.partner_us = cls.env["res.partner"].create(
            {
                "name": "American Partner",
                "street": "Broadway 42",
                "city": "New York",
                "country_id": cls.country_us.id,
            }
        )

        cls.partner_fr = cls.env["res.partner"].create(
            {
                "name": "French Partner",
                "street": "Rue de Rivoli 15",
                "city": "Paris",
                "country_id": cls.country_fr.id,
                "phone": "+33 1 23456789",
            }
        )

    def test_record_to_html_german_and_non_german(self):
        """Test record_to_html sets hide_country for DE, shows country for others."""
        options = {"fields": ["name", "address", "country_id"]}

        child_de = self.env["res.partner"].create(
            {"name": "DE Child", "parent_id": self.partner_de.id}
        )
        result_de = self.contact_widget.record_to_html(child_de, "parent_id", options)
        self.assertIsInstance(result_de, (str, Markup))
        self.assertIn("German Partner", str(result_de))

        child_us = self.env["res.partner"].create(
            {"name": "US Child", "parent_id": self.partner_us.id}
        )
        result_us = self.contact_widget.record_to_html(child_us, "parent_id", options)
        self.assertIn("United States", str(result_us))

        partner_no_parent = self.env["res.partner"].create(
            {"name": "No Parent Partner"}
        )
        result = self.contact_widget.record_to_html(partner_no_parent, "parent_id", {})
        self.assertFalse(result)

    def test_value_to_html_german_and_non_german(self):
        """Test value_to_html sets hide_country for DE, shows country for others."""
        options = {"fields": ["name", "address", "country_id"]}

        result_de = self.contact_widget.value_to_html(self.partner_de, options)
        self.assertIn("German Partner", str(result_de))
        self.assertIsInstance(result_de, (str, Markup))

        result_fr = self.contact_widget.value_to_html(self.partner_fr, options)
        self.assertIn("French Partner", str(result_fr))
        self.assertIn("France", str(result_fr))

        self.assertFalse(self.contact_widget.value_to_html(False, {}))
        self.assertFalse(self.contact_widget.value_to_html(self.env["res.partner"], {}))

    def test_value_to_html_all_fields_and_separator(self):
        """Test value_to_html with all fields and custom separator."""
        result = self.contact_widget.value_to_html(
            self.partner_de,
            {"fields": ["name", "address", "phone", "mobile", "email", "vat"]},
        )
        self.assertIn("German Partner", str(result))
        self.assertIn("+49 711 123456", str(result))

        result_sep = self.contact_widget.value_to_html(
            self.partner_fr, {"fields": ["name", "address"], "separator": " - "}
        )
        self.assertIsInstance(result_sep, (str, Markup))


@tagged(
    "much_unit", "much_qweb_updater", "contact_widget", "post_install", "-at_install"
)
class TestContactWidgetEdgeCases(MuchQwebTestCommon):
    """
    Test cases for edge cases, special scenarios, and name separation.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()
        cls.contact_widget = cls.env["ir.qweb.field.contact"]
        cls.country_de = cls.env.ref("base.de")

    def test_minimal_partner_and_no_country(self):
        """Test rendering with minimal info and partner without country."""
        minimal = self.env["res.partner"].create({"name": "Minimal Partner"})
        result = self.contact_widget._render_address(
            minimal, {"fields": ["name", "address"]}, hide_country=False
        )
        self.assertIn("Minimal Partner", str(result))

        partner = self.env["res.partner"].create(
            {"name": "No Country Partner", "street": "Unknown Location"}
        )
        result = self.contact_widget._render_address(
            partner, {"fields": ["name", "address", "country_id"]}, hide_country=False
        )
        self.assertIn("No Country Partner", str(result))

    def test_special_characters_and_unicode(self):
        """Test rendering with special characters and unicode content."""
        special = self.env["res.partner"].create(
            {
                "name": 'Test & Co. <GmbH> "Special"',
                "street": "Straße mit Ümläuten",
                "country_id": self.country_de.id,
            }
        )
        result = self.contact_widget._render_address(
            special, {"fields": ["name", "address"]}, hide_country=False
        )
        self.assertIn("Test", str(result))
        self.assertIn("Straße mit Ümläuten", str(result))

    def test_multiline_street_and_parent_inheritance(self):
        """Test multiline street and contact inheriting parent address."""
        multiline = self.env["res.partner"].create(
            {
                "name": "Multiline Corp",
                "street": "Building A",
                "street2": "Floor 5, Suite 501",
                "city": "Berlin",
                "country_id": self.country_de.id,
            }
        )
        result = self.contact_widget._render_address(
            multiline, {"fields": ["name", "address"]}, hide_country=False
        )
        self.assertIn("Multiline Corp", str(result))
        self.assertIn("Building A", str(result))

        parent = self.env["res.partner"].create(
            {
                "name": "Parent Company",
                "company_type": "company",
                "street": "Company Street 1",
                "city": "Company City",
                "country_id": self.country_de.id,
            }
        )
        contact = self.env["res.partner"].create(
            {
                "name": "Contact Person",
                "company_type": "person",
                "parent_id": parent.id,
            }
        )
        result = self.contact_widget._render_address(
            contact, {"fields": ["name", "address"]}, hide_country=False
        )
        self.assertIn("Contact Person", str(result))
        self.assertIn("Parent Company", str(result))

    def test_name_separation_and_whitespace(self):
        """Test company/contact name separation and whitespace handling."""
        company = self.env["res.partner"].create(
            {
                "name": "Separation Test GmbH",
                "company_type": "company",
                "street": "Test Street 1",
                "city": "Test City",
                "country_id": self.country_de.id,
            }
        )
        contact = self.env["res.partner"].create(
            {
                "name": "Hans Müller",
                "company_type": "person",
                "parent_id": company.id,
            }
        )
        options = {"fields": ["name", "address"]}

        result = self.contact_widget._render_address(
            contact, options, hide_country=False
        )
        self.assertIn("Hans Müller", str(result))
        self.assertIn("Separation Test GmbH", str(result))

        result = self.contact_widget._render_address(
            company, options, hide_country=False
        )
        self.assertIn("Separation Test GmbH", str(result))

        whitespace_partner = self.env["res.partner"].create(
            {"name": "  Whitespace Name  ", "company_type": "company"}
        )
        result = self.contact_widget._render_address(
            whitespace_partner, {"fields": ["name"]}, hide_country=False
        )
        self.assertIn("Whitespace Name", str(result))

    def test_render_address_with_res_users(self):
        """Test that _render_address handles res.users by resolving to partner."""
        partner = self.env["res.partner"].create(
            {
                "name": "Salesperson Partner",
                "street": "Verkäuferstraße 5",
                "city": "Hamburg",
                "country_id": self.country_de.id,
                "phone": "+49 40 9876543",
                "email": "sales@testcompany.de",
            }
        )
        user = self.env["res.users"].create(
            {
                "login": "test_salesperson@testcompany.de",
                "name": "Salesperson Partner",
                "partner_id": partner.id,
            }
        )

        result = self.contact_widget._render_address(
            user, {"fields": ["name", "address", "phone", "email"]}, hide_country=False
        )
        self.assertIsInstance(result, (str, Markup))
        self.assertIn("Salesperson Partner", str(result))
        self.assertIn("Verkäuferstraße 5", str(result))
        self.assertIn("+49 40 9876543", str(result))
        self.assertIn("sales@testcompany.de", str(result))

    def test_value_to_html_with_res_users(self):
        """Test that value_to_html handles res.users records."""
        partner = self.env["res.partner"].create(
            {
                "name": "User Partner",
                "street": "Userstraße 10",
                "city": "Munich",
                "country_id": self.country_de.id,
            }
        )
        user = self.env["res.users"].create(
            {
                "login": "test_user_vth@testcompany.de",
                "name": "User Partner",
                "partner_id": partner.id,
            }
        )

        result = self.contact_widget.value_to_html(
            user, {"fields": ["name", "address"]}
        )
        self.assertIsInstance(result, (str, Markup))
        self.assertIn("User Partner", str(result))

    def test_render_address_empty_user(self):
        """Test that empty res.users recordset does not crash."""
        empty_user = self.env["res.users"]

        # value_to_html catches empty recordsets before _render_address
        result = self.contact_widget.value_to_html(empty_user, {})
        self.assertFalse(result)

        # Call _render_address directly to test the internal guard
        result = self.contact_widget._render_address(empty_user, {})
        self.assertFalse(result)

    def test_render_address_empty_partner(self):
        """Test that empty res.partner recordset does not crash."""
        empty_partner = self.env["res.partner"]

        result = self.contact_widget._render_address(empty_partner, {})
        self.assertFalse(result)
