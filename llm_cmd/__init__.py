from llm import hookimpl
import click


@hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("prompt", required=False)
    def cmd(prompt):
        """Generate a shell command from a prompt."""
        if prompt is None:
            raise click.UsageError("Usage: llm cmd 'your request'")
        click.echo(prompt)
