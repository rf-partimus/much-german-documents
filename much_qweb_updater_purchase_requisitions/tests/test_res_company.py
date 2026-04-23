# -*- coding: utf-8 -*-
"""
Tests for res.company purchase requisition-specific configuration fields.

This module tests the company fields added for blanket order
customization, including print settings and description fields.
"""

from odoo.tests import tagged

from .common import MuchQwebPurchaseRequisitionTestCommon


@tagged(
    "much_unit",
    "much_qweb_updater_purchase_requisitions",
    "res_company",
    "post_install",
    "-at_install",
)
class TestResCompanyRequisitionPrintSettings(MuchQwebPurchaseRequisitionTestCommon):
    """
    Test cases for requisition print configuration fields.

    Tests boolean flags controlling what information appears on requisition documents.
    """

    def test_requisition_print_buyer_info_field(self):
        """Test requisition_print_buyer_info field can be set and read."""
        self.company.write({"requisition_print_buyer_info": True})
        self.assertTrue(self.company.requisition_print_buyer_info)

        self.company.write({"requisition_print_buyer_info": False})
        self.assertFalse(self.company.requisition_print_buyer_info)

    def test_print_existing_rfqs_field(self):
        """Test print_existing_rfqs field."""
        self.company.write({"print_existing_rfqs": True})
        self.assertTrue(self.company.print_existing_rfqs)

        self.company.write({"print_existing_rfqs": False})
        self.assertFalse(self.company.print_existing_rfqs)


@tagged(
    "much_unit",
    "much_qweb_updater_purchase_requisitions",
    "res_company",
    "post_install",
    "-at_install",
)
class TestResCompanyRequisitionDescriptionFields(MuchQwebPurchaseRequisitionTestCommon):
    """
    Test cases for requisition description HTML field.

    Tests the translatable description field for blanket orders.
    """

    def test_description_requisition_field(self):
        """Test description_requisition HTML field."""
        html_content = "<p>Blanket Order Description</p>"
        self.company.write({"description_requisition": html_content})
        self.assertEqual(self.company.description_requisition, html_content)

    def test_description_requisition_translation(self):
        """Test description_requisition field supports translation."""
        self.company.write({"description_requisition": "<p>English Requisition</p>"})
        self.company.with_context(lang="de_DE").write(
            {"description_requisition": "<p>Deutsche Rahmenvereinbarung</p>"}
        )

        german_desc = self.company.with_context(lang="de_DE").description_requisition

        self.assertIn("Rahmenvereinbarung", german_desc)

    def test_description_requisition_can_be_empty(self):
        """Test description_requisition can be cleared."""
        self.company.write({"description_requisition": False})
        self.assertFalse(self.company.description_requisition)


@tagged(
    "much_unit",
    "much_qweb_updater_purchase_requisitions",
    "res_company",
    "post_install",
    "-at_install",
)
class TestResCompanyRequisitionFieldPersistence(MuchQwebPurchaseRequisitionTestCommon):
    """
    Test cases for field value persistence.
    """

    def test_all_requisition_fields_persist(self):
        """Test all requisition fields persist correctly."""
        config = {
            "requisition_print_buyer_info": True,
            "print_existing_rfqs": True,
            "description_requisition": "<p>Requisition</p>",
        }

        self.company.write(config)
        self.company.invalidate_recordset()

        self.assertTrue(self.company.requisition_print_buyer_info)
        self.assertTrue(self.company.print_existing_rfqs)
        self.assertEqual(self.company.description_requisition, "<p>Requisition</p>")
