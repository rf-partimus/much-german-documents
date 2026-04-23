# -*- coding: utf-8 -*-
{
    "name": "Much OfD - QWeb Updater Delivery & Inventory",
    "summary": """
        Automatically update and set QWeb reports (Delivery and Inventory)""",
    "description": """""",
    "author": "much. GmbH",
    "website": "https://muchconsulting.de",
    "category": "Technical",
    "version": "19.0.1.1.0",
    "license": "Other proprietary",
    # any module necessary for this one to work correctly
    "depends": ["much_qweb_updater_inventory", "stock_delivery"],
    "data": [
        "data/delivery_inventory/report_delivery_document_din5008_inventory_much.xml",
        "data/delivery_inventory/report_invoice_document_din5008_inventory_much.xml",
    ],
    "auto_install": True,
    "active": True,
    "application": True,
    "module_type": "official",
    "pre_init_hook": "pre_init_hook",
}
