"""CLI wiring for the ``llm cmd`` subcommand."""

import click


def register_cmd_command(cli):
    """Attach the ``cmd`` command to the passed Click group."""

    @cli.command(name="cmd")
    @click.argument("prompt", required=False)
    def cmd(prompt):
        """Generate a shell command from a prompt."""
        if prompt is None:
            raise click.UsageError("Usage: llm cmd 'your request'")
        click.echo(prompt)

    return cmd
