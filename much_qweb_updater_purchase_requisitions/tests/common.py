# -*- coding: utf-8 -*-
"""
Common test utilities and base classes for module tests.

This module provides:
- MuchQwebPurchaseRequisitionTestCommon: Base class with requisition-specific setup
- Helper methods for creating test purchase requisitions
"""

from datetime import date, timedelta
from odoo.addons.much_qweb_updater.tests.common import MuchQwebTestCommon


class MuchQwebPurchaseRequisitionTestCommon(MuchQwebTestCommon):
    """
    Base test class providing common setup for purchase requisition module tests.

    This class extends MuchQwebTestCommon with:
    - Purchase requisition creation helpers
    - Product setup for requisition testing
    - Company requisition configuration

    All test classes in the much_qweb_updater_purchase_requisitions module
    should inherit from this class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures for purchase requisition tests.

        Creates:
        - Test products
        - Company requisition configuration
        """
        super().setUpClass()
        cls._setup_products()
        cls._setup_requisition_company_config()

    @classmethod
    def _setup_products(cls):
        """
        Set up test products for purchase requisitions.
        """
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Requisition Product",
                "type": "consu",
                "standard_price": 75.0,
            }
        )

    @classmethod
    def _setup_requisition_company_config(cls):
        """
        Set up company configuration for requisition features.

        Configures blanket order descriptions and print settings.
        """
        cls.company.write(
            {
                "requisition_print_buyer_info": True,
                "print_existing_rfqs": True,
                "description_requisition": "<p>Default Requisition Description</p>",
            }
        )

    def create_purchase_requisition(self, vendor=None, **kwargs):
        """
        Create a test purchase requisition.

        Args:
            vendor: Vendor partner for the requisition.
            **kwargs: Additional requisition field values.

        Returns:
            purchase.requisition: The created requisition record.
        """
        vendor = vendor or self.partner_vendor
        vals = {
            "vendor_id": vendor.id,
            "company_id": self.company.id,
            "date_start": date.today(),
            "date_end": date.today() + timedelta(days=30),
        }
        vals.update(kwargs)
        return self.env["purchase.requisition"].create(vals)

    def create_requisition_with_lines(self, vendor=None, line_count=1, **kwargs):
        """
        Create a test purchase requisition with lines.

        Args:
            vendor: Vendor partner for the requisition.
            line_count: Number of lines to create.
            **kwargs: Additional requisition field values.

        Returns:
            purchase.requisition: The created requisition with lines.
        """
        vendor = vendor or self.partner_vendor
        lines = []
        for i in range(line_count):
            lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": self.product.id,
                        "product_qty": 100,
                        "price_unit": 75.0,
                    },
                )
            )

        vals = {
            "vendor_id": vendor.id,
            "company_id": self.company.id,
            "date_start": date.today(),
            "date_end": date.today() + timedelta(days=30),
            "line_ids": lines,
        }
        vals.update(kwargs)
        return self.env["purchase.requisition"].create(vals)
