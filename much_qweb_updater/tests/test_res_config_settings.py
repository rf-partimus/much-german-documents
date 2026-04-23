# -*- coding: utf-8 -*-
"""
Tests for res.config.settings configuration interface.

This module tests the configuration settings interface that exposes
company settings to administrators through the Settings UI.
"""

from odoo.tests import tagged

from .common import MuchQwebTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettings(MuchQwebTestCommon):
    """
    Test cases for res.config.settings related fields and methods.

    Tests bidirectional sync between settings and company, execute behavior,
    and the edit_paper_format action.
    """

    def test_all_fields_write_and_sync(self):
        """Test all field types write values to company and can be cleared."""
        config_set = {
            "free_text_footer": True,
            "adjust_logo": True,
            "print_company": True,
            "column_1": "<p>Col 1</p>",
            "column_2": "<p>Col 2</p>",
            "column_3": "<p>Col 3</p>",
            "column_4": "<p>Col 4</p>",
            "footer_font_size": 14,
            "logo_width": 200,
            "logo_height": 100,
        }
        self.env["res.config.settings"].create(config_set)
        self.company.invalidate_recordset()

        for field, value in config_set.items():
            self.assertEqual(getattr(self.company, field), value)

        config_clear = {
            k: False if isinstance(v, (bool, str)) else 0 for k, v in config_set.items()
        }
        self.env["res.config.settings"].create(config_clear)
        self.company.invalidate_recordset()

        for field in config_set:
            self.assertFalse(getattr(self.company, field))

    def test_selection_fields_all_options(self):
        """Test all selection field options for logo units."""
        for unit in ["px", "in", "%"]:
            self.env["res.config.settings"].create(
                {
                    "logo_width_unit": unit,
                    "logo_height_unit": unit,
                }
            )
            self.company.invalidate_recordset()
            self.assertEqual(self.company.logo_width_unit, unit)
            self.assertEqual(self.company.logo_height_unit, unit)

    def test_settings_read_from_company(self):
        """Test all settings fields reflect current company values."""
        config = {
            "free_text_footer": True,
            "column_1": "<p>Company Col 1</p>",
            "column_2": "<p>Company Col 2</p>",
            "column_3": "<p>Company Col 3</p>",
            "column_4": "<p>Company Col 4</p>",
            "footer_font_size": 16,
            "print_company": False,
            "adjust_logo": True,
            "logo_width_unit": "%",
            "logo_width": 50,
            "logo_height_unit": "in",
            "logo_height": 2,
        }
        self.company.write(config)
        settings = self.env["res.config.settings"].create({})

        for field, value in config.items():
            self.assertEqual(getattr(settings, field), value)

    def test_settings_execute_persists_all_fields(self):
        """Test that calling execute() persists all settings to company."""
        config = {
            "free_text_footer": True,
            "column_1": "<p>Exec Col 1</p>",
            "column_2": "<p>Exec Col 2</p>",
            "column_3": "<p>Exec Col 3</p>",
            "column_4": "<p>Exec Col 4</p>",
            "footer_font_size": 12,
            "print_company": False,
            "adjust_logo": True,
            "logo_width_unit": "in",
            "logo_width": 3,
            "logo_height_unit": "%",
            "logo_height": 50,
        }
        settings = self.env["res.config.settings"].create(config)
        settings.execute()

        self.company.invalidate_recordset()
        for field, value in config.items():
            self.assertEqual(getattr(self.company, field), value)

    def test_edit_paper_format_action(self):
        """Test edit_paper_format returns correct action with/without paperformat."""
        settings = self.env["res.config.settings"].create({})
        result = settings.edit_paper_format()

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("type"), "ir.actions.act_window")
        self.assertEqual(result.get("res_model"), "report.paperformat")
        self.assertEqual(result.get("view_mode"), "form")
        self.assertEqual(result.get("res_id"), self.env.company.paperformat_id.id)

        self.company.write({"paperformat_id": False})
        result = settings.edit_paper_format()
        self.assertFalse(result.get("res_id"))


@tagged(
    "much_unit",
    "much_qweb_updater",
    "res_config_settings",
    "post_install",
    "-at_install",
)
class TestResConfigSettingsEdgeCases(MuchQwebTestCommon):
    """
    Test cases for edge cases in res.config.settings.
    """

    def test_settings_with_different_company_and_special_content(self):
        """Test settings work correctly with different company/special HTML content."""
        new_company = self.create_company_with_config(
            name="Settings Test Company",
            footer_font_size=20,
            column_1="<p>New Company Column</p>",
        )

        self.env["res.config.settings"].with_company(new_company).create(
            {
                "footer_font_size": 22,
            }
        )

        new_company.invalidate_recordset()
        self.assertEqual(new_company.footer_font_size, 22)
        self.assertEqual(self.company.footer_font_size, 10)

        special_html = '<p class="test">Content &amp; "more"</p>'
        self.env["res.config.settings"].create({"column_1": special_html})
        self.company.invalidate_recordset()
        self.assertEqual(self.company.column_1, special_html)

    def test_multiple_settings_instances_and_defaults(self):
        """Test multiple settings instances and that defaults come from company."""
        self.company.write(
            {
                "free_text_footer": True,
                "footer_font_size": 15,
                "logo_width_unit": "in",
            }
        )

        settings = self.env["res.config.settings"].create({})
        self.assertTrue(settings.free_text_footer)
        self.assertEqual(settings.footer_font_size, 15)
        self.assertEqual(settings.logo_width_unit, "in")

        self.env["res.config.settings"].create({"footer_font_size": 14})
        self.env["res.config.settings"].create({"footer_font_size": 16})

        self.company.invalidate_recordset()
        self.assertEqual(self.company.footer_font_size, 16)
