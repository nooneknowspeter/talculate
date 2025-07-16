# talculate

A programmer oriented tui calculator. simple keys. minimal ui.

![talc](public/preview.gif)

## Run

```sh
pip install -r requirements.txt
python src/main.py
```

or using Make

```sh
make all
```

Run the calculator, type number, see results.

## Keybindings

- `q`: Quit
- `v`: Paste
- `c`: Copy selected value
- `l`: Copy line variable
- `tab`: Toggle focus between input and output
- `ctrl+x`: Toggle hexadecimal output
- `ctrl+b`: Toggle binary output

## Configuration

### Folder Location

The configuration files are located in:

#### Linux

The config files are located in XDG config home.

```sh
~/.config/talculate/
```

#### Windows

The config files are located in Local AppData.

```ps1
$env:LOCALAPPDATA\talculate
```

### Default Configuration

Values can be ommited but the keys cannot.

`config.yaml` uses default values when ommited

```yaml
bindings:
  quit:
  paste:
  copy_selected:
  copy_line_var:
  toggle_focus:
  toggle_hex:
  toggle_binary:
theme:
```

