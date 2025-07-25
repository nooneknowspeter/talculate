import yaml
from textual.theme import Theme

from talculate.paths import config_file_path, theme_file_path

default_bindings = {
    "quit": "q",
    "paste": "v",
    "copy_selected": "c",
    "copy_line_var": "l",
    "toggle_focus": "tab",
    "toggle_hex": "ctrl+x",
    "toggle_binary": "ctrl+b",
}

with open(file=config_file_path, mode="r") as file:
    config_file = yaml.safe_load(file)

    user_config_bindings = {
        default_action: (
            bind if not bind is None and default_action == action else default_bind
        )
        for (default_action, default_bind), (action, bind) in zip(
            default_bindings.items(), config_file["bindings"].items()
        )
    }

    user_selected_theme = "textual-dark"

    if not config_file["theme"] is None:
        user_selected_theme = config_file["theme"]

with open(file=theme_file_path, mode="r") as file:
    theme_file = yaml.safe_load(file)

    user_custom_theme = Theme(
        name=theme_file["name"],
        primary=theme_file["primary"],
        secondary=theme_file["secondary"],
        accent=theme_file["accent"],
        foreground=theme_file["foreground"],
        background=theme_file["background"],
        success=theme_file["success"],
        warning=theme_file["warning"],
        error=theme_file["error"],
        surface=theme_file["surface"],
        panel=theme_file["panel"],
        dark=theme_file["dark"],
    )
