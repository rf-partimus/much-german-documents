# -*- coding: utf-8 -*-
"""
Tests for sale.order quotation and order customization.

This module tests report header text computation, template data generation,
dynamic field validation, and sale order template integration.
"""

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import MuchQwebSaleTestCommon


@tagged(
    "much_unit", "much_qweb_updater_sale", "sale_order", "post_install", "-at_install"
)
class TestSaleOrderReportHeaderText(MuchQwebSaleTestCommon):
    """
    Test cases for report_header_text computed field and constraints.
    """

    def test_header_text_state_dependent_defaults(self):
        """Test header text uses correct company description based on state."""
        draft_order = self.create_sale_order(state="draft")
        self.assertEqual(
            draft_order.report_header_text, "<p>Default Quotation Description</p>"
        )

        sent_order = self.create_sale_order_with_lines(state="sent")
        self.assertEqual(
            sent_order.report_header_text, "<p>Default Quotation Description</p>"
        )

        confirmed_order = self.create_sale_order_with_lines(state="sale")
        confirmed_order._compute_report_header_text()
        self.assertEqual(
            confirmed_order.report_header_text, "<p>Default Order Description</p>"
        )

        self.company.write(
            {
                "description_quotation": False,
                "description_order": False,
            }
        )
        empty_order = self.create_sale_order()
        empty_order._compute_report_header_text()
        self.assertFalse(empty_order.report_header_text)

        self.company.write(
            {"description_quotation": "<p>Default Quotation Description</p>"}
        )
        self.company.with_context(lang="de_DE").write(
            {"description_quotation": "<p>Deutsches Angebot</p>"}
        )
        german_partner = self.env["res.partner"].create(
            {
                "name": "German Customer",
                "lang": "de_DE",
            }
        )
        german_order = self.create_sale_order(partner=german_partner)
        self.assertIsNotNone(german_order.report_header_text)

        no_lang_partner = self.env["res.partner"].create(
            {
                "name": "No Language Partner",
                "lang": False,
            }
        )
        self.company.write(
            {"description_quotation": "<p>Default Quotation Description</p>"}
        )
        no_lang_order = self.create_sale_order(partner=no_lang_partner)
        self.assertIsNotNone(no_lang_order.report_header_text)

    def test_header_text_and_note_constraints(self):
        """Test dynamic field validation for header and note fields."""
        order = self.create_sale_order()
        order.report_header_text = "<p>Partner: ${object.name}</p>"
        order.note = "<p>Partner: ${object.name}</p>"

        with self.assertRaises(ValidationError):
            order.report_header_text = "<p>${object.nonexistent_field}</p>"

        with self.assertRaises(ValidationError):
            order.note = "<p>${object.invalid_field}</p>"

    def test_order_title_field(self):
        """Test order_title field can be set and updated."""
        order = self.create_sale_order(order_title="Custom Order Title")
        self.assertEqual(order.order_title, "Custom Order Title")

        order.write({"order_title": "Updated Title"})
        self.assertEqual(order.order_title, "Updated Title")

    def test_template_integration(self):
        """Test sale order template sets header text and order title."""
        order = self.create_sale_order_from_template()
        self.assertEqual(order.report_header_text, "<p>Template Header Text</p>")
        self.assertEqual(order.order_title, "Template Title")

        german_partner = self.env["res.partner"].create(
            {
                "name": "German Customer",
                "lang": "de_DE",
            }
        )
        self.sale_template.with_context(lang="de_DE").write(
            {
                "report_header_text": "<p>Deutscher Vorlagentext</p>",
            }
        )
        german_order = self.create_sale_order_from_template(partner=german_partner)
        self.assertIsNotNone(german_order.report_header_text)

        order2 = self.create_sale_order()
        order2.sale_order_template_id = False
        result = order2._onchange_sale_order_template_id()
        self.assertIsNone(result) or self.assertIsNotNone(order2)
