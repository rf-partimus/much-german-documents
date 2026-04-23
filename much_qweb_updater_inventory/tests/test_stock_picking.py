# -*- coding: utf-8 -*-
"""
Tests for stock.picking delivery document customization.

This module tests report header text computation, date formatting,
template data generation, and dynamic field validation.
"""

from datetime import datetime, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import MuchQwebInventoryTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_inventory",
    "stock_picking",
    "post_install",
    "-at_install",
)
class TestStockPickingReportHeaderText(MuchQwebInventoryTestCommon):
    """
    Test cases for report_header_text computed field and constraints.
    """

    def test_header_text_computation_and_language_handling(self):
        """Test header text defaults, language handling, and fallbacks."""
        picking = self.create_picking()
        self.assertEqual(
            picking.report_header_text, "<p>Default Delivery Description</p>"
        )

        self.company.write({"description_delivery": False})
        picking2 = self.create_picking()
        picking2._compute_report_header_text()
        self.assertFalse(picking2.report_header_text)

        self.company.write(
            {"description_delivery": "<p>Default Delivery Description</p>"}
        )
        self.company.with_context(lang="de_DE").write(
            {"description_delivery": "<p>Deutsche Lieferbeschreibung</p>"}
        )

        german_partner = self.env["res.partner"].create(
            {
                "name": "German Customer",
                "lang": "de_DE",
            }
        )
        picking3 = self.create_picking(partner=german_partner)
        picking3._compute_report_header_text()
        self.assertIsNotNone(picking3.report_header_text)

        no_lang_partner = self.env["res.partner"].create(
            {
                "name": "No Language Partner",
                "lang": False,
            }
        )
        picking4 = self.create_picking(partner=no_lang_partner)
        self.assertIsNotNone(picking4.report_header_text)

    def test_header_text_constraint_and_order_title(self):
        """Test dynamic field validation and order_title field."""
        picking = self.create_picking()
        picking.report_header_text = "<p>Partner: ${object.name}</p>"

        with self.assertRaises(ValidationError):
            picking.report_header_text = "<p>${object.nonexistent_field}</p>"

        picking2 = self.create_picking(order_title="Custom Delivery Title")
        self.assertEqual(picking2.order_title, "Custom Delivery Title")

        picking2.write({"order_title": "Updated Title"})
        self.assertEqual(picking2.order_title, "Updated Title")


@tagged(
    "much_unit",
    "much_qweb_updater_inventory",
    "stock_picking",
    "post_install",
    "-at_install",
)
class TestStockPickingFormatDateByLang(MuchQwebInventoryTestCommon):
    """
    Test cases for format_date_by_lang method.
    """

    def test_format_date_by_lang(self):
        """Test language-specific date formatting and edge cases."""
        german_partner = self.env["res.partner"].create(
            {
                "name": "German Customer",
                "lang": "de_DE",
            }
        )
        picking = self.create_picking(partner=german_partner)
        test_datetime = datetime(2026, 6, 15, 10, 30, 0)

        formatted = picking.format_date_by_lang(test_datetime)
        self.assertIsNotNone(formatted)
        self.assertIsInstance(formatted, str)

        no_lang_partner = self.env["res.partner"].create(
            {
                "name": "No Language Partner",
                "lang": False,
            }
        )
        picking2 = self.create_picking(partner=no_lang_partner)
        formatted2 = picking2.format_date_by_lang(test_datetime)
        self.assertIsNotNone(formatted2)

        picking3 = self.create_picking()
        self.assertIsNone(picking3.format_date_by_lang(None))
        self.assertFalse(picking3.format_date_by_lang(False))


@tagged(
    "much_unit",
    "much_qweb_updater_inventory",
    "stock_picking",
    "post_install",
    "-at_install",
)
class TestStockPickingTemplateData(MuchQwebInventoryTestCommon):
    """
    Test cases for get_l10n_din5008_template_data method.
    """

    def test_template_data_basic_fields(self):
        """Test template data includes/excludes basic fields correctly."""
        picking = self.create_picking(origin="SO001")
        data = picking.get_l10n_din5008_template_data()
        self.assert_field_in_data(data, "origin", "SO001")

        picking2 = self.create_picking(origin=False)
        data2 = picking2.get_l10n_din5008_template_data()
        self.assert_field_not_in_data(data2, "origin")

        scheduled = datetime.now() + timedelta(days=7)
        picking3 = self.create_picking(scheduled_date=scheduled)
        data3 = picking3.get_l10n_din5008_template_data()
        self.assert_field_in_data(data3, "shipping_date")

        picking4 = self.create_picking_with_moves()
        picking4.action_confirm()
        picking4.action_assign()
        for move in picking4.move_ids:
            move.quantity = move.product_uom_qty
        picking4.button_validate()
        data4 = picking4.get_l10n_din5008_template_data()
        self.assert_field_in_data(data4, "shipping_date")

        picking5 = self.create_picking(origin="TEST-001")
        picking5._compute_l10n_din5008_template_data()
        self.assertIsNotNone(picking5.l10n_din5008_template_data)

    def test_template_data_from_sale_order(self):
        """Test template data from linked sale order."""
        sale_order, picking = self.create_sale_order_with_picking()

        if not picking:
            return

        sale_order.write({"client_order_ref": "CUST-REF-001"})
        data = picking.get_l10n_din5008_template_data()
        self.assert_field_in_data(data, "customer_reference", "CUST-REF-001")

        sale_order.write({"client_order_ref": False})
        data2 = picking.get_l10n_din5008_template_data()
        self.assert_field_not_in_data(data2, "customer_reference")

        if "incoterm" in sale_order._fields:
            incoterm = self.env["account.incoterms"].search([], limit=1)
            if incoterm:
                sale_order.write(
                    {
                        "incoterm": incoterm.id,
                        "incoterm_location": "Hamburg Port",
                    }
                )
                data3 = picking.get_l10n_din5008_template_data()
                self.assert_field_in_data(data3, "incoterm")

                sale_order.write({"incoterm_location": False})
                data4 = picking.get_l10n_din5008_template_data()
                self.assert_field_in_data(data4, "incoterm")
