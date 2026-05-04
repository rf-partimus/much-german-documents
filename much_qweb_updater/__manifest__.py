# -*- coding: utf-8 -*-
{
    "name": "Much OfD - QWeb Updater",
    "summary": """Automatically update and set QWeb templates""",
    "description": """""",
    "author": "much. GmbH",
    "website": "https://muchconsulting.de/",
    "category": "Technical Settings",
    "version": "19.0.1.2.2",
    "license": "Other proprietary",
    "depends": ["l10n_din5008", "l10n_de_reports"],
    "data": [
        "report/web/external_layout_din5008_much.xml",
        "views/res_company.xml",
        "views/res_config_setting_views.xml",
        "views/res_partner_views.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "much_qweb_updater/static/src/**/*",
        ],
    },
    "auto_install": False,
    "application": True,
    "module_type": "official",
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
}
