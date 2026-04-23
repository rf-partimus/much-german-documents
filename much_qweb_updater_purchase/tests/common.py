# -*- coding: utf-8 -*-
"""
Common test utilities and base classes for much_qweb_updater_purchase tests.

This module provides:
- MuchQwebPurchaseTestCommon: Base class with purchase-specific setup
- Helper methods for creating test purchase orders
"""

from datetime import date, timedelta
from odoo.addons.much_qweb_updater.tests.common import MuchQwebTestCommon


class MuchQwebPurchaseTestCommon(MuchQwebTestCommon):
    """
    Base test class providing common setup for purchase module tests.

    This class extends MuchQwebTestCommon with:
    - Purchase order creation helpers
    - Product setup for purchase testing
    - Company purchase configuration

    All test classes in the much_qweb_updater_purchase module should inherit
    from this class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures for purchase tests.

        Creates:
        - Test products
        - Company purchase configuration
        """
        super().setUpClass()
        cls._setup_products()
        cls._setup_purchase_company_config()

    @classmethod
    def _setup_products(cls):
        """
        Set up test products for purchase orders.
        """
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Purchase Product",
                "type": "consu",
                "standard_price": 50.0,
            }
        )

    @classmethod
    def _setup_purchase_company_config(cls):
        """
        Set up company configuration for purchase features.

        Configures RFQ/PO descriptions and print settings.
        """
        cls.company.write(
            {
                "print_buyer_info": True,
                "purchase_print_datev_identifier": True,
                "description_rfq": "<p>Default RFQ Description</p>",
                "description_purchase": "<p>Default Purchase Order Description</p>",
            }
        )

    def create_purchase_order(self, partner=None, state="draft", **kwargs):
        """
        Create a test purchase order.

        Args:
            partner: Vendor partner for the purchase order.
            state: Initial state of the order ('draft', 'sent', 'purchase').
            **kwargs: Additional purchase order field values.

        Returns:
            purchase.order: The created purchase order record.
        """
        partner = partner or self.partner_vendor
        vals = {
            "partner_id": partner.id,
            "company_id": self.company.id,
            "date_order": date.today(),
        }
        vals.update(kwargs)
        order = self.env["purchase.order"].create(vals)

        if state == "sent":
            order.write({"state": "sent"})
        elif state == "purchase":
            order.button_confirm()

        return order

    def create_purchase_order_with_lines(
        self, partner=None, line_count=1, state="draft", **kwargs
    ):
        """
        Create a test purchase order with order lines.

        Args:
            partner: Vendor partner for the purchase order.
            line_count: Number of order lines to create.
            state: Initial state of the order.
            **kwargs: Additional purchase order field values.

        Returns:
            purchase.order: The created purchase order with lines.
        """
        partner = partner or self.partner_vendor
        lines = []
        for i in range(line_count):
            lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": self.product.id,
                        "name": f"Test Line {i + 1}",
                        "product_qty": 10,
                        "price_unit": 50.0,
                        "product_uom_id": self.product.uom_id.id,
                        "date_planned": date.today() + timedelta(days=7),
                    },
                )
            )

        vals = {
            "partner_id": partner.id,
            "company_id": self.company.id,
            "date_order": date.today(),
            "order_line": lines,
        }
        vals.update(kwargs)
        order = self.env["purchase.order"].create(vals)

        if state == "sent":
            order.write({"state": "sent"})
        elif state == "purchase":
            order.button_confirm()

        return order

    def create_vendor_with_datev_identifier(self, identifier):
        """
        Create a vendor partner with DATEV supplier identifier.

        Args:
            identifier: DATEV identifier value.

        Returns:
            res.partner: The created vendor partner.
        """
        return self.env["res.partner"].create(
            {
                "name": "DATEV Vendor",
                "l10n_de_datev_identifier": identifier,
                "supplier_rank": 1,
            }
        )
