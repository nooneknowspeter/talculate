import os
import sys

import xdg

cwd = os.getcwd()
xdg_config_home = xdg.xdg_config_home()

if sys.platform == "win32":
    talc_config_folder_path = os.path.join("$env:LOCALAPPDATA\\talculate")
else:
    talc_config_folder_path = os.path.join(xdg_config_home, "talculate")

config_file_path = os.path.join(talc_config_folder_path, "config.yaml")
if not os.path.exists(talc_config_folder_path):
    os.mkdir(talc_config_folder_path)

if not os.path.exists(config_file_path):
    default_config_file = """# default config
bindings:
  quit: "q"
  paste: "v"
  copy_selected: "c"
  copy_line_var: "l"
  toggle_focus: "tab"
  toggle_hex: "ctrl+x"
  toggle_binary: "ctrl+b"
theme:
"""

    with open(config_file_path, "w") as file:
        file.write(default_config_file)

