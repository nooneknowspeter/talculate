import ast
import operator as op
import re
import statistics

import pyperclip
from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Label, ListItem, ListView, OptionList, Static, TextArea

from talculate.user_config import (
    user_config_bindings,
    user_custom_theme,
    user_selected_theme,
)


class ClickableFooterItem(Static):
    def __init__(self, label: str, id: str, on_click=None):
        super().__init__(label, id=id, classes="footer-item")
        self.on_click_handler = on_click

    def on_click(self) -> None:
        if self.on_click_handler:
            self.on_click_handler()


class CustomFooter(Horizontal):
    DEFAULT_CSS = """
    CustomFooter {
        width: 100%;
        height: 1;
        layout: grid;
        grid-size: 8;
        grid-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
    }
    ClickableFooterItem {
        padding: 0 1;
        height: 1;
    }
    ClickableFooterItem.clickable {
        color: $accent;
    }
    """

    def __init__(self, items):
        super().__init__()
        self.items = items

    def add_item(self, label: str, id: str, on_click=None):
        self.items.append((label, id, on_click))

    def compose(self) -> ComposeResult:
        yield from self.items


class Calculator(App):
    CSS = """
    Horizontal {
    }
    TextArea {
        width: 50%;
        height: 100%;
        scrollbar-size: 1 1;
    }
    ListView {
        width: 50%;
        height: 100%;
        scrollbar-size: 1 1;
    }
    CustomFooter {
        dock: bottom;
    }
    #calculation_options {
        align: center middle;
        width: 20;
        height: auto;
    }
    """
    BINDINGS = [
        Binding(
            key=user_config_bindings["quit"],
            action="quit",
            description="quit",
            priority=True,
        ),
        Binding(
            key=user_config_bindings["paste"],
            action="paste",
            description="paste",
            priority=True,
        ),
        Binding(
            key=user_config_bindings["copy_selected"],
            action="copy_selected",
            description="copy val",
        ),
        Binding(
            key=user_config_bindings["copy_line_var"],
            action="copy_line_var",
            description="copy var",
        ),
        Binding(
            key=user_config_bindings["toggle_focus"],
            action="toggle_focus",
            description="focus",
            priority=True,
        ),
        Binding(
            key=user_config_bindings["toggle_hex"],
            action="toggle_hex",
            description="hex",
            priority=True,
        ),
        Binding(
            key=user_config_bindings["toggle_binary"],
            action="toggle_binary",
            description="bin",
        ),
    ]

    def __init__(self):
        super().__init__()
        self.lines = {}
        self.output_base = 10
        self.current_calculation = "sum"

    def compose(self) -> ComposeResult:
        footer_items = []
        for binding in self.BINDINGS:
            footer_items.append(
                ClickableFooterItem(
                    f"{binding.key}: {binding.description}", binding.action
                )
            )
        footer_items.append(
            ClickableFooterItem(
                self.get_calculation_text(),
                "calculation",
                on_click=self.toggle_calculation_options,
            )
        )

        yield CustomFooter(footer_items)
        with Horizontal():
            yield TextArea.code_editor(id="input")
            yield ListView(id="output")

    def on_mount(self):
        self.input = self.query_one("#input", TextArea)
        self.output = self.query_one("#output", ListView)
        self.footer = self.query_one(CustomFooter)
        self.calculate()
        self.register_theme(user_custom_theme)
        self.theme = user_selected_theme

    def toggle_calculation_options(self):
        if self.query("#calculation_options"):
            self.query_one("#calculation_options").remove()
        else:
            option_list = OptionList(
                "Sum", "Average", "Median", "Min", "Max", id="calculation_options"
            )
            option_list.focus()
            self.mount(option_list)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.current_calculation = event.option.prompt.lower()
        self.query_one("#calculation_options").remove()
        self.query_one("ClickableFooterItem#calculation").update(
            self.get_calculation_text()
        )

    def get_calculation_text(self):
        values = list(self.lines.values())
        if not values:
            return f"{self.current_calculation} = 0"

        if self.current_calculation == "sum":
            result = sum(values)
        elif self.current_calculation == "average":
            result = statistics.mean(values)
        elif self.current_calculation == "median":
            result = statistics.median(values)
        elif self.current_calculation == "min":
            result = min(values)
        elif self.current_calculation == "max":
            result = max(values)

        return f"{self.current_calculation} = {result:.2f}"

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id == "input":
            self.calculate()

    def sync_input_cursor(self, index):
        if index is not None and 0 <= index < len(self.input.text.split("\n")):
            self.input.move_cursor((index, 0))

    def action_paste(self):
        self.input.insert(pyperclip.paste())

    def action_toggle_focus(self) -> None:
        if self.input.has_focus:
            self.output.focus()
            cursor_line, _ = self.input.cursor_location
            self.output.index = cursor_line
        elif self.output.has_focus:
            self.input.focus()

    def action_toggle_hex(self) -> None:
        self.output_base = 16 if self.output_base != 16 else 10
        self.calculate()

    def action_toggle_binary(self) -> None:
        self.output_base = 2 if self.output_base != 2 else 10
        self.calculate()

    def action_copy_selected(self) -> None:
        if self.output.has_focus:
            selected = self.output.highlighted_child
            if selected:
                text = selected.children[0].render()
                pyperclip.copy(text)
                self.notify(f"Copied '{text}' to clipboard")

    def action_copy_line_var(self) -> None:
        if self.output.has_focus:
            selected = self.output.highlighted_child
            if selected:
                text = str(self.output.index + 1)
                pyperclip.copy(f"line{text}")
                self.notify(f"Copied 'line{text}' to clipboard")

    def calculate(self):
        input_lines = self.input.text.split("\n")
        current_items = self.output.children
        new_items = []

        if not self.input.text:
            self.lines = {}

        for i, line in enumerate(input_lines):
            try:
                result = self.evaluate(line)
                self.lines[f"line{i + 1}"] = result
                formatted_result = self.format_result(result)

                if i < len(current_items):
                    # Update existing ListItem's Label
                    current_items[i].children[0].update(formatted_result)
                    new_items.append(current_items[i])
                else:
                    # Create new ListItem
                    new_items.append(ListItem(Label(formatted_result)))
            except Exception as e:
                if i < len(current_items):
                    current_items[i].children[0].update("...")
                    new_items.append(current_items[i])
                else:
                    new_items.append(ListItem(Label("...")))

        # Add new items or Remove any excess items
        if len(new_items) < len(current_items):
            remove_indices = list(range(len(new_items), len(current_items)))
            self.output.remove_items(remove_indices)
        else:
            self.output.extend(new_items[len(current_items) :])

        cursor_line, _ = self.input.cursor_location
        self.output.index = cursor_line
        self.query_one("ClickableFooterItem#calculation").update(
            self.get_calculation_text()
        )

    def evaluate(self, expr):
        def eval_expr(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return operators[type(node.op)](
                    eval_expr(node.left), eval_expr(node.right)
                )
            elif isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](eval_expr(node.operand))
            elif isinstance(node, ast.Name):
                if node.id not in self.lines:
                    raise NameError(f"Name '{node.id}' is not defined")
                return self.lines[node.id]
            elif isinstance(node, ast.Call):
                func_name = node.func.id
                if func_name not in custom_functions:
                    raise NameError(f"Function '{func_name}' is not defined")
                args = [eval_expr(arg) for arg in node.args]
                return custom_functions[func_name](*args)
            else:
                raise ValueError(f"Unsupported node type: {type(node)}")

        operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
            ast.BitXor: op.xor,
            ast.USub: op.neg,
            ast.LShift: op.lshift,
            ast.RShift: op.rshift,
            ast.BitOr: op.or_,
            ast.BitAnd: op.and_,
            ast.Invert: op.invert,
        }

        def parse_number(match):
            num = match.group(0)
            if num.startswith("0x"):
                return str(int(num, 16))
            elif num.startswith("0b"):
                return str(int(num, 2))
            return num

        # Custom functions
        def to_bin(x):
            return bin(int(x))

        def to_hex(x):
            return hex(int(x))

        def to_dec(x):
            return int(x)

        custom_functions = {"bin": to_bin, "hex": to_hex, "dec": to_dec}

        # Replace number literals with their decimal equivalents
        expr = re.sub(r"\b(0x[0-9a-fA-F]+|0b[01]+|\d+)\b", parse_number, expr)

        if not expr.strip():
            raise ValueError("Empty expression")

        tree = ast.parse(expr, mode="eval")
        result = eval_expr(tree.body)
        return (
            int(result) if isinstance(result, float) and result.is_integer() else result
        )

    def format_result(self, result):
        if isinstance(result, int):
            if self.output_base == 16:
                return f"0x{result:X}"
            elif self.output_base == 2:
                return f"0b{result:b}"
        elif isinstance(result, str):
            # For bin() and hex() results
            return result
        return str(result)


def run():
    app = Calculator()
    app.run()


if __name__ == "__main__":
    run()
