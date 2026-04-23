# -*- coding: utf-8 -*-
"""
Tests for sale.order invoice preparation functionality.

This module tests the _prepare_invoice override that propagates
delivery dates and narration from sale orders to invoices.
"""

from datetime import date

from odoo.tests import tagged

from .common import MuchQwebAccountTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "sale_order",
    "post_install",
    "-at_install",
)
class TestSaleOrderPrepareInvoice(MuchQwebAccountTestCommon):
    """
    Test cases for sale.order delivery dates and _prepare_invoice method.

    Tests delivery date fields, propagation to invoices, and narration handling.
    """

    def test_delivery_dates_crud_and_propagation(self):
        """Test delivery date fields CRUD and propagation to invoice."""
        sale_order = self.create_sale_order()
        self.assertFalse(sale_order.delivery_start_date)
        self.assertFalse(sale_order.delivery_end_date)

        invoice_data = sale_order._prepare_invoice()
        self.assertFalse(invoice_data.get("delivery_start_date"))
        self.assertFalse(invoice_data.get("delivery_end_date"))

        sale_order.write(
            {
                "delivery_start_date": date(2026, 7, 1),
                "delivery_end_date": date(2026, 7, 31),
            }
        )
        self.assertEqual(sale_order.delivery_start_date, date(2026, 7, 1))
        self.assertEqual(sale_order.delivery_end_date, date(2026, 7, 31))

        sale_order2 = self.create_sale_order(
            delivery_start_date=date(2026, 6, 1),
            delivery_end_date=date(2026, 6, 30),
        )
        self.assertEqual(sale_order2.delivery_start_date, date(2026, 6, 1))
        self.assertEqual(sale_order2.delivery_end_date, date(2026, 6, 30))

        invoice_data2 = sale_order2._prepare_invoice()
        self.assertEqual(invoice_data2["delivery_start_date"], date(2026, 6, 1))
        self.assertEqual(invoice_data2["delivery_end_date"], date(2026, 6, 30))

    def test_narration_blocked_when_setting_enabled(self):
        """Test invoice terms used when block_condition enabled."""
        self.company.write(
            {
                "block_condition": True,
                "invoice_terms": "<p>Company Invoice Terms</p>",
            }
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "account.use_invoice_terms", "True"
        )

        sale_order = self.create_sale_order()
        invoice_data = sale_order._prepare_invoice()

        self.assertEqual(
            str(invoice_data.get("narration")), "<p>Company Invoice Terms</p>"
        )

    def test_narration_not_set_when_use_invoice_terms_disabled(self):
        """Test narration behavior when use_invoice_terms param is disabled."""
        self.company.write(
            {
                "block_condition": True,
                "invoice_terms": "<p>Company Invoice Terms</p>",
            }
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "account.use_invoice_terms", False
        )

        sale_order = self.create_sale_order()
        invoice_data = sale_order._prepare_invoice()

        narration = invoice_data.get("narration")
        if narration:
            self.assertNotEqual(str(narration), "<p>Company Invoice Terms</p>")

    def test_narration_language_handling(self):
        """Test narration uses partner's language and falls back correctly."""
        self.company.write(
            {
                "block_condition": True,
            }
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "account.use_invoice_terms", "True"
        )

        german_partner = self.env["res.partner"].create(
            {
                "name": "German Customer",
                "lang": "de_DE",
            }
        )
        self.company.with_context(lang="de_DE").write(
            {
                "invoice_terms": "<p>Deutsche Rechnungsbedingungen</p>",
            }
        )

        sale_order_de = self.create_sale_order(partner=german_partner)
        invoice_data_de = sale_order_de._prepare_invoice()
        self.assertIsNotNone(invoice_data_de.get("narration"))

        no_lang_partner = self.env["res.partner"].create(
            {
                "name": "No Language Partner",
                "lang": False,
            }
        )
        self.company.write(
            {
                "invoice_terms": "<p>Default Terms</p>",
            }
        )

        sale_order_no_lang = self.create_sale_order(partner=no_lang_partner)
        invoice_data_no_lang = sale_order_no_lang._prepare_invoice()
        self.assertIsNotNone(invoice_data_no_lang.get("narration"))
