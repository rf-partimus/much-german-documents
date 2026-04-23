# -*- coding: utf-8 -*-
"""
Tests for ir.actions.report QWeb PDF rendering extension.

This module tests the extended _render_qweb_pdf method that computes
report header text for active models before rendering.
"""

from unittest.mock import patch
from odoo.tests import tagged

from .common import MuchQwebTestCommon


@tagged(
    "much_unit", "much_qweb_updater", "ir_actions_report", "post_install", "-at_install"
)
class TestIrActionsReportRenderQwebPdf(MuchQwebTestCommon):
    """
    Test cases for _render_qweb_pdf method extension.

    Tests the computation of report header text for various
    model and record scenarios.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for report rendering tests."""
        super().setUpClass()
        cls.report = cls.env.ref(
            "base.action_report_partnerform", raise_if_not_found=False
        )
        if not cls.report:
            cls.report = cls.env["ir.actions.report"].search([], limit=1)

    def test_method_exists_and_callable(self):
        """Test that _render_qweb_pdf method exists and is callable."""
        self.assertTrue(hasattr(self.report, "_render_qweb_pdf"))
        self.assertTrue(callable(getattr(self.report, "_render_qweb_pdf", None)))
        self.assertEqual(self.report._name, "ir.actions.report")

    def test_render_calls_compute_method_when_available(self):
        """Test that _compute_report_header_text is called when method exists."""
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        with patch.object(
            type(partner), "_compute_report_header_text", create=True
        ) as mock_compute:
            mock_compute.return_value = None

            with patch(
                "odoo.addons.base.models.ir_actions_report."
                "IrActionsReport._render_qweb_pdf",
                return_value=(b"pdf_content", "pdf"),
            ):
                data = {"context": {"active_model": "res.partner"}}
                self.report._render_qweb_pdf(
                    self.report, res_ids=[partner.id], data=data
                )

            mock_compute.assert_called_once()

    def test_render_skips_compute_when_method_not_available(self):
        """Test that rendering proceeds with no _compute_report_header_text."""
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        compute_method = getattr(partner, "_compute_report_header_text", None)
        self.assertIsNone(compute_method)
        self.assertFalse(callable(compute_method))

        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ) as mock_super:
            data = {"context": {"active_model": "res.partner"}}
            result = self.report._render_qweb_pdf(
                self.report, res_ids=[partner.id], data=data
            )
            mock_super.assert_called_once()
            self.assertEqual(result, (b"pdf_content", "pdf"))

    def test_render_with_none_data_and_context_fallback(self):
        """Test None data creates default and None res_ids falls back to context."""
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ) as mock_super:
            self.report._render_qweb_pdf(self.report, res_ids=[partner.id], data=None)
            mock_super.assert_called_once()

        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ):
            report_with_context = self.report.with_context(active_ids=[partner.id])
            result = report_with_context._render_qweb_pdf(
                self.report,
                res_ids=None,
                data={"context": {"active_model": "res.partner"}},
            )
            self.assertEqual(result, (b"pdf_content", "pdf"))

    def test_render_skips_compute_without_model_or_res_ids(self):
        """Test that rendering skips header computation without model or res_ids."""
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ) as mock_super:
            self.report._render_qweb_pdf(
                self.report, res_ids=[partner.id], data={"context": {}}
            )
            self.report._render_qweb_pdf(
                self.report,
                res_ids=None,
                data={"context": {"active_model": "res.partner"}},
            )
            self.report._render_qweb_pdf(
                self.report,
                res_ids=[partner.id],
                data={"context": {"active_model": False}},
            )
            self.assertEqual(mock_super.call_count, 3)


