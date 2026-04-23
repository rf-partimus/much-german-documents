import logging


def _migrate(
    env,
    old_module_name,
    new_module_name,
):
    _logger = logging.getLogger(
        f"QWeb-Migration-Script: {old_module_name} -> {new_module_name}"
    )
    _logger.info("Renaming ir_module_dependency")
    env.cr.execute(
        "UPDATE ir_module_module_dependency "
        f"SET name='{new_module_name}' "
        f"WHERE name='{old_module_name}';"
    )
    _logger.info("Updating ir_model_data")
    env.cr.execute(
        f"UPDATE ir_model_data SET module='{new_module_name}'"
        f"WHERE module='{old_module_name}'"
    )
    _logger.info("Updating app list")
    env["ir.module.module"].update_list()
    _logger.info("Cleaning up redundant menu items")
    env.cr.execute(
        "delete from ir_ui_menu where id in "
        "(select res_id from ir_model_data "
        f"where module='{old_module_name}' "
        "and model='ir.ui.menu')"
    )
    _logger.info("Cleaning up redundant actions")
    env.cr.execute(
        "delete from ir_actions where id in "
        "(select res_id from ir_model_data "
        f"where module='{old_module_name}' "
        "and model='ir.actions.act_window')"
    )
    _logger.info("Cleaning up redundant ir_model_data")
    env.cr.execute(f"DELETE FROM ir_model_data WHERE module='{old_module_name}'")
    _logger.info("Cleaning up redundant views")
    env.cr.execute(f"DELETE FROM ir_ui_view WHERE arch_fs LIKE '{old_module_name}%';")
    _logger.info("Cleaning up redundant ir_module_module")
    env.cr.execute(f"DELETE FROM ir_module_module WHERE name='{old_module_name}';")


def migrate(
    env, old_module_name="much_ofd_qweb_updater", new_module_name="much_qweb_updater"
):
    env.cr.execute(f"SELECT * from ir_module_module WHERE name='{old_module_name}';")
    res = env.cr.dictfetchall()
    if res:
        _migrate(env, old_module_name, new_module_name)
