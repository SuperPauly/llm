import ast
import importlib
import inspect
import os
from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from llm_cmd.cli import register_cmd_command


LLM_CMD_PLACEHOLDER_MODULES = [
    "llm_cmd.policy",
    "llm_cmd.render",
    "llm_cmd.history",
    "llm_cmd.fix",
    "llm_cmd.session",
    "llm_cmd.alias",
    "llm_cmd.execution",
]


@pytest.mark.parametrize("module_name", LLM_CMD_PLACEHOLDER_MODULES)
def test_llm_cmd_modules_import_without_openai_api_key(monkeypatch, module_name):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    module = importlib.import_module(module_name)
    assert module is not None


@pytest.mark.parametrize("module_name", LLM_CMD_PLACEHOLDER_MODULES)
def test_llm_cmd_placeholder_modules_have_intentional_docstring(module_name):
    module = importlib.import_module(module_name)
    assert inspect.getdoc(module) == "Module placeholder for llm cmd functionality."


def _build_test_cli():
    @click.group()
    def test_cli():
        pass

    register_cmd_command(test_cli)
    return test_cli


def test_llm_cmd_cli_parsing_unquoted_argv_tokens_are_rejected_as_extra_args():
    runner = CliRunner()
    result = runner.invoke(_build_test_cli(), ["cmd", "show", "logs"])
    assert result.exit_code != 0
    assert "unexpected extra argument" in result.output.lower()


def test_llm_cmd_cli_options_interactive_empty_input_usage_error():
    runner = CliRunner()
    result = runner.invoke(_build_test_cli(), ["cmd"])
    assert result.exit_code == 2
    assert "Usage: llm cmd 'your request'" in result.output


def test_llm_cmd_execution_module_does_not_use_shell_true_or_string_subprocess_calls():
    tree = ast.parse(Path("llm_cmd/execution.py").read_text("utf-8"))
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr not in {"run", "Popen", "call", "check_call", "check_output"}:
            continue
        for keyword in node.keywords:
            if keyword.arg == "shell":
                assert not (
                    isinstance(keyword.value, ast.Constant) and keyword.value.value is True
                )
        if node.args and isinstance(node.args[0], ast.Constant):
            assert not isinstance(node.args[0].value, str)


def test_llm_cmd_tests_do_not_require_openai_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    runner = CliRunner()
    result = runner.invoke(_build_test_cli(), ["cmd", "echo hello"])
    assert result.exit_code == 0
    assert result.output.strip() == "echo hello"
    assert os.environ.get("OPENAI_API_KEY") is None
