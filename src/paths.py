import os
import sys

import xdg

cwd = os.getcwd()
xdg_config_home = xdg.xdg_config_home()

if sys.platform == "win32":
else:

