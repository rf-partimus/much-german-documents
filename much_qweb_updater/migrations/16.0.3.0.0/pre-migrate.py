# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """
    Auto Install OfD apps if all dependencies are installed
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    ir_model_data = env["ir.model.data"]
    all_data = ir_model_data.search([("module", "=", "much_qweb_updater")])

    # move to much_qweb_updater_account
    # 19 fields
    # 1 form view
    # 4 report templates
    account_data = all_data.filtered(
        lambda data: data.name
        in (
            "field_account_bank_statement_line__delivery_date_error_message",
            "field_account_bank_statement_line__delivery_end_date",
            "field_account_bank_statement_line__delivery_start_date",
            "field_account_bank_statement_line__order_title",
            "field_account_bank_statement_line__report_header_text",
            "field_account_move__delivery_date_error_message",
            "field_account_move__delivery_end_date",
            "field_account_move__delivery_start_date",
            "field_account_move__order_title",
            "field_account_move__report_header_text",
            "field_account_move_line__delivery_end_date",
            "field_account_move_line__delivery_start_date",
            "field_account_payment__delivery_date_error_message",
            "field_account_payment__delivery_end_date",
            "field_account_payment__delivery_start_date",
            "field_account_payment__order_title",
            "field_account_payment__report_header_text",
            "field_sale_order__delivery_end_date",
            "field_sale_order__delivery_start_date",
            "report_invoice_document_din5008_much",
            "report_invoice_document_with_payments_din5008_much",
            "report_invoice_much_custom_din5008",
            "report_invoice_with_payments_much_custom_din5008",
            "view_move_form_much_din5008",
        )
    )
    account_data.write({"module": "much_qweb_updater_account"})
    # deactivate view where order_title is used
    s = env.ref("much_qweb_updater.delivery_date_order_form")
    s.write({"active": False})

    # move to much_qweb_updater_crm
    # 1 field
    # 1 form view
    # 1 report template will be created
    crm_data = all_data.filtered(
        lambda data: data.name
        in ("crm_team_form_updater_custom", "field_crm_team__report_text")
    )
    crm_data.write({"module": "much_qweb_updater_crm"})

    # move to much_qweb_updater_inventory
    # 2 fields
    # 1 form view
    # 4 report templates
    inventory_data = all_data.filtered(
        lambda data: data.name
        in (
            "field_stock_picking__order_title",
            "field_stock_picking__report_header_text",
            "report_delivery_document_din5008_much",
            "report_deliveryslip_much_custom_din5008",
            "stock_report_delivery_aggregated_move_lines_custom",
            "stock_report_delivery_has_serial_move_line_custom",
            "view_stock_picking_much_updater",
        )
    )
    inventory_data.write({"module": "much_qweb_updater_inventory"})

    # move to much_qweb_updater_purchase
    # 2 fields
    # 1 form view
    # 4 report templates
    purchase_data = all_data.filtered(
        lambda data: data.name
        in (
            "field_purchase_order__order_title",
            "field_purchase_order__report_header_text",
            "report_purchaseorder_document_din5008_much",
            "report_purchaseorder_much_custom_din5008",
            "report_purchasequotation_document_din5008_much",
            "report_purchasequotation_much_custom_din5008",
            "view_purchase_order_form_much_din5008",
        )
    )
    purchase_data.write({"module": "much_qweb_updater_purchase"})

    # move to much_qweb_updater_sale
    # 4 fields
    # 2 form views
    # 3 report templates
    # 1 portal template
    sale_data = all_data.filtered(
        lambda data: data.name
        in (
            "field_sale_order__order_title",
            "field_sale_order__report_header_text",
            "field_sale_order_template__order_title",
            "field_sale_order_template__report_header_text",
            "report_saleorder_document_din5008_much",
            "report_saleorder_much_custom_din5008",
            "report_saleorder_pro_forma_much_custom_din5008",
            "sale_order_portal_content_inherit_updater",
            "sale_order_template_view_form_much_din5008",
        )
    )
    sale_data.write({"module": "much_qweb_updater_sale"})
