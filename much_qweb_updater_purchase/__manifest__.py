# -*- coding: utf-8 -*-
{
    "name": "Much OfD - QWeb Updater Purchase",
    "summary": """
        Automatically update and set QWeb reports (Purchase)""",
    "description": """""",
    "author": "much. GmbH",
    "website": "https://muchconsulting.de",
    "category": "Technical",
    "version": "19.0.1.1.0",
    "license": "Other proprietary",
    # any module necessary for this one to work correctly
    "depends": ["base", "purchase", "much_qweb_updater", "l10n_din5008_purchase"],
    "data": [
        "data/purchase/report_purchaseorder_document_din5008_much.xml",
        "data/purchase/report_purchasequotation_document_din5008_much.xml",
        "views/purchase_order_views.xml",
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
