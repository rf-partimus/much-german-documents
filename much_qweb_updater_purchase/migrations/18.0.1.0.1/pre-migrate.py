from odoo import api, SUPERUSER_ID

import logging


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Start migration script for much_qweb_updater_purchase")
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Searching for view report_purchaseorder_document_l10n_din5008_much")
    view = env.ref(
        "much_qweb_updater_purchase.report_purchaseorder_document_l10n_din5008_much",
        raise_if_not_found=False,
    )
    if view:
        _logger.info(
            "Deleting inherit_id for view "
            "report_purchaseorder_document_l10n_din5008_much"
        )
        view.inherit_id = False
        _logger.info("Pre-Migrate script done.")
    else:
        _logger.warning(
            "View report_purchaseorder_document_l10n_din5008_much not found "
            "script skipped"
        )
