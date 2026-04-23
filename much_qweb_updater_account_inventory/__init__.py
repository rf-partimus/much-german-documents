# -*- coding: utf-8 -*-

from odoo.addons.much_qweb_updater.migrations.rename_migration import migrate


def pre_init_hook(env):
    migrate(
        env,
        old_module_name="much_ofd_qweb_updater_account_inventory",
        new_module_name="much_qweb_updater_account_inventory",
    )
