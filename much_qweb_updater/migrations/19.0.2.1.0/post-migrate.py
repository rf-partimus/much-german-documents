# Setzt das randlose 2026-Paperformat als Firmenstandard (Design 2026).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute(
        """
        UPDATE res_company
        SET paperformat_id = (
            SELECT res_id FROM ir_model_data
            WHERE module = 'much_qweb_updater'
              AND name = 'paperformat_din5008_much_2026'
        )
        WHERE paperformat_id IN (
            SELECT res_id FROM ir_model_data
            WHERE module = 'l10n_din5008'
              AND name IN ('paperformat_euro_din', 'paperformat_euro_din_a')
        )
        """
    )
    _logger.info("Design 2026: %s Firmen auf randloses Paperformat umgestellt", cr.rowcount)
