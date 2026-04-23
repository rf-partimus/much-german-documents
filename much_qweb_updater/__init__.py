# -*- coding: utf-8 -*-

from . import models
from .migrations.rename_migration import migrate


def pre_init_hook(env):
    migrate(env)
