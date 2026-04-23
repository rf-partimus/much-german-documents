# -*- coding: utf-8 -*-
"""
Common test utilities and base classes for much_qweb_updater tests.

This module provides:
- MuchQwebTestCommon: Base class with common setup for all tests
- Helper methods for creating test data
- Constants used across tests
"""

from odoo.tests import TransactionCase


class MuchQwebTestCommon(TransactionCase):
    """
    Base test class providing common setup and utilities for all tests.

    This class provides:
    - Company setup with required configuration
    - User setup with appropriate permissions
    - Partner setup for testing references
    - Helper methods for common test operations

    All test classes in the much_qweb_updater modules should inherit from this class
    to ensure consistent test setup and behavior.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures used by all test methods.

        Creates:
        - Test company with default configuration
        - Test user with appropriate access rights
        - Test partners for reference testing
        """
        super().setUpClass()
        cls.env["res.lang"]._activate_lang("de_DE")
        cls._setup_company()
        cls._setup_user()
        cls._setup_partners()

    @classmethod
    def _setup_company(cls):
        """
        Set up the test company with default configuration.

        Configures logo settings, footer columns, and other base fields
        required for QWeb report generation.
        """
        cls.company = cls.env.company
        cls.company.write(
            {
                "free_text_footer": True,
                "footer_font_size": 10,
                "logo_width_unit": "px",
                "logo_width": 100,
                "logo_height_unit": "px",
                "logo_height": 50,
                "print_company": True,
                "adjust_logo": False,
                "column_1": "<p>Column 1 Content</p>",
                "column_2": "<p>Column 2 Content</p>",
                "column_3": "<p>Column 3 Content</p>",
                "column_4": "<p>Column 4 Content</p>",
            }
        )

    @classmethod
    def _setup_user(cls):
        """
        Set up the test user with required permissions.

        Creates a user with access to the base module functionality.
        """
        cls.test_user = cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_user@example.com",
                "email": "test_user@example.com",
                "company_id": cls.company.id,
                "company_ids": [(6, 0, [cls.company.id])],
            }
        )

    @classmethod
    def _setup_partners(cls):
        """
        Set up test partners for reference field testing.

        Creates partners with vendor_ref and customer_ref fields set
        for testing reference propagation in documents.
        """
        cls.partner_customer = cls.env["res.partner"].create(
            {
                "name": "Test Customer",
                "email": "customer@example.com",
                "vendor_ref": "VENDOR-001",
                "customer_ref": "CUSTOMER-001",
                "company_type": "company",
            }
        )

        cls.partner_vendor = cls.env["res.partner"].create(
            {
                "name": "Test Vendor",
                "email": "vendor@example.com",
                "vendor_ref": "VENDOR-002",
                "customer_ref": "CUSTOMER-002",
                "company_type": "company",
            }
        )

        cls.partner_contact = cls.env["res.partner"].create(
            {
                "name": "Test Contact",
                "email": "contact@example.com",
                "parent_id": cls.partner_customer.id,
                "company_type": "person",
            }
        )

    def create_company_with_config(self, **kwargs):
        """
        Create a company with custom configuration.

        Args:
            **kwargs: Company field values to set.

        Returns:
            res.company: The created company record.
        """
        default_vals = {
            "name": "Test Company",
            "free_text_footer": True,
            "footer_font_size": 10,
            "print_company": True,
        }
        default_vals.update(kwargs)
        return self.env["res.company"].create(default_vals)

    def create_partner_with_refs(
        self, name, vendor_ref=None, customer_ref=None, **kwargs
    ):
        """
        Create a partner with reference fields.

        Args:
            name: Partner name.
            vendor_ref: Our vendor reference at customer.
            customer_ref: Our customer reference at vendor.
            **kwargs: Additional partner field values.

        Returns:
            res.partner: The created partner record.
        """
        vals = {
            "name": name,
            "vendor_ref": vendor_ref,
            "customer_ref": customer_ref,
        }
        vals.update(kwargs)
        return self.env["res.partner"].create(vals)

    def get_dynamic_field_value(self, obj, html_content, check=False):
        """
        Evaluate dynamic field content using the user helper.

        Args:
            obj: The object context for evaluation.
            html_content: HTML content with ${...} patterns.
            check: If True, only validate without returning value.

        Returns:
            str or bool: Evaluated content or validation result.
        """
        return self.env.user.get_evaluated_val(obj, html_content, check=check)

    def assert_field_in_data(self, data, field_key, expected_value=None):
        """
        Assert that a field exists in template data with optional value check.

        Args:
            data: List of tuples from get_l10n_din5008_template_data.
            field_key: The key to search for (third element of tuple).
            expected_value: Optional expected value (second element of tuple).

        Raises:
            AssertionError: If field not found or value doesn't match.
        """
        field_data = [item for item in data if item[2] == field_key]
        self.assertTrue(
            len(field_data) > 0,
            f"Field '{field_key}' not found in template data: {data}",
        )
        if expected_value is not None:
            self.assertEqual(
                field_data[0][1], expected_value, f"Field '{field_key}' value mismatch"
            )

    def assert_field_not_in_data(self, data, field_key):
        """
        Assert that a field does not exist in template data.

        Args:
            data: List of tuples from get_l10n_din5008_template_data.
            field_key: The key to search for (third element of tuple).

        Raises:
            AssertionError: If field is found.
        """
        field_data = [item for item in data if item[2] == field_key]
        self.assertFalse(
            len(field_data) > 0,
            f"Field '{field_key}' should not be in template data: {data}",
        )

    def has_model(self, model_name):
        """
        Check if a model is available in the registry.

        Args:
            model_name: Technical name of the model (e.g., 'account.move').

        Returns:
            bool: True if the model exists, False otherwise.
        """
        return model_name in self.env.registry

    def has_field(self, model_name, field_name):
        """
        Check if a field exists on a model.

        Args:
            model_name: Technical name of the model.
            field_name: Name of the field to check.

        Returns:
            bool: True if field exists, False otherwise.
        """
        if not self.has_model(model_name):
            return False
        return field_name in self.env[model_name]._fields
