# -*- coding: utf-8 -*-
"""
Common test utilities and base classes for much_qweb_updater_account tests.

This module provides:
- MuchQwebAccountTestCommon: Base class with accounting-specific setup
- Helper methods for creating test invoices, moves, and related data
"""

from datetime import date, timedelta
from odoo.addons.much_qweb_updater.tests.common import MuchQwebTestCommon


class MuchQwebAccountTestCommon(MuchQwebTestCommon):
    """
    Base test class providing common setup for accounting module tests.

    This class extends MuchQwebTestCommon with:
    - Account and journal setup
    - Invoice/move creation helpers
    - Delivery date testing utilities
    - Company accounting configuration

    All test classes in the much_qweb_updater_account module should inherit
    from this class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures for accounting tests.

        Creates:
        - Test accounts for receivable/payable
        - Test journals
        - Company accounting configuration
        - Sample invoices for testing
        """
        super().setUpClass()
        cls._setup_accounts()
        cls._setup_journals()
        cls._setup_account_company_config()
        cls._setup_products()

    @classmethod
    def _setup_accounts(cls):
        """
        Set up test accounts for invoice creation.

        Creates receivable, payable, and income accounts needed
        for invoice line creation.
        """
        cls.account_receivable = cls.env["account.account"].search(
            [
                ("account_type", "=", "asset_receivable"),
                ("company_ids", "in", cls.company.id),
            ],
            limit=1,
        )

        if not cls.account_receivable:
            cls.account_receivable = cls.env["account.account"].create(
                {
                    "name": "Test Receivable",
                    "code": "120000",
                    "account_type": "asset_receivable",
                    "reconcile": True,
                    "company_ids": [(4, cls.company.id)],
                }
            )

        cls.account_payable = cls.env["account.account"].search(
            [
                ("account_type", "=", "liability_payable"),
                ("company_ids", "in", cls.company.id),
            ],
            limit=1,
        )

        if not cls.account_payable:
            cls.account_payable = cls.env["account.account"].create(
                {
                    "name": "Test Payable",
                    "code": "210000",
                    "account_type": "liability_payable",
                    "reconcile": True,
                    "company_ids": [(4, cls.company.id)],
                }
            )

        cls.account_income = cls.env["account.account"].search(
            [
                ("account_type", "=", "income"),
                ("company_ids", "in", cls.company.id),
            ],
            limit=1,
        )

        if not cls.account_income:
            cls.account_income = cls.env["account.account"].create(
                {
                    "name": "Test Income",
                    "code": "400000",
                    "account_type": "income",
                    "company_ids": [(4, cls.company.id)],
                }
            )

    @classmethod
    def _setup_journals(cls):
        """
        Set up test journals for invoice creation.
        """
        cls.sale_journal = cls.env["account.journal"].search(
            [
                ("type", "=", "sale"),
                ("company_id", "=", cls.company.id),
            ],
            limit=1,
        )

        if not cls.sale_journal:
            cls.sale_journal = cls.env["account.journal"].create(
                {
                    "name": "Test Sales Journal",
                    "code": "TSLJ",
                    "type": "sale",
                    "company_id": cls.company.id,
                }
            )

        cls.purchase_journal = cls.env["account.journal"].search(
            [
                ("type", "=", "purchase"),
                ("company_id", "=", cls.company.id),
            ],
            limit=1,
        )

        if not cls.purchase_journal:
            cls.purchase_journal = cls.env["account.journal"].create(
                {
                    "name": "Test Purchase Journal",
                    "code": "TPUJ",
                    "type": "purchase",
                    "company_id": cls.company.id,
                }
            )

    @classmethod
    def _setup_account_company_config(cls):
        """
        Set up company configuration for accounting features.

        Configures invoice/credit note descriptions, print settings,
        and delivery time frame options.
        """
        cls.company.write(
            {
                "print_sale_person": True,
                "block_condition": False,
                "print_payment_ref": True,
                "print_time_frame": True,
                "print_incoterm": True,
                "ac_print_coo": True,
                "ac_print_hs_code": True,
                "description_inv": "<p>Default Invoice Description</p>",
                "description_credit_note": "<p>Default Credit Note Description</p>",
                "invoice_print_datev_identifier_customer": True,
            }
        )

    @classmethod
    def _setup_products(cls):
        """
        Set up test products for invoice lines.
        """
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "list_price": 100.0,
            }
        )

    def create_invoice(self, move_type="out_invoice", partner=None, **kwargs):
        """
        Create a test invoice/move.

        Args:
            move_type: Type of move ('out_invoice', 'out_refund', etc.).
            partner: Partner for the invoice, defaults to partner_customer.
            **kwargs: Additional move field values.

        Returns:
            account.move: The created invoice record.
        """
        partner = partner or self.partner_customer
        vals = {
            "move_type": move_type,
            "partner_id": partner.id,
            "invoice_date": date.today(),
            "company_id": self.company.id,
            "journal_id": self.sale_journal.id,
        }
        vals.update(kwargs)
        return self.env["account.move"].create(vals)

    def create_invoice_with_lines(
        self, move_type="out_invoice", partner=None, line_count=1, **kwargs
    ):
        """
        Create a test invoice with invoice lines.

        Args:
            move_type: Type of move.
            partner: Partner for the invoice.
            line_count: Number of invoice lines to create.
            **kwargs: Additional move field values.

        Returns:
            account.move: The created invoice with lines.
        """
        partner = partner or self.partner_customer
        lines = []
        for i in range(line_count):
            lines.append(
                (
                    0,
                    0,
                    {
                        "name": f"Test Line {i + 1}",
                        "quantity": 1,
                        "price_unit": 100.0,
                        "account_id": self.account_income.id,
                    },
                )
            )

        vals = {
            "move_type": move_type,
            "partner_id": partner.id,
            "invoice_date": date.today(),
            "company_id": self.company.id,
            "journal_id": self.sale_journal.id,
            "invoice_line_ids": lines,
        }
        vals.update(kwargs)
        return self.env["account.move"].create(vals)

    def create_invoice_with_delivery_dates(
        self, start_date, end_date, move_type="out_invoice", **kwargs
    ):
        """
        Create an invoice with specific delivery dates.

        Args:
            start_date: Delivery start date.
            end_date: Delivery end date.
            move_type: Type of move.
            **kwargs: Additional move field values.

        Returns:
            account.move: The created invoice.
        """
        return self.create_invoice(
            move_type=move_type,
            delivery_start_date=start_date,
            delivery_end_date=end_date,
            **kwargs,
        )

    def get_dates_months_apart(self, months=1, start_day=15):
        """
        Get a pair of dates that are exactly months apart.

        Args:
            months: Number of months between dates.
            start_day: Day of the month for start date.

        Returns:
            tuple: (start_date, end_date) that are months apart.
        """
        start_date = date.today().replace(day=start_day)
        end_month = start_date.month + months
        end_year = start_date.year
        if end_month > 12:
            end_month -= 12
            end_year += 1
        end_date = date(end_year, end_month, start_day - 1)
        return start_date, end_date

    def get_dates_not_months_apart(self):
        """
        Get a pair of dates that are NOT exactly months apart.

        Returns:
            tuple: (start_date, end_date) that are not months apart.
        """
        start_date = date.today().replace(day=15)
        end_date = start_date + timedelta(days=45)
        return start_date, end_date

    def create_sale_order(self, partner=None, **kwargs):
        """
        Create a test sale order.

        Args:
            partner: Partner for the sale order.
            **kwargs: Additional sale order field values.

        Returns:
            sale.order: The created sale order.
        """
        if not self.has_model("sale.order"):
            return None
        partner = partner or self.partner_customer
        vals = {
            "partner_id": partner.id,
            "company_id": self.company.id,
        }
        vals.update(kwargs)
        return self.env["sale.order"].create(vals)

    def create_purchase_order(self, partner=None, **kwargs):
        """
        Create a test purchase order.

        Args:
            partner: Partner for the purchase order.
            **kwargs: Additional purchase order field values.

        Returns:
            purchase.order: The created purchase order.
        """
        if not self.has_model("purchase.order"):
            return None
        partner = partner or self.partner_vendor
        vals = {
            "partner_id": partner.id,
            "company_id": self.company.id,
        }
        vals.update(kwargs)
        return self.env["purchase.order"].create(vals)

    def render_din5008_invoice_html(self, invoice, context=None):
        """Render the DIN5008 invoice report via the invoice report action."""
        report_model = self.env["ir.actions.report"]
        report_action = report_model._get_report_from_name("account.report_invoice_document")
        if not report_action:
            self.skipTest("account invoice report action not available")

        company = invoice.company_id
        din5008_layout = self.env.ref(
            "l10n_din5008.external_layout_din5008", raise_if_not_found=False
        )
        previous_layout = company.external_report_layout_id
        if previous_layout != din5008_layout:
            company.external_report_layout_id = din5008_layout

        ctx = {
            "active_model": "account.move",
            "active_ids": invoice.ids,
        }
        if context:
            ctx.update(context)
        html, _ = report_action.with_context(**ctx)._render_qweb_html(invoice.ids)

        return html.decode("utf-8")
