import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

STUDIO_VIEW_KEY = (
    "web_studio.report_editor_customization_full"
    ".view._l10n_din5008.external_layout_din5008"
)


def migrate(cr, version):
    """Deactivate the Web Studio customization view that overrides
    the DIN5008 layout with a frozen v17 snapshot.

    In Odoo 19, the l10n_din5008 module replaced the old
    ``l10n_din5008_template_data`` field-based approach with QWeb
    ``t-set`` body content variables (``din5008_document_information``,
    ``din5008_document_title``, ``din5008_address_block``).

    The Web Studio view (created in v17) uses ``position="replace"
    mode="inner"`` with priority 9999999, overriding all modern
    template inheritances with outdated logic.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    view = env["ir.ui.view"].search(
        [
            ("key", "=", STUDIO_VIEW_KEY),
            ("active", "=", True),
        ],
        limit=1,
    )
    if view:
        view.active = False
        _logger.info(
            "Deactivated Web Studio DIN5008 layout override (view id=%s)",
            view.id,
        )
    else:
        _logger.info(
            "Web Studio DIN5008 layout override not found or already inactive"
        )
