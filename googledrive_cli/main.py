import click


@click.group
def cli():
    pass

# @click.command()
# @click.argument('path')
# def ls(path):
#     print(path)


@click.command()
@click.option('--path', default='')
def cd(path):
    print(path)


cli.add_command(cd)


def main():
    pass


if __name__ == "__main__":
    cli()
