{ lib
, python3
, fetchFromGitHub
,
}:

python3.pkgs.buildPythonApplication rec {
  pname = "talculate";
  version = "unstable-2025-07-25";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "nooneknowspeter";
    repo = "talculate";
    rev = "c11ff5e70713adaac775efe75be821635d661d73";
    hash = "sha256-5kEpZt2DIgYnAnaMpyLUcCaLMr8o5bf0X3jmNL/9wx0=";
  };

  build-system = [
    python3.pkgs.poetry-core
  ];

  dependencies = with python3.pkgs; [
    pyperclip
    pyyaml
    rich
    textual
    xdg
  ];

  pythonImportsCheck = [
    "talculate"
  ];

  meta = {
    description = "A programmer oriented tui calculator. simple keys. minimal ui";
    homepage = "https://github.com/nooneknowspeter/talculate";
    license = lib.licenses.unfree;
    maintainers = with lib.maintainers; [ nooneknowspeter ];
    mainProgram = "talculate";
  };
}
