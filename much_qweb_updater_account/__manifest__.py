# -*- coding: utf-8 -*-
{
    "name": "Much OfD - QWeb Updater Accounting",
    "summary": """
        Automatically update and set QWeb reports (Accounting)""",
    "description": """""",
    "author": "much. GmbH",
    "website": "https://muchconsulting.de",
    "category": "Technical",
    "version": "19.0.1.1.1",
    "license": "Other proprietary",
    # any module necessary for this one to work correctly
    "depends": ["base", "account", "much_qweb_updater", "sale"],
    "data": [
        "data/account/report_invoice_document_din5008_much.xml",
        "views/account_move_views.xml",
        "views/res_company_views.xml",
        "views/res_config_setting_views.xml",
        "views/sale_order_views.xml",
    ],
    "demo": [],
    "auto_install": True,
    "active": True,
    "application": True,
    "module_type": "official",
    "pre_init_hook": "pre_init_hook",
}
