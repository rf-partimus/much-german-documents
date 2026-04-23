# -*- coding: utf-8 -*-
"""
Tests for account.move.reversal wizard customization.

This module tests the _prepare_default_reversal override that
sets the credit note description on reversal moves.
"""

from odoo.tests import tagged

from .common import MuchQwebAccountTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "account_move_reversal",
    "post_install",
    "-at_install",
)
class TestAccountMoveReversal(MuchQwebAccountTestCommon):
    """
    Test cases for account.move.reversal wizard customization.

    Tests the credit note description assignment during reversal,
    including _prepare_default_reversal method and full workflow.
    """

    def test_prepare_default_reversal_description_handling(self):
        """Test _prepare_default_reversal handles description correctly."""
        self.company.write(
            {
                "description_credit_note": "<p>Credit Note Description</p>",
            }
        )

        invoice = self.create_invoice_with_lines(move_type="out_invoice")
        invoice.action_post()

        reversal_wizard = self.env["account.move.reversal"].create(
            {
                "move_ids": [(6, 0, [invoice.id])],
                "reason": "Test Reversal",
                "journal_id": self.sale_journal.id,
            }
        )

        defaults = reversal_wizard._prepare_default_reversal(invoice)

        self.assertEqual(
            defaults.get("report_header_text"), "<p>Credit Note Description</p>"
        )
        self.assertIsInstance(defaults, dict)

        self.company.write(
            {
                "description_credit_note": False,
            }
        )

        invoice2 = self.create_invoice_with_lines(move_type="out_invoice")
        invoice2.action_post()

        reversal_wizard2 = self.env["account.move.reversal"].create(
            {
                "move_ids": [(6, 0, [invoice2.id])],
                "reason": "Test Reversal",
                "journal_id": self.sale_journal.id,
            }
        )

        defaults2 = reversal_wizard2._prepare_default_reversal(invoice2)

        self.assertNotIn("report_header_text", defaults2)

    def test_full_reversal_workflow_and_multiple_invoices(self):
        """Test full reversal workflow and multiple invoice handling."""
        self.company.write(
            {
                "description_credit_note": "<p>Standard Credit Note Terms</p>",
            }
        )

        invoice = self.create_invoice_with_lines(move_type="out_invoice")
        invoice.action_post()

        reversal_wizard = (
            self.env["account.move.reversal"]
            .with_context(
                active_model="account.move",
                active_ids=[invoice.id],
            )
            .create(
                {
                    "reason": "Test Credit Note",
                    "journal_id": self.sale_journal.id,
                }
            )
        )

        action = reversal_wizard.reverse_moves()

        if "res_id" in action:
            credit_note = self.env["account.move"].browse(action["res_id"])
        else:
            credit_note = self.env["account.move"].search(
                [("reversed_entry_id", "=", invoice.id)], limit=1
            )

        if credit_note:
            self.assertEqual(
                credit_note.report_header_text, "<p>Standard Credit Note Terms</p>"
            )

        self.company.write(
            {
                "description_credit_note": "<p>Credit Terms</p>",
            }
        )

        invoices = []
        for i in range(3):
            inv = self.create_invoice_with_lines(move_type="out_invoice")
            inv.action_post()
            invoices.append(inv)

        bulk_reversal_wizard = (
            self.env["account.move.reversal"]
            .with_context(
                active_model="account.move",
                active_ids=[inv.id for inv in invoices],
            )
            .create(
                {
                    "reason": "Bulk Reversal",
                    "journal_id": self.sale_journal.id,
                }
            )
        )

        for inv in invoices:
            defaults = bulk_reversal_wizard._prepare_default_reversal(inv)
            self.assertEqual(defaults.get("report_header_text"), "<p>Credit Terms</p>")
