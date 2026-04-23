# -*- coding: utf-8 -*-
import logging
import time


def create_report_header_text_column(cr, table_name):
    """
    Creates report_header_text column for the specified table.
    This prevents expensive recomputation on large datasets during fresh installs.
    """
    _logger = logging.getLogger(f"QWeb-Hook: {table_name}")

    start_time = time.time()
    _logger.info(
        "============= Report header text column creation for %s start =============",
        table_name,
    )

    try:
        cr.execute(  # pylint: disable=E8103
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN IF NOT EXISTS report_header_text text
        """
        )
        elapsed_time = time.time() - start_time
        _logger.info(
            "Report header text column created for %s, elapsed time: %.3f seconds",
            table_name,
            elapsed_time,
        )
        _logger.info(
            "============= Report header text column creation"
            "for %s finished, took %.3f seconds =============",
            table_name,
            elapsed_time,
        )
    except Exception as e:
        elapsed_time = time.time() - start_time
        _logger.error(
            "Failed to create report header text column for %s after %.3f seconds: %s",
            table_name,
            elapsed_time,
            str(e),
        )
        _logger.error(
            "============= Report header text column creation"
            "for %s failed, took %.3f seconds =============",
            table_name,
            elapsed_time,
        )
        raise
