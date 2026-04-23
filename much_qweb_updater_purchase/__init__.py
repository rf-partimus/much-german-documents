# -*- coding: utf-8 -*-

from . import models
from odoo.addons.much_qweb_updater.hooks import create_report_header_text_column
from odoo.addons.much_qweb_updater.migrations.rename_migration import migrate


def pre_init_hook(env):
    migrate(
        env,
        old_module_name="much_ofd_qweb_updater_purchase",
        new_module_name="much_qweb_updater_purchase",
    )
    create_report_header_text_column(env.cr, "purchase_order")
