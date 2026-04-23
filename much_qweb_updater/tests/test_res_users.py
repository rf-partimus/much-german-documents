# -*- coding: utf-8 -*-
"""
Tests for res.users dynamic field evaluation functionality.

This module tests the get_evaluated_val method which evaluates
dynamic ${...} patterns in HTML fields.
"""

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import MuchQwebTestCommon


@tagged("much_unit", "much_qweb_updater", "res_users", "post_install", "-at_install")
class TestResUsersDynamicEvaluation(MuchQwebTestCommon):
    """
    Test cases for the get_evaluated_val method on res.users.

    This method evaluates ${...} patterns in HTML content using safe_eval,
    allowing dynamic field references in report templates.
    """

    def test_evaluate_field_references(self):
        """Test evaluating simple, multiple, nested, and repeated field references."""
        test_cases = [
            ("<p>Partner: ${object.name}</p>", "<p>Partner: Test Customer</p>"),
            (
                "<p>Name: ${object.name}, Email: ${object.email}</p>",
                "<p>Name: Test Customer, Email: customer@example.com</p>",
            ),
            (
                "<p>${object.name} - ${object.name}</p>",
                "<p>Test Customer - Test Customer</p>",
            ),
            ("${object.name}", "Test Customer"),
            ("${object.name}${object.email}", "Test Customercustomer@example.com"),
            ("${object.name} is the partner", "Test Customer is the partner"),
            ("The partner is ${object.name}", "The partner is Test Customer"),
            (
                "<p>${object.name}</p><p>${object.name}</p><p>${object.name}</p>",
                "<p>Test Customer</p><p>Test Customer</p><p>Test Customer</p>",
            ),
        ]
        for html_content, expected in test_cases:
            result = self.get_dynamic_field_value(self.partner_customer, html_content)
            self.assertEqual(result, expected)

        result = self.get_dynamic_field_value(
            self.partner_contact, "<p>Parent: ${object.parent_id.name}</p>"
        )
        self.assertEqual(result, "<p>Parent: Test Customer</p>")

    def test_evaluate_various_field_types(self):
        """Test evaluating boolean, numeric, False, and custom fields."""
        result = self.get_dynamic_field_value(
            self.partner_customer, "<p>Is Company: ${object.is_company}</p>"
        )
        self.assertIn("Is Company:", result)

        result = self.get_dynamic_field_value(
            self.partner_customer, "<p>ID: ${object.id}</p>"
        )
        self.assertIn(str(self.partner_customer.id), result)

        partner_no_email = self.env["res.partner"].create({"name": "No Email Partner"})
        result = self.get_dynamic_field_value(
            partner_no_email, "<p>Email: ${object.email}</p>"
        )
        self.assertEqual(result, "<p>Email: False</p>")

        result = self.get_dynamic_field_value(
            self.partner_customer, "<p>Vendor Ref: ${object.vendor_ref}</p>"
        )
        self.assertEqual(result, "<p>Vendor Ref: VENDOR-001</p>")

        self.company.write({"logo_width": 0})
        result = self.get_dynamic_field_value(
            self.company, "<p>Width: ${object.logo_width}</p>"
        )
        self.assertEqual(result, "<p>Width: 0</p>")

        partner = self.env["res.partner"].create(
            {"name": "Empty Ref", "vendor_ref": ""}
        )
        result = self.get_dynamic_field_value(
            partner, "<p>Ref: ${object.vendor_ref}</p>"
        )
        self.assertEqual(result, "<p>Ref: </p>")

    def test_evaluate_empty_and_static_content(self):
        """Test empty, None, and static content without patterns."""
        self.assertEqual(self.get_dynamic_field_value(self.partner_customer, ""), "")
        self.assertEqual(self.get_dynamic_field_value(self.partner_customer, None), "")

        static = "<p>Static content without patterns</p>"
        self.assertEqual(
            self.get_dynamic_field_value(self.partner_customer, static), static
        )

    def test_evaluate_multiline_and_mixed_content(self):
        """Test multiline HTML and mixed dynamic/static content."""
        html_content = """
        <div>
            <p>Name: ${object.name}</p>
            <p>Email: ${object.email}</p>
        </div>
        """
        result = self.get_dynamic_field_value(self.partner_customer, html_content)
        self.assertIn("Test Customer", result)
        self.assertIn("customer@example.com", result)

        mixed = (
            "<div class='test'><span>${object.name}</span><br/>"
            "<em>Static</em><strong>${object.email}</strong></div>"
        )
        result = self.get_dynamic_field_value(self.partner_customer, mixed)
        self.assertIn("Test Customer", result)
        self.assertIn("customer@example.com", result)
        self.assertIn("Static", result)
        self.assertIn("<div class='test'>", result)

    def test_evaluate_special_characters_and_whitespace(self):
        """Test fields with special characters and patterns with whitespace."""
        partner = self.env["res.partner"].create({"name": "Test & Company <Ltd>"})
        result = self.get_dynamic_field_value(partner, "<p>${object.name}</p>")
        self.assertIn("Test & Company <Ltd>", result)

        result = self.get_dynamic_field_value(
            self.partner_customer, "<p>${ object.name }</p>"
        )
        self.assertEqual(result, "<p>Test Customer</p>")

    def test_evaluate_with_different_objects(self):
        """Test evaluating fields on company and user objects."""
        result = self.get_dynamic_field_value(
            self.company, "<p>Company: ${object.name}</p>"
        )
        self.assertIn("Company:", result)

        result = self.get_dynamic_field_value(
            self.test_user, "<p>User: ${object.name}, Login: ${object.login}</p>"
        )
        self.assertIn("Test User", result)
        self.assertIn("test_user@example.com", result)

    def test_check_mode(self):
        """Test check mode for valid and invalid field references."""
        self.assertTrue(
            self.get_dynamic_field_value(
                self.partner_customer, "<p>${object.name}</p>", check=True
            )
        )
        self.assertTrue(
            self.get_dynamic_field_value(
                self.partner_customer, "<p>Static content</p>", check=True
            )
        )
        self.assertTrue(
            self.get_dynamic_field_value(self.partner_customer, "", check=True)
        )
        self.assertTrue(
            self.get_dynamic_field_value(self.partner_customer, None, check=True)
        )

        with self.assertRaises(ValidationError) as context:
            self.get_dynamic_field_value(
                self.partner_customer, "<p>${object.nonexistent_field}</p>", check=True
            )
        self.assertIn("field doesn't exist", str(context.exception).lower())


