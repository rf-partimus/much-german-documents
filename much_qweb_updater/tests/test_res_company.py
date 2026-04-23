# -*- coding: utf-8 -*-
"""
Tests for res.company QWeb configuration fields.

This module tests the company configuration fields used for
logo sizing, footer customization, and report settings.
"""

from odoo.tests import tagged

from .common import MuchQwebTestCommon


@tagged("much_unit", "much_qweb_updater", "res_company", "post_install", "-at_install")
class TestResCompanyConfiguration(MuchQwebTestCommon):
    """
    Test cases for company configuration fields.

    Tests logo settings, footer customization, print settings,
    field persistence, defaults, and edge cases.
    """

    def test_boolean_fields_crud(self):
        """Test enabling, disabling, and persistence of all boolean fields."""
        boolean_fields = {
            "free_text_footer": True,
            "adjust_logo": True,
            "print_company": True,
        }
        self.company.write(boolean_fields)
        for field, value in boolean_fields.items():
            self.assertEqual(getattr(self.company, field), value)

        self.company.write({k: False for k in boolean_fields})
        for field in boolean_fields:
            self.assertFalse(getattr(self.company, field))

    def test_logo_unit_selection_and_dimensions(self):
        """Test all logo unit options and dimension values including boundaries."""
        test_cases = [
            {
                "logo_width_unit": "px",
                "logo_width": 150,
                "logo_height_unit": "px",
                "logo_height": 75,
            },
            {
                "logo_width_unit": "in",
                "logo_width": 2,
                "logo_height_unit": "in",
                "logo_height": 1,
            },
            {
                "logo_width_unit": "%",
                "logo_width": 50,
                "logo_height_unit": "%",
                "logo_height": 25,
            },
            {"logo_width": 0, "logo_height": 0},
            {"logo_width": 9999, "logo_height": 9999},
        ]
        for config in test_cases:
            self.company.write(config)
            for field, value in config.items():
                self.assertEqual(getattr(self.company, field), value)

    def test_footer_columns_and_font_size(self):
        """Test footer column HTML fields, font size, and special content."""
        config = {
            "column_1": "<p>Footer Column 1</p>",
            "column_2": "<p>Footer Column 2</p>",
            "column_3": "<p>Footer Column 3</p>",
            "column_4": "<p>Footer Column 4</p>",
            "footer_font_size": 14,
        }
        self.company.write(config)
        for field, value in config.items():
            self.assertEqual(getattr(self.company, field), value)

        self.company.write({k: False for k in config})
        for field in config:
            self.assertFalse(getattr(self.company, field))

        special_content = [
            '<p>Test &amp; "Special" </p>',
            "<p>Ümlauts: äöü, 日本語, émojis: 🎉</p>",
        ]
        for content in special_content:
            self.company.write({"column_1": content})
            self.assertEqual(self.company.column_1, content)

        for size in [1, 10, 100]:
            self.company.write({"footer_font_size": size})
            self.assertEqual(self.company.footer_font_size, size)

    def test_report_color_related_fields(self):
        """Test report color fields are properly related to primary/secondary colors."""
        color_tests = [
            {"primary_color": "#FF0000", "secondary_color": "#00FF00"},
            {"primary_color": "#123456", "secondary_color": "#ABCDEF"},
            {"primary_color": False, "secondary_color": False},
        ]
        for colors in color_tests:
            self.company.write(colors)
            self.assertEqual(self.company.report_primary_color, colors["primary_color"])
            self.assertEqual(
                self.company.report_secondary_color, colors["secondary_color"]
            )

    def test_full_configuration_persistence(self):
        """Test that full company configuration persists after cache invalidation."""
        config = {
            "free_text_footer": True,
            "column_1": "<p>Persistent Column 1</p>",
            "column_2": "<p>Persistent Column 2</p>",
            "column_3": "<p>Persistent Column 3</p>",
            "column_4": "<p>Persistent Column 4</p>",
            "footer_font_size": 14,
            "logo_width_unit": "in",
            "logo_width": 3,
            "logo_height_unit": "%",
            "logo_height": 25,
            "print_company": False,
            "adjust_logo": True,
        }
        self.company.write(config)
        self.company.invalidate_recordset()

        for field, value in config.items():
            self.assertEqual(getattr(self.company, field), value)

    def test_partial_update_preserves_other_fields(self):
        """Test partial updates don't affect unrelated fields."""
        self.company.write(
            {"footer_font_size": 10, "logo_width": 100, "logo_height": 50}
        )
        self.company.write({"footer_font_size": 16})

        self.assertEqual(self.company.footer_font_size, 16)
        self.assertEqual(self.company.logo_width, 100)
        self.assertEqual(self.company.logo_height, 50)


@tagged("much_unit", "much_qweb_updater", "res_company", "post_install", "-at_install")
class TestResCompanyDefaults(MuchQwebTestCommon):
    """
    Test cases for company field default values.
    """

    def test_new_company_defaults(self):
        """Test that new companies get correct default values for all field types."""
        new_company = self.env["res.company"].create({"name": "New Test Company"})

        self.assertFalse(new_company.free_text_footer)
        self.assertFalse(new_company.adjust_logo)
        self.assertTrue(new_company.print_company)

        self.assertEqual(new_company.footer_font_size, 10)
        self.assertFalse(new_company.logo_width)
        self.assertFalse(new_company.logo_height)

        self.assertEqual(new_company.logo_width_unit, "px")
        self.assertEqual(new_company.logo_height_unit, "px")

        for col in ["column_1", "column_2", "column_3", "column_4"]:
            self.assertFalse(getattr(new_company, col))


@tagged("much_unit", "much_qweb_updater", "res_company", "post_install", "-at_install")
class TestResCompanyMultiCompany(MuchQwebTestCommon):
    """
    Test cases for multi-company isolation and bulk operations.
    """

    def test_multi_company_isolation(self):
        """Test that company configurations are isolated between companies."""
        company_a = self.create_company_with_config(
            name="Company A",
            footer_font_size=12,
            column_1="<p>Company A Footer</p>",
        )
        company_b = self.create_company_with_config(
            name="Company B",
            footer_font_size=14,
            column_1="<p>Company B Footer</p>",
        )

        self.assertEqual(company_a.footer_font_size, 12)
        self.assertEqual(company_b.footer_font_size, 14)
        self.assertEqual(company_a.column_1, "<p>Company A Footer</p>")
        self.assertEqual(company_b.column_1, "<p>Company B Footer</p>")

        company_a.write({"footer_font_size": 16})
        self.assertEqual(company_a.footer_font_size, 16)
        self.assertEqual(company_b.footer_font_size, 14)

    def test_bulk_update_method(self):
        """Test bulk update method exists and handles various scenarios."""
        self.assertTrue(
            hasattr(self.company, "_update_report_header_text_bulk"),
            "Method _update_report_header_text_bulk should exist on res.company",
        )

        if not self.has_model("account.move"):
            self.skipTest("account.move model not available")

        self.company._update_report_header_text_bulk(
            table_name="account_move",
            partner_field="partner_id",
            field_mapping={"out_invoice": "name"},
            state_conditions={"out_invoice": "move_type = 'out_invoice'"},
        )

        self.company._update_report_header_text_bulk(
            table_name="account_move",
            partner_field="partner_id",
            field_mapping={None: "name"},
            state_conditions=None,
        )

        company_a = self.create_company_with_config(name="Company A")
        company_b = self.create_company_with_config(name="Company B")
        (company_a | company_b)._update_report_header_text_bulk(
            table_name="account_move",
            partner_field="partner_id",
            field_mapping={None: "name"},
            state_conditions=None,
        )
