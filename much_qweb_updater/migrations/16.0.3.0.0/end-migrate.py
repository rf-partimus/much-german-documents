# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """
    Auto Install OfD apps if all dependencies are installed
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    env["ir.module.module"].update_list()
    module_list = [
        "much_qweb_updater_account",
        "much_qweb_updater_crm",
        "much_qweb_updater_inventory",
        "much_qweb_updater_purchase",
        "much_qweb_updater_sale",
    ]
    module_ids = env["ir.module.module"].search(
        [("name", "in", module_list), ("state", "=", "uninstalled")]
    )
    for ofd_app in module_ids:
        dependencies = ofd_app.dependencies_id.filtered(
            lambda app: app.name != "much_qweb_updater"
        )
        if ofd_app.dependencies_id and all(
            dependencies.mapped(lambda x: x.state == "installed")
        ):
            ofd_app.sudo().write({"state": "to install"})
