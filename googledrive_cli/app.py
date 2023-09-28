import cmd2
import argparse
from googledrive_cli.data_types.storable import Directory, Document
from googledrive_cli.storage import CloudStorage, LocalStorage
from typing import Type
from googledrive_cli.exceptions import *


class Application(cmd2.Cmd):
    def __init__(self, local_storage: LocalStorage, remote_storage: CloudStorage):
        super().__init__()
        self._local_storage = local_storage
        self._remote_storage = remote_storage

    cd_parser = cmd2.Cmd2ArgumentParser()
    cd_parser.add_argument('-r', '--remote', action='store_true')
    cd_parser.add_argument('path', nargs='?', help='path go to', default='')

    @cmd2.with_argparser(cd_parser)
    def do_cd(self, args):
        try:
            if args.remote:
                self._remote_storage.cd(args.path)
            else:
                self._local_storage.cd(args.path)
        except PathNotExistsError as e:
            self.poutput(str(e))

    ls_parser = cmd2.Cmd2ArgumentParser()
    ls_parser.add_argument('-r', '--remote', action='store_true')

    @cmd2.with_argparser(ls_parser)
    def do_ls(self, args):
        if args.remote:
            self._remote_storage.display()
        else:
            self._local_storage.display()

    mkdir_parser = cmd2.Cmd2ArgumentParser()
    mkdir_parser.add_argument('-r', '--remote', action='store_true')
    mkdir_parser.add_argument('directory_name', help='directory name')

    @cmd2.with_argparser(mkdir_parser)
    def do_mkdir(self, args):
        try:
            if args.remote:
                self._remote_storage.add(Directory(args.directory_name))
            else:
                self._local_storage.add(Directory(args.directory_name))
        except StorableNameAlreadyExists as e:
            self.poutput(str(e))

    download_parser = cmd2.Cmd2ArgumentParser()
    download_parser.add_argument('path')

    @cmd2.with_argparser(download_parser)
    def do_download(self, args):
        try:
            downloaded = self._remote_storage.download_component(args.path)
            self._local_storage.current_dir.add(downloaded)

        except StorableObjectNotExists as e:
            self.poutput((str(e)))

        except StorableNameAlreadyExists as e:
            self.poutput(str(e) + '. Download canceled')

    touch_parser = cmd2.Cmd2ArgumentParser()
    touch_parser.add_argument('-r', '--remote', action='store_true')
    touch_parser.add_argument( 'document_name')
    touch_parser.add_argument('text', default='', nargs='+')

    @cmd2.with_argparser(touch_parser)
    def do_touch(self, args):
        try:
            text = args.text
            if isinstance(args.text, list):
                text = ' '.join(args.text)

            if args.remote:
                self._remote_storage.add(Document(args.document_name, text))
            else:
                self._local_storage.add(Document(args.document_name, text))
        except StorableNameAlreadyExists as e:
            self.poutput(str(e))

    cat_parser = cmd2.Cmd2ArgumentParser()
    cat_parser.add_argument('-r', '--remote', action='store_true')
    cat_parser.add_argument('document_name')

    @cmd2.with_argparser(cat_parser)
    def do_cat(self, args):
        try:
            storable = None
            if args.remote:
                storable = self._remote_storage.current_dir.get_child(args.document_name)
            else:
                storable = self._local_storage.current_dir.get_child(args.document_name)
            storable.display_data()
        except StorableObjectNotExists as e:
            self.poutput(str(e))
        except AttributeError:
            self.poutput(f'This storable object it is not a document')



