# -*- coding: utf-8 -*-

{
    "name": "Much OfD - QWeb Updater Purchase Requisitions",
    "summary": """
        Automatically update and set QWeb reports (Purchase Agreement / Blanket Order)
    """,
    "author": "much. GmbH",
    "website": "https://muchconsulting.de",
    "category": "Technical",
    "version": "19.0.1.1.0",
    "license": "Other proprietary",
    "depends": ["purchase_requisition", "much_qweb_updater"],
    "data": [
        "data/report_purchaserequisitions_document_din5008.xml",
        "views/purchase_requisition_views.xml",
        "views/res_company_views.xml",
        "views/res_config_setting_views.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": True,
    "active": True,
    "module_type": "official",
    "pre_init_hook": "pre_init_hook",
}