@tagged("much_unit", "much_qweb_updater", "res_users", "post_install", "-at_install")
class TestResUsersDynamicEvaluationEdgeCases(MuchQwebTestCommon):
    """
    Test cases for edge cases and error handling in get_evaluated_val method.
    """

    def test_malformed_and_partial_patterns(self):
        """Test handling of malformed, unclosed, and partial patterns."""
        test_cases = [
            ("<p>${object.name", "<p>${object.name"),
            ("${object\n.name}", "${object\n.name}"),
            ("<p>${object.name} and {other}</p>", "<p>Test Customer and {other}</p>"),
            ("<p>$100 and ${object.name}</p>", "<p>$100 and Test Customer</p>"),
            ("<p>${object.name} {nested}</p>", "<p>Test Customer {nested}</p>"),
        ]
        for html_content, expected in test_cases:
            result = self.get_dynamic_field_value(self.partner_customer, html_content)
            self.assertEqual(result, expected)

    def test_relational_field_edge_cases(self):
        """Test relational fields that are empty or deeply nested."""
        partner_no_parent = self.env["res.partner"].create(
            {"name": "No Parent Partner"}
        )
        result = self.get_dynamic_field_value(
            partner_no_parent, "<p>Parent: ${object.parent_id.name}</p>"
        )
        self.assertEqual(result, "<p>Parent: False</p>")

        result = self.get_dynamic_field_value(
            self.partner_contact, "<p>${object.parent_id.company_id.name}</p>"
        )
        self.assertIsInstance(result, str)

    def test_invalid_field_references(self):
        """Test invalid field ref raise ValidationError with informative messages."""
        with self.assertRaises(ValidationError):
            self.get_dynamic_field_value(
                self.partner_customer, "<p>${object.invalid_field_name}</p>"
            )

        with self.assertRaises(ValidationError) as context:
            self.get_dynamic_field_value(
                self.partner_customer, "<p>${object.totally_fake_field}</p>"
            )
        self.assertIn("field doesn't exist", str(context.exception).lower())


@tagged("much_unit", "much_qweb_updater", "res_users", "post_install", "-at_install")
class TestResUsersDynamicEvaluationSecurity(MuchQwebTestCommon):
    """
    Test cases for security aspects of get_evaluated_val method.

    Ensures safe_eval prevents dangerous operations.
    """

    def test_safe_eval_blocks_dangerous_operations(self):
        """Test that dangerous operations are blocked by safe_eval."""
        dangerous_patterns = [
            "<p>${__import__('os').system('ls')}</p>",
            "<p>${exec('print(1)')}</p>",
            "<p>${eval('1+1')}</p>",
            "<p>${open('/etc/passwd').read()}</p>",
            "<p>${env['res.partner'].search([])}</p>",
            "<p>${self.env}</p>",
        ]
        for html_content in dangerous_patterns:
            with self.assertRaises(ValidationError):
                self.get_dynamic_field_value(self.partner_customer, html_content)
