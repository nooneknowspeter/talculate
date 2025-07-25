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
theme_file_path = os.path.join(talc_config_folder_path, "theme.yaml")


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

if not os.path.exists(theme_file_path):
    default_theme_file = """name: "custom"
primary: "#00c0d0"
secondary: "#81A1C1"
accent: "#B48EAD"
foreground: "#D8DEE9"
background: "#2E3440"
success: "#A3BE8C"
warning: "#EBCB8B"
error: "#BF616A"
surface: "#3B4252"
panel: "#434C5E"
dark: true
footer-foreground: "#FFFFFF"
footer-background: "#000000"
"""

    with open(theme_file_path, "w") as file:
        file.write(default_theme_file)
