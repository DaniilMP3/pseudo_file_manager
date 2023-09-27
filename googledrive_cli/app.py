import cmd2
import argparse
from googledrive_cli.storage import CloudStorage, LocalStorage
from typing import Type
from googledrive_cli.exceptions import *


class Application(cmd2.Cmd):
    def __init__(self, local_storage: LocalStorage, remote_storage: CloudStorage):
        super().__init__()
        self._local_storage = local_storage
        self._cloud_storage = remote_storage

    cd_parser = cmd2.Cmd2ArgumentParser()
    cd_parser.add_argument('-r', '--remote', action='store_true')
    cd_parser.add_argument('path', help='path go to')

    @cmd2.with_argparser(cd_parser)
    def do_cd(self, args):
        # try:
        #     if args.remote:
        #         self._cloud_storage.cd(args.path)
        #     else:
        #         self._local_storage.cd(args.path)
        # except PathNotExistsError as e:
        #     self.poutput(str(e))


    mkdir_parser = cmd2.Cmd2ArgumentParser()
    mkdir_parser.add_argument('directory_name', nargs='+', help='directory name')

    @cmd2.with_argparser(mkdir_parser)
    def mkdir(self, args):
        pass







