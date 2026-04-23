# -*- coding: utf-8 -*-
"""
Common test utilities and base classes for much_qweb_updater_sale tests.

This module provides:
- MuchQwebSaleTestCommon: Base class with sales-specific setup
- Helper methods for creating test sale orders and templates
"""

from datetime import date
from odoo.addons.much_qweb_updater.tests.common import MuchQwebTestCommon


class MuchQwebSaleTestCommon(MuchQwebTestCommon):
    """
    Base test class providing common setup for sales module tests.

    This class extends MuchQwebTestCommon with:
    - Sale order creation helpers
    - Sale order template setup
    - Product setup for sales testing
    - Company sales configuration

    All test classes in the much_qweb_updater_sale module should inherit
    from this class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures for sales tests.

        Creates:
        - Test products
        - Sale order templates
        - Company sales configuration
        """
        super().setUpClass()
        cls._setup_products()
        cls._setup_sale_company_config()
        cls._setup_sale_templates()

    @classmethod
    def _setup_products(cls):
        """
        Set up test products for sale orders.
        """
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Sale Product",
                "type": "consu",
                "list_price": 100.0,
            }
        )

    @classmethod
    def _setup_sale_company_config(cls):
        """
        Set up company configuration for sales features.

        Configures quotation/order descriptions and print settings.
        """
        cls.company.write(
            {
                "so_print_sale_person": True,
                "so_print_datev_identifier_customer": True,
                "taxes_on_line": False,
                "description_quotation": "<p>Default Quotation Description</p>",
                "description_order": "<p>Default Order Description</p>",
            }
        )

    @classmethod
    def _setup_sale_templates(cls):
        """
        Set up test sale order templates.
        """
        cls.sale_template = cls.env["sale.order.template"].create(
            {
                "name": "Test Template",
                "report_header_text": "<p>Template Header Text</p>",
                "order_title": "Template Title",
            }
        )

    def create_sale_order(self, partner=None, state="draft", **kwargs):
        """
        Create a test sale order.

        Args:
            partner: Partner for the sale order.
            state: Initial state of the order ('draft', 'sent', 'sale').
            **kwargs: Additional sale order field values.

        Returns:
            sale.order: The created sale order record.
        """
        partner = partner or self.partner_customer
        vals = {
            "partner_id": partner.id,
            "company_id": self.company.id,
            "date_order": date.today(),
        }
        vals.update(kwargs)
        order = self.env["sale.order"].create(vals)

        if state == "sent":
            order.action_quotation_sent()
        elif state == "sale":
            order.action_confirm()

        return order

    def create_sale_order_with_lines(
        self, partner=None, line_count=1, state="draft", **kwargs
    ):
        """
        Create a test sale order with order lines.

        Args:
            partner: Partner for the sale order.
            line_count: Number of order lines to create.
            state: Initial state of the order.
            **kwargs: Additional sale order field values.

        Returns:
            sale.order: The created sale order with lines.
        """
        partner = partner or self.partner_customer
        lines = []
        for i in range(line_count):
            lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": self.product.id,
                        "name": f"Test Line {i + 1}",
                        "product_uom_qty": 1,
                        "price_unit": 100.0,
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
        order = self.env["sale.order"].create(vals)

        if state == "sent":
            order.action_quotation_sent()
        elif state == "sale":
            order.action_confirm()

        return order

    def create_sale_order_from_template(self, template=None, partner=None, **kwargs):
        """
        Create a sale order using a template.

        Args:
            template: Sale order template to use.
            partner: Partner for the sale order.
            **kwargs: Additional sale order field values.

        Returns:
            sale.order: The created sale order.
        """
        template = template or self.sale_template
        partner = partner or self.partner_customer

        order = self.create_sale_order(partner=partner, **kwargs)
        order.sale_order_template_id = template.id
        order._onchange_sale_order_template_id()

        return order

    def create_partner_with_datev_identifier(self, identifier):
        """
        Create a partner with DATEV customer identifier.

        Args:
            identifier: DATEV identifier value.

        Returns:
            res.partner: The created partner.
        """
        return self.env["res.partner"].create(
            {
                "name": "DATEV Partner",
                "l10n_de_datev_identifier_customer": identifier,
            }
        )
