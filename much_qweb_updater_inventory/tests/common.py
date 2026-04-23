# -*- coding: utf-8 -*-
"""
Common test utilities and base classes for much_qweb_updater_inventory tests.

This module provides:
- MuchQwebInventoryTestCommon: Base class with inventory-specific setup
- Helper methods for creating test stock pickings and related data
"""

from odoo.addons.much_qweb_updater.tests.common import MuchQwebTestCommon


class MuchQwebInventoryTestCommon(MuchQwebTestCommon):
    """
    Base test class providing common setup for inventory module tests.

    This class extends MuchQwebTestCommon with:
    - Warehouse and location setup
    - Stock picking creation helpers
    - Product setup for delivery testing
    - Company inventory configuration

    All test classes in the much_qweb_updater_inventory module should inherit
    from this class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures for inventory tests.

        Creates:
        - Test warehouse and locations
        - Test products
        - Stock picking types
        - Company inventory configuration
        """
        super().setUpClass()
        cls._setup_warehouse()
        cls._setup_products()
        cls._setup_inventory_company_config()

    @classmethod
    def _setup_warehouse(cls):
        """
        Set up test warehouse and locations.
        """
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)], limit=1
        )

        if not cls.warehouse:
            cls.warehouse = cls.env["stock.warehouse"].create(
                {
                    "name": "Test Warehouse",
                    "code": "TWH",
                    "company_id": cls.company.id,
                }
            )

        cls.location_stock = cls.warehouse.lot_stock_id
        cls.location_customer = cls.env.ref("stock.stock_location_customers")
        cls.location_supplier = cls.env.ref("stock.stock_location_suppliers")

        cls.picking_type_out = cls.warehouse.out_type_id
        cls.picking_type_in = cls.warehouse.in_type_id
        cls.picking_type_internal = cls.warehouse.int_type_id

    @classmethod
    def _setup_products(cls):
        """
        Set up test products for delivery pickings.
        """
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Delivery Product",
                "type": "consu",
                "is_storable": True,
                "list_price": 50.0,
            }
        )

    @classmethod
    def _setup_inventory_company_config(cls):
        """
        Set up company configuration for inventory features.

        Configures delivery description and print settings.
        """
        cls.company.write(
            {
                "inventory_print_coo": True,
                "inventory_print_hs_code": True,
                "print_weight": True,
                "description_delivery": "<p>Default Delivery Description</p>",
            }
        )

    def create_picking(self, picking_type=None, partner=None, **kwargs):
        """
        Create a test stock picking.

        Args:
            picking_type: Picking type (defaults to outgoing).
            partner: Partner for the picking.
            **kwargs: Additional picking field values.

        Returns:
            stock.picking: The created picking record.
        """
        picking_type = picking_type or self.picking_type_out
        partner = partner or self.partner_customer

        vals = {
            "picking_type_id": picking_type.id,
            "partner_id": partner.id,
            "location_id": self.location_stock.id,
            "location_dest_id": self.location_customer.id,
            "company_id": self.company.id,
        }
        vals.update(kwargs)
        return self.env["stock.picking"].create(vals)

    def create_picking_with_moves(
        self, picking_type=None, partner=None, move_count=1, **kwargs
    ):
        """
        Create a test picking with stock moves.

        Args:
            picking_type: Picking type.
            partner: Partner for the picking.
            move_count: Number of stock moves to create.
            **kwargs: Additional picking field values.

        Returns:
            stock.picking: The created picking with moves.
        """
        picking = self.create_picking(picking_type, partner, **kwargs)

        for i in range(move_count):
            self.env["stock.move"].create(
                {
                    "product_id": self.product.id,
                    "product_uom_qty": 10,
                    "product_uom": self.product.uom_id.id,
                    "picking_id": picking.id,
                    "location_id": picking.location_id.id,
                    "location_dest_id": picking.location_dest_id.id,
                }
            )

        return picking

    def create_sale_order_with_picking(self, partner=None):
        """
        Create a sale order and its associated picking.

        Args:
            partner: Partner for the sale order.

        Returns:
            tuple: (sale.order, stock.picking) records.
        """
        partner = partner or self.partner_customer

        sale_order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "company_id": self.company.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 5,
                        },
                    )
                ],
            }
        )
        sale_order.action_confirm()

        picking = sale_order.picking_ids[0] if sale_order.picking_ids else None
        return sale_order, picking

    def create_incoming_picking(self, partner=None, **kwargs):
        """
        Create an incoming (receipt) picking.

        Args:
            partner: Vendor partner.
            **kwargs: Additional picking field values.

        Returns:
            stock.picking: The created incoming picking.
        """
        partner = partner or self.partner_vendor
        return self.create_picking(
            picking_type=self.picking_type_in,
            partner=partner,
            location_id=self.location_supplier.id,
            location_dest_id=self.location_stock.id,
            **kwargs,
        )

    def create_internal_picking(self, **kwargs):
        """
        Create an internal transfer picking.

        Args:
            **kwargs: Additional picking field values.

        Returns:
            stock.picking: The created internal picking.
        """
        return self.create_picking(
            picking_type=self.picking_type_internal,
            location_id=self.location_stock.id,
            location_dest_id=self.location_stock.id,
            **kwargs,
        )
