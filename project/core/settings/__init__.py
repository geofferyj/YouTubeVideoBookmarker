import os

if os.environ.get("PRODUCTION"):
    from .settings_prod import *
else:
    from .settings_dev import * 