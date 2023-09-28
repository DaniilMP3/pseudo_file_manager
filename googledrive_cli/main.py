from googledrive_cli.storage import CloudStorage, LocalStorage
from googledrive_cli.app import Application


def cli():
    import sys

    c = Application(LocalStorage(), CloudStorage())
    sys.exit(c.cmdloop())


def main():
    pass


if __name__ == "__main__":

    cli()
