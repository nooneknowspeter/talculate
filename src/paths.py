import os
import sys

import xdg

cwd = os.getcwd()
xdg_config_home = xdg.xdg_config_home()

if sys.platform == "win32":
    talc_config_folder_path = os.path.join("$env:LOCALAPPDATA\\talculate")
else:
    talc_config_folder_path = os.path.join(xdg_config_home, "talculate")