@tagged(
    "much_unit", "much_qweb_updater", "ir_actions_report", "post_install", "-at_install"
)
class TestIrActionsReportEdgeCases(MuchQwebTestCommon):
    """
    Test cases for edge cases and boundary conditions.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for edge case tests."""
        super().setUpClass()
        cls.report = cls.env.ref(
            "base.action_report_partnerform", raise_if_not_found=False
        )
        if not cls.report:
            cls.report = cls.env["ir.actions.report"].search([], limit=1)

    def test_render_with_empty_and_multiple_res_ids(self):
        """Test rendering with empty res_ids list and multiple record IDs."""
        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ) as mock_super:
            data = {"context": {"active_model": "res.partner"}}
            self.report._render_qweb_pdf(self.report, res_ids=[], data=data)
            mock_super.assert_called_once()

        partners = self.env["res.partner"].create(
            [
                {"name": "Partner 1"},
                {"name": "Partner 2"},
                {"name": "Partner 3"},
            ]
        )

        with patch.object(
            type(partners), "_compute_report_header_text", create=True
        ) as mock_compute:
            mock_compute.return_value = None

            with patch(
                "odoo.addons.base.models.ir_actions_report."
                "IrActionsReport._render_qweb_pdf",
                return_value=(b"pdf_content", "pdf"),
            ):
                data = {"context": {"active_model": "res.partner"}}
                self.report._render_qweb_pdf(
                    self.report, res_ids=partners.ids, data=data
                )

            mock_compute.assert_called_once()

    def test_render_with_missing_or_empty_context(self):
        """Test rendering with missing context key or empty context."""
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ) as mock_super:
            self.report._render_qweb_pdf(self.report, res_ids=[partner.id], data={})
            self.report._render_qweb_pdf(
                self.report, res_ids=[partner.id], data={"context": {}}
            )
            self.assertEqual(mock_super.call_count, 2)

    def test_render_with_invalid_model_name(self):
        """Test rendering with non-existent model name raises KeyError."""
        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ):
            data = {"context": {"active_model": "non.existent.model"}}
            with self.assertRaises(KeyError):
                self.report._render_qweb_pdf(self.report, res_ids=[1], data=data)

    def test_render_preserves_original_data(self):
        """Test that original data dict is not modified unexpectedly."""
        partner = self.env["res.partner"].create({"name": "Test Partner"})
        original_data = {
            "context": {"active_model": "res.partner", "custom_key": "value"}
        }

        with patch(
            "odoo.addons.base.models.ir_actions_report."
            "IrActionsReport._render_qweb_pdf",
            return_value=(b"pdf_content", "pdf"),
        ):
            self.report._render_qweb_pdf(
                self.report, res_ids=[partner.id], data=original_data
            )
            self.assertEqual(original_data["context"]["custom_key"], "value")

    def test_render_handles_non_callable_attribute(self):
        """Test rendering when _compute_report_header_text exists but uncallable."""
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        with patch.object(
            type(partner), "_compute_report_header_text", "not_a_method", create=True
        ):
            with patch(
                "odoo.addons.base.models.ir_actions_report."
                "IrActionsReport._render_qweb_pdf",
                return_value=(b"pdf_content", "pdf"),
            ) as mock_super:
                data = {"context": {"active_model": "res.partner"}}
                self.report._render_qweb_pdf(
                    self.report, res_ids=[partner.id], data=data
                )
                mock_super.assert_called_once()


@tagged(
    "much_unit", "much_qweb_updater", "ir_actions_report", "post_install", "-at_install"
)
class TestIrActionsReportWithDependentModels(MuchQwebTestCommon):
    """
    Test cases for _render_qweb_pdf with dependent models.

    These tests verify integration with models that have
    _compute_report_header_text method when modules are installed.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for dependent model tests."""
        super().setUpClass()
        cls.report = cls.env.ref(
            "base.action_report_partnerform", raise_if_not_found=False
        )
        if not cls.report:
            cls.report = cls.env["ir.actions.report"].search([], limit=1)

    def test_render_with_account_move_model(self):
        """Test rendering with account.move if available."""
        if not self.has_model("account.move"):
            self.skipTest("account.move model not available")

        move = self.env["account.move"].create({"move_type": "out_invoice"})

        with patch.object(
            type(move), "_compute_report_header_text", create=True
        ) as mock_compute:
            mock_compute.return_value = None

            with patch(
                "odoo.addons.base.models.ir_actions_report."
                "IrActionsReport._render_qweb_pdf",
                return_value=(b"pdf_content", "pdf"),
            ):
                data = {"context": {"active_model": "account.move"}}
                self.report._render_qweb_pdf(self.report, res_ids=[move.id], data=data)

            mock_compute.assert_called_once()

    def test_render_with_sale_order_model(self):
        """Test rendering with sale.order if available."""
        if not self.has_model("sale.order"):
            self.skipTest("sale.order model not available")

        partner = self.env["res.partner"].create({"name": "Test Customer"})
        order = self.env["sale.order"].create({"partner_id": partner.id})

        with patch.object(
            type(order), "_compute_report_header_text", create=True
        ) as mock_compute:
            mock_compute.return_value = None

            with patch(
                "odoo.addons.base.models.ir_actions_report."
                "IrActionsReport._render_qweb_pdf",
                return_value=(b"pdf_content", "pdf"),
            ):
                data = {"context": {"active_model": "sale.order"}}
                self.report._render_qweb_pdf(self.report, res_ids=[order.id], data=data)

            mock_compute.assert_called_once()
