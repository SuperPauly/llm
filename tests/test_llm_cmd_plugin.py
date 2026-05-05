import tomllib
from pathlib import Path

from click.testing import CliRunner

from llm import cli
from llm.plugins import pm
import llm_cmd


def test_pyproject_declares_llm_cmd_plugin_metadata():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    assert pyproject["project"]["name"] == "llm-cmd"
    assert pyproject["project"]["requires-python"] == ">=3.10"
    assert pyproject["project"]["entry-points"]["llm"]["cmd"] == "llm_cmd"


def test_cmd_command_registered_via_llm_plugin_hook():
    runner = CliRunner()
    pm.register(llm_cmd, name="llm_cmd")
    pm.hook.register_commands(cli=cli.cli)
    try:
        result = runner.invoke(cli.cli, ["cmd", "echo hello"])
        assert result.exit_code == 0
        assert result.output.strip() == "echo hello"
    finally:
        pm.unregister(name="llm_cmd")
