# -*- coding: utf-8 -*-

from odoo import models


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    def _prepare_default_reversal(self, move):
        res = super()._prepare_default_reversal(move)
        if move.company_id.description_credit_note:
            res["report_header_text"] = move.company_id.description_credit_note
        return res
