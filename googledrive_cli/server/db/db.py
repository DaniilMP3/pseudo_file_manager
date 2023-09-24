import sqlite3
from typing import LiteralString, Iterable, Any
from googledrive_cli.server import config


def get_db() -> sqlite3.Connection:
    """
    Return database connection(for .database file specified in config)
    :return: sqlite3.Connection
    """
    if not getattr(get_db, 'db', None):
        db = sqlite3.connect(config.SQLITE_DB_FILE)
        get_db.db = db

    return sqlite3.connect(config.SQLITE_DB_FILE)


def fetchone(sql: LiteralString, params: Iterable[Any] | None = None) -> dict | None:
    cursor = _get_cursor(sql, params)
    row_ = cursor.fetchone()
    if not row_:
        cursor.close()
        return None
    row = _get_dict_result(cursor, row_)
    cursor.close()
    return row


def fetchall(sql: LiteralString, params: Iterable[Any] | None = None) -> list[dict] | None:
    cursor = _get_cursor(sql, params)
    rows = cursor.fetchall()
    if not rows:
        return None

    res = [_get_dict_result(cursor, row_) for row_ in rows]
    cursor.close()

    return res


def execute(sql: LiteralString, params: Iterable[Any] | None = None, autocommit: bool = True) -> None:
    cursor = _get_cursor(sql, params)
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)


def _get_cursor(sql: LiteralString, params: Iterable[Any] | None) -> sqlite3.Cursor:
    """
    :param sql: sqlite query
    :param params: params, if specified in query
    :return: sqlite3.Cursor
    """
    cursor = get_db().cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)

    return cursor


def _get_dict_result(cursor: sqlite3.Cursor, row: tuple) -> dict:
    column_names = [description[0] for description in cursor.description]
    return {column_name: row[i] for i, column_name in enumerate(column_names)}
