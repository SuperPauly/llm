"""Plugin hook implementations for ``llm_cmd``."""

from llm import hookimpl

from .cli import register_cmd_command


@hookimpl
def register_commands(cli):
    """Register the ``llm cmd`` top-level subcommand."""
    register_cmd_command(cli)
