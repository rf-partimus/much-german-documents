# -*- coding: utf-8 -*-
import logging
import time

from . import models
from . import wizard
from odoo.addons.much_qweb_updater.hooks import create_report_header_text_column
from odoo.addons.much_qweb_updater.migrations.rename_migration import migrate


def pre_init_hook(env):
    _logger = logging.getLogger("QWeb-Account-Hook")

    migrate(
        env,
        old_module_name="much_ofd_qweb_updater_account",
        new_module_name="much_qweb_updater_account",
    )

    cr = env.cr

    create_report_header_text_column(cr, "account_move")

    _logger.info("Generating delivery start and end date columns for aml/aml")

    cr.execute(
        "ALTER TABLE account_move ADD COLUMN IF NOT EXISTS delivery_start_date date"
    )
    cr.execute(
        "ALTER TABLE account_move ADD COLUMN IF NOT EXISTS delivery_end_date date"
    )
    cr.execute(
        "ALTER TABLE account_move_line ADD COLUMN IF NOT EXISTS delivery_start_date "
        "date"
    )
    cr.execute(
        "ALTER TABLE account_move_line ADD COLUMN IF NOT EXISTS delivery_end_date date"
    )

    _logger.info("Delivery start and end date columns generated for am/aml")
