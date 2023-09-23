import sqlite3
from typing import LiteralString
from googledrive_cli.server import config


def get_db() -> sqlite3.Connection:
    return sqlite3.connect(config.SQLITE_DB_FILE)

def fetchone(sql: LiteralString, )
