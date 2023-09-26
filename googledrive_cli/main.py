import click
from googledrive_cli.data_types.storable import Directory, Document

# @click.group
# def cli():
#     pass
#
# # @click.command()
# # @click.argument('path')
# # def ls(path):
# #     print(path)
#
#
# @click.command()
# @click.option('--path', default='')
# def cd(path):
#     print(path)
#
#
# cli.add_command(cd)


def cli():
    root_dir = Directory('Root')
    new_dir = Directory('Folder1')
    root_dir.add(new_dir)
    new_file = Document('Document1', 'Test text, test')
    new_dir.add(new_file)
    root_dir.add(Document('Document2', 'Document2 text'))
    root_dir.display()




def main():
    pass


if __name__ == "__main__":
    cli()
