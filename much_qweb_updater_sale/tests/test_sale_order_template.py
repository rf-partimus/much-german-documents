# -*- coding: utf-8 -*-
"""
Tests for sale.order.template customization.

This module tests the report_header_text and order_title fields
added to sale order templates.
"""

from odoo.tests import tagged

from .common import MuchQwebSaleTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_sale",
    "sale_order_template",
    "post_install",
    "-at_install",
)
class TestSaleOrderTemplateFields(MuchQwebSaleTestCommon):
    """
    Test cases for sale order template custom fields.

    Tests the report_header_text and order_title fields, propagation, and persistence.
    """

    def test_template_fields_crud_and_persistence(self):
        """Test template fields can be set, updated, cleared, and persist."""
        template = self.env["sale.order.template"].create(
            {
                "name": "Test Template",
                "report_header_text": "<p>Template Header</p>",
                "order_title": "Template Order Title",
            }
        )
        self.assertEqual(template.report_header_text, "<p>Template Header</p>")
        self.assertEqual(template.order_title, "Template Order Title")

        template.write(
            {
                "report_header_text": "<p>Updated Header</p>",
                "order_title": "Updated Title",
            }
        )
        self.assertEqual(template.report_header_text, "<p>Updated Header</p>")
        self.assertEqual(template.order_title, "Updated Title")

        template2 = self.env["sale.order.template"].create(
            {
                "name": "Empty Fields Template",
                "report_header_text": False,
                "order_title": False,
            }
        )
        self.assertFalse(template2.report_header_text)
        self.assertFalse(template2.order_title)

        template3 = self.env["sale.order.template"].create(
            {
                "name": "Persistence Test",
                "report_header_text": "<p>Persistent Header</p>",
                "order_title": "Persistent Title",
            }
        )
        template3.invalidate_recordset()
        self.assertEqual(template3.report_header_text, "<p>Persistent Header</p>")
        self.assertEqual(template3.order_title, "Persistent Title")

    def test_template_propagation_and_translation(self):
        """Test template fields propagate to orders and support translation."""
        order = self.create_sale_order()
        order.sale_order_template_id = self.sale_template.id
        order._onchange_sale_order_template_id()

        self.assertEqual(
            order.report_header_text, self.sale_template.report_header_text
        )
        self.assertEqual(order.order_title, self.sale_template.order_title)

        order.sale_order_template_id = False
        self.assertIsNotNone(order.report_header_text)

        self.sale_template.write(
            {
                "report_header_text": "<p>English Header</p>",
                "order_title": "English Title",
            }
        )
        self.sale_template.with_context(lang="de_DE").write(
            {
                "report_header_text": "<p>Deutscher Header</p>",
                "order_title": "Deutscher Titel",
            }
        )
        german_header = self.sale_template.with_context(lang="de_DE").report_header_text
        self.assertIn("Deutscher", german_header)
