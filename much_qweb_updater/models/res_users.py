# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
import re


class Users(models.Model):
    _inherit = "res.users"

    def get_evaluated_val(self, obj, val, check=False):
        """Evaluate dynamic vals in html field as odoo only evaluates html"""
        # Regex to match ${...} pattern
        MAIN_REGEX = r"\${.*?}"
        val = eval_val = val or ""

        # Logic here is to find whole pattern matching ${...},
        # Then extract ... from ${}, evaluate the value of ... using safe eval
        # Replace the whole match ${...} with evaluated val in the main string
        # Replace 1 match at a time to avoid errors next iterations if same
        # value is used multiple times
        try:
            matches = re.finditer(MAIN_REGEX, val, re.MULTILINE)
            for match in matches:
                to_eval_val = (match.group()).strip().split("${")[1].split("}")[0]
                val = safe_eval(to_eval_val, {"object": obj})
                eval_val = eval_val.replace((match.group()), str(val) or "", 1)
            if not check:
                return eval_val
            return True
        except Exception as e:
            raise ValidationError(
                _(
                    f"{e}\n\n The field doesn't exist in the object. "
                    f"Please check the attribute again or add the field"
                )
            )
