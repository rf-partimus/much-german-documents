# -*- coding: utf-8 -*-
{
    "name": "Much OfD - QWeb Updater Accounting & Inventory",
    "summary": """
        Automatically update and set QWeb reports (Accounting and Inventory)""",
    "description": """""",
    "author": "much. GmbH",
    "website": "https://muchconsulting.de",
    "category": "Technical",
    "version": "19.0.1.1.0",
    "license": "Other proprietary",
    # any module necessary for this one to work correctly
    "depends": ["much_qweb_updater_account", "stock_delivery"],
    "data": ["data/account/report_invoice_document_din5008_inventory_much.xml"],
    "auto_install": True,
    "active": True,
    "application": True,
    "module_type": "official",
    "pre_init_hook": "pre_init_hook",
}
