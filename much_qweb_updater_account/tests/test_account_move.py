# -*- coding: utf-8 -*-
"""
Tests for account.move invoice customization.

This module tests delivery date management, report header text computation,
date validation, and template data generation for invoices.
"""

from datetime import date
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from .common import MuchQwebAccountTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move",
    "post_install",
    "-at_install",
)
class TestAccountMoveReportHeaderText(MuchQwebAccountTestCommon):
    """Test cases for report_header_text field and related functionality."""

    def test_report_header_text_default_invoice(self):
        """Test report_header_text defaults to company description for invoices."""
        invoice = self.create_invoice(move_type="out_invoice")
        self.assertEqual(
            invoice.report_header_text, "<p>Default Invoice Description</p>"
        )

    def test_report_header_text_default_refund(self):
        """Test report_header_text defaults to company description for refunds."""
        refund = self.create_invoice(move_type="out_refund")
        self.assertEqual(
            refund.report_header_text, "<p>Default Credit Note Description</p>"
        )

    def test_report_header_text_false_when_company_description_empty(self):
        """Test report_header_text is False when company description is empty."""
        self.company.write({"description_inv": False})
        invoice = self.create_invoice(move_type="out_invoice")
        self.assertFalse(invoice.report_header_text)

    def test_report_header_text_manual_flag_set_on_manual_edit(self):
        """Test that manual flag is set when user manually edits the field."""
        invoice = self.create_invoice(move_type="out_invoice")
        invoice.report_header_text = "<p>Manual Text</p>"
        self.assertTrue(invoice.report_header_text_manual)

    def test_report_header_text_manual_flag_cleared_when_emptied(self):
        """Test that manual flag is cleared when field is emptied."""
        invoice = self.create_invoice(move_type="out_invoice")
        invoice.report_header_text = "<p>Manual Text</p>"
        self.assertTrue(invoice.report_header_text_manual)
        invoice.report_header_text = False
        self.assertFalse(invoice.report_header_text_manual)

    def test_report_header_text_preserved_on_partner_change(self):
        """Test manually set text is preserved when partner changes."""
        invoice = self.create_invoice(move_type="out_invoice")
        invoice.report_header_text = "<p>Manual Text</p>"
        invoice.partner_id = self.partner_vendor
        self.assertEqual(invoice.report_header_text, "<p>Manual Text</p>")

    def test_report_header_text_constraint_valid_dynamic_field(self):
        """Test constraint passes for valid dynamic field references."""
        invoice = self.create_invoice(move_type="out_invoice")
        invoice.report_header_text = "<p>Valid ${object.name}</p>"
        self.assertEqual(invoice.report_header_text, "<p>Valid ${object.name}</p>")

    def test_report_header_text_constraint_invalid_dynamic_field(self):
        """Test constraint raises ValidationError for invalid dynamic field."""
        invoice = self.create_invoice(move_type="out_invoice")
        with self.assertRaises(ValidationError):
            invoice.report_header_text = "<p>${object.nonexistent_field}</p>"

    def test_narration_constraint_valid_dynamic_field(self):
        """Test narration constraint passes for valid dynamic field."""
        invoice = self.create_invoice(move_type="out_invoice")
        invoice.narration = "<p>Valid ${object.name}</p>"
        self.assertEqual(invoice.narration, "<p>Valid ${object.name}</p>")

    def test_narration_constraint_invalid_dynamic_field(self):
        """Test narration constraint raises ValidationError for invalid field."""
        invoice = self.create_invoice(move_type="out_invoice")
        with self.assertRaises(ValidationError):
            invoice.narration = "<p>${object.invalid_field}</p>"

    def test_report_header_text_with_partner_language(self):
        """Test report_header_text respects partner language."""
        self.partner_customer.write({"lang": "de_DE"})
        self.company.with_context(lang="de_DE").write(
            {"description_inv": "<p>Deutsche Rechnungsbeschreibung</p>"}
        )
        invoice = self.create_invoice(
            move_type="out_invoice", partner=self.partner_customer
        )
        self.assertEqual(
            invoice.report_header_text, "<p>Deutsche Rechnungsbeschreibung</p>"
        )

    def test_report_header_text_other_move_types(self):
        """Test report_header_text is False for non-invoice/refund move types."""
        entry = self.env["account.move"].create(
            {
                "move_type": "entry",
                "company_id": self.company.id,
                "journal_id": self.sale_journal.id,
            }
        )
        self.assertFalse(entry.report_header_text)


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move",
    "post_install",
    "-at_install",
)
class TestAccountMovePrintTimeFrame(MuchQwebAccountTestCommon):
    """Test cases for print_time_frame related field."""

    def test_print_time_frame_related_to_company(self):
        """Test print_time_frame reflects company setting."""
        self.company.write({"print_time_frame": True})
        invoice = self.create_invoice()
        self.assertTrue(invoice.print_time_frame)

        self.company.write({"print_time_frame": False})
        invoice.invalidate_recordset()
        self.assertFalse(invoice.print_time_frame)

    def test_order_title_field(self):
        """Test order_title field CRUD operations."""
        invoice = self.create_invoice()
        self.assertFalse(invoice.order_title)

        invoice.order_title = "Test Order"
        self.assertEqual(invoice.order_title, "Test Order")

        invoice.order_title = False
        self.assertFalse(invoice.order_title)


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move",
    "post_install",
    "-at_install",
)
class TestAccountMoveDeliveryDates(MuchQwebAccountTestCommon):
    """Test cases for delivery date fields and validation."""

    def test_delivery_dates_default_values(self):
        """Test delivery dates have default values on creation."""
        invoice = self.create_invoice_with_lines()
        self.assertTrue(invoice.delivery_start_date)
        self.assertTrue(invoice.delivery_end_date)

    def test_delivery_dates_crud(self):
        """Test delivery date fields can be set and retrieved."""
        invoice = self.create_invoice_with_lines()
        invoice.write(
            {
                "delivery_start_date": date(2026, 6, 1),
                "delivery_end_date": date(2026, 6, 30),
            }
        )
        self.assertEqual(invoice.delivery_start_date, date(2026, 6, 1))
        self.assertEqual(invoice.delivery_end_date, date(2026, 6, 30))

    def test_validate_dates_both_empty(self):
        """Test validation passes when both dates are empty."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write({"delivery_start_date": False, "delivery_end_date": False})
        self.assertTrue(invoice.validate_dates_are_months_apart(line))

    def test_validate_dates_start_only(self):
        """Test validation passes when only start date is set."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write(
            {"delivery_start_date": date(2026, 6, 1), "delivery_end_date": False}
        )
        self.assertTrue(invoice.validate_dates_are_months_apart(line))

    def test_validate_dates_end_only(self):
        """Test validation passes when only end date is set."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write(
            {"delivery_start_date": False, "delivery_end_date": date(2026, 6, 30)}
        )
        self.assertTrue(invoice.validate_dates_are_months_apart(line))

    def test_validate_dates_same_day(self):
        """Test validation passes when both dates are the same day."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write(
            {
                "delivery_start_date": date(2026, 6, 15),
                "delivery_end_date": date(2026, 6, 15),
            }
        )
        self.assertTrue(invoice.validate_dates_are_months_apart(line))

    def test_validate_dates_exactly_one_month_apart(self):
        """Test validation passes for dates exactly one month apart."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write(
            {
                "delivery_start_date": date(2026, 6, 15),
                "delivery_end_date": date(2026, 7, 14),
            }
        )
        self.assertTrue(invoice.validate_dates_are_months_apart(line))
        invoice._compute_validate_invoice_dates()
        self.assertFalse(invoice.delivery_date_error_message)

    def test_validate_dates_full_year(self):
        """Test validation passes for full year span."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write(
            {
                "delivery_start_date": date(2026, 1, 1),
                "delivery_end_date": date(2026, 12, 31),
            }
        )
        self.assertTrue(invoice.validate_dates_are_months_apart(line))

    def test_validate_dates_not_months_apart(self):
        """Test validation fails for dates not exactly months apart."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write(
            {
                "delivery_start_date": date(2026, 6, 15),
                "delivery_end_date": date(2026, 7, 20),
            }
        )
        self.assertFalse(invoice.validate_dates_are_months_apart(line))
        invoice._compute_validate_invoice_dates()
        self.assertIn(
            "not exact months apart", invoice.delivery_date_error_message.lower()
        )

    def test_validate_dates_start_after_end(self):
        """Test validation error when start date is after end date."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]
        line.write(
            {
                "delivery_start_date": date(2026, 7, 15),
                "delivery_end_date": date(2026, 6, 15),
            }
        )
        invoice._compute_validate_invoice_dates()
        self.assertIn("after end date", invoice.delivery_date_error_message.lower())


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move",
    "post_install",
    "-at_install",
)
class TestAccountMoveDeliveryDatePropagation(MuchQwebAccountTestCommon):
    """Test cases for delivery date propagation between move and lines."""

    def test_propagate_dates_from_move_to_lines(self):
        """Test delivery dates propagate from move to all lines."""
        invoice = self.create_invoice_with_lines(line_count=2)
        invoice.write(
            {
                "delivery_start_date": date(2026, 8, 1),
                "delivery_end_date": date(2026, 8, 31),
            }
        )
        for line in invoice.invoice_line_ids:
            self.assertEqual(line.delivery_start_date, date(2026, 8, 1))
            self.assertEqual(line.delivery_end_date, date(2026, 8, 31))

    def test_disable_set_line_date_context(self):
        """Test disable_set_line_date context prevents line updates."""
        invoice = self.create_invoice_with_lines(line_count=2)
        invoice.invoice_line_ids[0].write(
            {
                "delivery_start_date": date(2026, 5, 1),
                "delivery_end_date": date(2026, 5, 31),
            }
        )
        invoice.with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": date(2026, 9, 1),
            }
        )
        self.assertEqual(
            invoice.invoice_line_ids[0].delivery_start_date, date(2026, 5, 1)
        )

    def test_propagate_dates_from_lines_to_move(self):
        """Test move dates expand when line dates are outside range."""
        invoice = self.create_invoice_with_lines(line_count=2)
        invoice.write(
            {
                "delivery_start_date": date(2026, 6, 1),
                "delivery_end_date": date(2026, 6, 30),
            }
        )
        invoice.invoice_line_ids[0].with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": date(2026, 3, 1),
                "delivery_end_date": date(2026, 10, 31),
            }
        )
        invoice._propagate_delivery_date_changes({"line_ids": True})
        self.assertEqual(invoice.delivery_start_date, date(2026, 3, 1))
        self.assertEqual(invoice.delivery_end_date, date(2026, 10, 31))

    def test_propagate_dates_fills_empty_lines(self):
        """Test move dates fill in empty line dates."""
        invoice = self.create_invoice_with_lines()
        invoice.write(
            {
                "delivery_start_date": date(2026, 7, 1),
                "delivery_end_date": date(2026, 7, 31),
            }
        )
        for line in invoice.line_ids:
            line.with_context(disable_set_line_date=True).write(
                {
                    "delivery_start_date": False,
                    "delivery_end_date": False,
                }
            )
        invoice._propagate_delivery_date_changes({})
        filled_lines = invoice.line_ids.filtered(
            lambda line: line.delivery_start_date == date(2026, 7, 1)
        )
        self.assertTrue(filled_lines)

    def test_create_with_delivery_dates_propagates_to_lines(self):
        """Test that create() propagates delivery dates to lines."""
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_customer.id,
                "company_id": self.company.id,
                "journal_id": self.sale_journal.id,
                "delivery_start_date": date(2026, 4, 1),
                "delivery_end_date": date(2026, 4, 30),
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Line",
                            "quantity": 1,
                            "price_unit": 100.0,
                            "account_id": self.account_income.id,
                        },
                    )
                ],
            }
        )
        for line in invoice.invoice_line_ids:
            self.assertEqual(line.delivery_start_date, date(2026, 4, 1))
            self.assertEqual(line.delivery_end_date, date(2026, 4, 30))

    def test_din5008_report_respects_incoterm_toggle(self):
        """Ensure the DIN5008 QWeb report obeys the company incoterm toggle."""
        incoterm = self.env["account.incoterms"].create(
            {
                "name": "EXW",
                "code": "EXW",
            }
        )
        invoice_vals = {
            "invoice_incoterm_id": incoterm.id,
        }
        if "incoterm_location" in self.env["account.move"]._fields:
            invoice_vals["incoterm_location"] = "Berlin"
        invoice = self.create_invoice_with_lines(**invoice_vals)
        invoice.action_post()

        html_enabled = self.render_din5008_invoice_html(invoice)
        self.assertIn("Incoterm", html_enabled)
        self.assertIn("EXW", html_enabled)
        if "incoterm_location" in self.env["account.move"]._fields:
            self.assertIn("Berlin", html_enabled)

        self.company.write({"print_incoterm": False})
        html_disabled = self.render_din5008_invoice_html(invoice)
        self.assertNotIn("Incoterm", html_disabled)
        self.assertNotIn("EXW", html_disabled)
        self.company.write({"print_incoterm": True})

    def test_din5008_report_hides_without_incoterm(self):
        """Incoterm row stays hidden when no incoterm is set."""
        invoice_vals = {}
        if "incoterm_location" in self.env["account.move"]._fields:
            invoice_vals["incoterm_location"] = False
        invoice = self.create_invoice_with_lines(**invoice_vals)
        invoice.action_post()

        html = self.render_din5008_invoice_html(invoice)
        self.assertNotIn("Incoterm", html)

    def test_din5008_report_incoterm_label_translated(self):
        """Incoterm label should be translated according to report language."""
        incoterm = self.env["account.incoterms"].create(
            {
                "name": "FCA",
                "code": "FCA",
            }
        )
        invoice = self.create_invoice_with_lines(invoice_incoterm_id=incoterm.id)
        invoice.action_post()

        html_de = self.render_din5008_invoice_html(invoice, context={"lang": "de_DE"})
        self.assertIn("Lieferbedingungen", html_de)
