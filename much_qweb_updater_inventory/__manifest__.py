# -*- coding: utf-8 -*-
{
    "name": "Much OfD - QWeb Updater Inventory",
    "summary": """
        Automatically update and set QWeb reports (Inventory)""",
    "description": """""",
    "author": "much. GmbH",
    "website": "https://muchconsulting.de",
    "category": "Technical",
    "version": "19.0.1.1.0",
    "license": "Other proprietary",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "stock",
        "sale_stock",
        "much_qweb_updater",
        "l10n_din5008_stock",
    ],
    "data": [
        "data/inventory/report_delivery_document_din5008_much.xml",
        "views/stock_picking_view.xml",
        "views/res_company_views.xml",
        "views/res_config_setting_views.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "much_qweb_updater_inventory/static/src/scss/*",
        ],
    },
    "demo": [],
    "auto_install": True,
    "active": True,
    "application": True,
    "module_type": "official",
    "pre_init_hook": "pre_init_hook",
}
