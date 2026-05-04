# -*- coding: utf-8 -*-

from . import models
from .migrations.rename_migration import migrate


def pre_init_hook(env):
    migrate(env)


def post_init_hook(env):
    """Deactivate the Web Studio DIN5008 layout override and set company defaults.

    The Web Studio view replaces the entire DIN5008 layout with a frozen v17
    snapshot that uses deprecated ``l10n_din5008_template_data`` instead of
    the v19 QwebContent variables.  It must be deactivated so that the proper
    inheritance chain (base → l10n_din5008_sale → much) works correctly.
    """
    env.cr.execute(
        "UPDATE ir_ui_view SET active = false "
        "WHERE key = %s AND active = true",
        (
            "web_studio.report_editor_customization_full"
            ".view._l10n_din5008.external_layout_din5008",
        ),
    )

    # Ensure company settings for report printing are enabled
    env.cr.execute(
        "UPDATE res_company SET so_print_sale_person = true "
        "WHERE so_print_sale_person IS NOT TRUE"
    )
