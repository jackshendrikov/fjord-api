import click


@click.group()
def cli() -> None:
    """Main click group."""


if __name__ == "__main__":
    cli()
