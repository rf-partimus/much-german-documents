# -*- coding: utf-8 -*-
"""
Tests for account.move.line delivery date fields.

This module tests the delivery_start_date and delivery_end_date
fields added to invoice lines.
"""

from datetime import date

from odoo.tests import tagged

from .common import MuchQwebAccountTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move_line",
    "post_install",
    "-at_install",
)
class TestAccountMoveLineDeliveryDates(MuchQwebAccountTestCommon):
    """
    Test cases for delivery date fields on account.move.line.

    Tests default value inheritance, independent line date management,
    field types, and synchronization with move.
    """

    def test_line_delivery_dates_inherit_from_move(self):
        """Test line dates inherit from move on creation."""
        invoice = self.create_invoice_with_lines(
            delivery_start_date=date(2026, 6, 1),
            delivery_end_date=date(2026, 6, 30),
            line_count=3,
        )

        for line in invoice.invoice_line_ids:
            self.assertEqual(line.delivery_start_date, date(2026, 6, 1))
            self.assertEqual(line.delivery_end_date, date(2026, 6, 30))

    def test_line_delivery_dates_can_be_set_independently(self):
        """Test each line can have independent delivery dates."""
        invoice = self.create_invoice_with_lines(
            delivery_start_date=date(2026, 6, 1),
            delivery_end_date=date(2026, 6, 30),
            line_count=3,
        )

        dates = [
            (date(2026, 4, 1), date(2026, 4, 30)),
            (date(2026, 5, 1), date(2026, 5, 31)),
            (date(2026, 6, 1), date(2026, 6, 30)),
        ]

        for i, line in enumerate(invoice.invoice_line_ids):
            line.with_context(disable_set_line_date=True).write(
                {
                    "delivery_start_date": dates[i][0],
                    "delivery_end_date": dates[i][1],
                }
            )

        for i, line in enumerate(invoice.invoice_line_ids):
            self.assertEqual(line.delivery_start_date, dates[i][0])
            self.assertEqual(line.delivery_end_date, dates[i][1])

    def test_line_delivery_dates_can_be_cleared(self):
        """Test line delivery dates can be set to False."""
        invoice = self.create_invoice_with_lines(
            delivery_start_date=date(2026, 6, 1),
            delivery_end_date=date(2026, 6, 30),
        )

        invoice.invoice_line_ids[0].with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": False,
                "delivery_end_date": False,
            }
        )

        self.assertFalse(invoice.invoice_line_ids[0].delivery_start_date)
        self.assertFalse(invoice.invoice_line_ids[0].delivery_end_date)

    def test_delivery_date_field_types(self):
        """Test delivery dates are proper date fields."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]

        line.write(
            {
                "delivery_start_date": date(2026, 6, 15),
                "delivery_end_date": date(2026, 7, 14),
            }
        )

        self.assertIsInstance(line.delivery_start_date, date)
        self.assertEqual(line.delivery_start_date.year, 2026)
        self.assertEqual(line.delivery_start_date.month, 6)
        self.assertEqual(line.delivery_start_date.day, 15)

        self.assertIsInstance(line.delivery_end_date, date)
        self.assertEqual(line.delivery_end_date.year, 2026)
        self.assertEqual(line.delivery_end_date.month, 7)
        self.assertEqual(line.delivery_end_date.day, 14)


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move_line",
    "post_install",
    "-at_install",
)
class TestAccountMoveLineSynchronization(MuchQwebAccountTestCommon):
    """
    Test cases for delivery date synchronization between move and lines.
    """

    def test_move_date_change_propagates_to_lines(self):
        """Test that changing move dates updates all lines."""
        invoice = self.create_invoice_with_lines(line_count=3)
        new_start = date(2026, 9, 1)
        new_end = date(2026, 9, 30)

        invoice.write(
            {
                "delivery_start_date": new_start,
                "delivery_end_date": new_end,
            }
        )

        for line in invoice.invoice_line_ids:
            self.assertEqual(line.delivery_start_date, new_start)
            self.assertEqual(line.delivery_end_date, new_end)

    def test_line_date_change_expands_move_dates(self):
        """Test that line date outside move range expands move dates."""
        invoice = self.create_invoice_with_lines(line_count=3)
        invoice.write(
            {
                "delivery_start_date": date(2026, 6, 1),
                "delivery_end_date": date(2026, 6, 30),
            }
        )

        invoice.invoice_line_ids[0].with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": date(2026, 5, 1),
            }
        )

        invoice._propagate_delivery_date_changes({"line_ids": True})

        self.assertEqual(invoice.delivery_start_date, date(2026, 5, 1))

    def test_new_line_inherits_move_dates(self):
        """Test newly added line inherits move delivery dates."""
        invoice = self.create_invoice(
            delivery_start_date=date(2026, 6, 1),
            delivery_end_date=date(2026, 6, 30),
        )

        self.env["account.move.line"].create(
            {
                "move_id": invoice.id,
                "name": "New Test Line",
                "quantity": 1,
                "price_unit": 50.0,
                "account_id": self.account_income.id,
            }
        )

        invoice._propagate_delivery_date_changes({})

        for line in invoice.line_ids:
            if line.delivery_start_date:
                self.assertEqual(line.delivery_start_date, date(2026, 6, 1))
            if line.delivery_end_date:
                self.assertEqual(line.delivery_end_date, date(2026, 6, 30))

    def test_disable_set_line_date_context_prevents_propagation(self):
        """Test that disable_set_line_date context prevents line updates."""
        invoice = self.create_invoice_with_lines(line_count=2)
        invoice.write(
            {
                "delivery_start_date": date(2026, 6, 1),
                "delivery_end_date": date(2026, 6, 30),
            }
        )

        invoice.invoice_line_ids[0].with_context(disable_set_line_date=True).write(
            {"delivery_start_date": date(2026, 3, 1)}
        )

        invoice.with_context(disable_set_line_date=True).write(
            {"delivery_start_date": date(2026, 7, 1)}
        )

        self.assertEqual(
            invoice.invoice_line_ids[0].delivery_start_date, date(2026, 3, 1)
        )


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move_line",
    "post_install",
    "-at_install",
)
class TestAccountMoveLineEdgeCases(MuchQwebAccountTestCommon):
    """
    Test cases for edge cases in account.move.line delivery dates.
    """

    def test_line_with_only_start_date(self):
        """Test line with only start date set."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]

        line.with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": date(2026, 6, 1),
                "delivery_end_date": False,
            }
        )

        self.assertEqual(line.delivery_start_date, date(2026, 6, 1))
        self.assertFalse(line.delivery_end_date)

    def test_line_with_only_end_date(self):
        """Test line with only end date set."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]

        line.with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": False,
                "delivery_end_date": date(2026, 6, 30),
            }
        )

        self.assertFalse(line.delivery_start_date)
        self.assertEqual(line.delivery_end_date, date(2026, 6, 30))

    def test_multiple_lines_different_dates(self):
        """Test multiple lines can have completely different date ranges."""
        invoice = self.create_invoice_with_lines(line_count=3)

        lines = invoice.invoice_line_ids
        lines[0].with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": date(2026, 1, 1),
                "delivery_end_date": date(2026, 1, 31),
            }
        )
        lines[1].with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": date(2026, 6, 1),
                "delivery_end_date": date(2026, 6, 30),
            }
        )
        lines[2].with_context(disable_set_line_date=True).write(
            {
                "delivery_start_date": date(2026, 12, 1),
                "delivery_end_date": date(2026, 12, 31),
            }
        )

        self.assertEqual(lines[0].delivery_start_date, date(2026, 1, 1))
        self.assertEqual(lines[1].delivery_start_date, date(2026, 6, 1))
        self.assertEqual(lines[2].delivery_start_date, date(2026, 12, 1))

    def test_line_dates_persist_after_move_invalidation(self):
        """Test line dates persist after cache invalidation."""
        invoice = self.create_invoice_with_lines()
        line = invoice.invoice_line_ids[0]

        line.write(
            {
                "delivery_start_date": date(2026, 8, 15),
                "delivery_end_date": date(2026, 9, 14),
            }
        )

        line.invalidate_recordset()

        self.assertEqual(line.delivery_start_date, date(2026, 8, 15))
        self.assertEqual(line.delivery_end_date, date(2026, 9, 14))

    def test_line_dates_on_non_invoice_lines(self):
        """Test delivery dates work on non-invoice move lines."""
        invoice = self.create_invoice_with_lines()

        for line in invoice.line_ids:
            line.with_context(disable_set_line_date=True).write(
                {
                    "delivery_start_date": date(2026, 7, 1),
                    "delivery_end_date": date(2026, 7, 31),
                }
            )
            self.assertEqual(line.delivery_start_date, date(2026, 7, 1))
            self.assertEqual(line.delivery_end_date, date(2026, 7, 31))
            break

    def test_line_creation_with_explicit_dates(self):
        """Test creating line with explicit dates ignores move dates."""
        invoice = self.create_invoice(
            delivery_start_date=date(2026, 6, 1),
            delivery_end_date=date(2026, 6, 30),
        )

        line = self.env["account.move.line"].create(
            {
                "move_id": invoice.id,
                "name": "Line with explicit dates",
                "quantity": 1,
                "price_unit": 100.0,
                "account_id": self.account_income.id,
                "delivery_start_date": date(2026, 3, 1),
                "delivery_end_date": date(2026, 3, 31),
            }
        )

        self.assertEqual(line.delivery_start_date, date(2026, 3, 1))
        self.assertEqual(line.delivery_end_date, date(2026, 3, 31))
