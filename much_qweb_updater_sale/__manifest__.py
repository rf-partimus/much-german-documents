# -*- coding: utf-8 -*-
{
    "name": "Much OfD - QWeb Updater Sale",
    "summary": """
        Automatically update and set QWeb reports (Sales)""",
    "description": """""",
    "author": "much. GmbH",
    "website": "https://muchconsulting.de",
    "category": "Technical",
    "version": "19.0.1.1.6",
    "license": "Other proprietary",
    "depends": [
        "base",
        "sale_management",
        "much_qweb_updater",
        "l10n_din5008_sale",
    ],
    "data": [
        "data/report_saleorder_document_din5008_much.xml",
        "views/sale_order.xml",
        "views/sale_order_template_views.xml",
        "views/sale_portal_template.xml",
        "views/res_company_views.xml",
        "views/res_config_setting_views.xml",
    ],
    "demo": [],
    "auto_install": True,
    "active": True,
    "application": True,
    "module_type": "official",
    "pre_init_hook": "pre_init_hook",
}
