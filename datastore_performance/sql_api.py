from __future__ import absolute_import

import logging
import os.path
from contextlib import closing, contextmanager

import pg8000
from DBUtils.PooledDB import PooledDB
from google.appengine.api import datastore
from google.appengine.datastore import entity_pb
from google.appengine.ext import db
from google.appengine.ext.db import NotSavedError
from simpleflake import simpleflake

_logger = logging.getLogger(__name__)

pool = None


class PgQueryMixin(object):

    @classmethod
    def initalize_table(cls):
        with cursor() as db_cursor:
            columns = [
                "{column} NCHAR(36) DEFAULT NULL".format(column=column)
                for column in sorted(cls._properties.keys())
            ]
            columns = ", ".join(columns)
            sql = """
            CREATE TABLE IF NOT EXISTS {table_name} (
                key_string varchar(256) PRIMARY KEY,
                {columns}
            )
            """.format(
                table_name=cls.__name__,
                columns=columns,
            )

            try:
                db_cursor.execute("BEGIN")
                db_cursor.execute(sql, tuple())
                db_cursor.execute("COMMIT")
            except Exception as e:
                _logger.error("Failed to execute SQL: {}".format(sql))
                _logger.exception(e.message)
                db_cursor.execute("ROLLBACK")
                raise NotImplementedError(sql)

    @classmethod
    def keys(cls, limit):
        cls.initalize_table()
        sql = "SELECT key_string FROM {table_name} ORDER BY key_string LIMIT {limit}".format(
            table_name=cls.__name__,
            limit=limit,
        )
        with cursor() as db_cursor:
            db_cursor.execute(sql)
            results = db_cursor.fetchall()
            keys = []
            for result in results:
                key_string = result[0]
                keys.append(db.Key(key_string))
        return keys

    @classmethod
    def get(cls, keys):
        keys, multiple = datastore.NormalizeAndTypeCheckKeys(keys)
        if not keys:
            return [] if multiple else None

        cls.initalize_table()

        columns = sorted(cls._properties.keys())

        key_strings = map(str, keys)
        key_strings = map(lambda key_string: "'{key_string}'".format(key_string=key_string), key_strings)
        key_strings = ','.join(key_strings)
        sql = "SELECT key_string, {columns} FROM {table_name} WHERE key_string IN ({key_strings})".format(
            table_name=cls.__name__,
            key_strings=key_strings,
            columns=', '.join(columns),
        )

        rows = []
        with cursor() as db_cursor:
            try:
                db_cursor.execute("BEGIN")
                db_cursor.execute(sql)
                results = db_cursor.fetchall()
                db_cursor.execute("COMMIT")
            except Exception as e:
                _logger.error("Failed to execute SQL: {}".format(sql))
                _logger.exception(e.message)
                db_cursor.execute("ROLLBACK")
                raise NotImplementedError(sql)

            for result in results:
                key_string = result[0]
                row = cls(key=db.Key(key_string))
                for index, column in enumerate(columns):
                    value = result[index + 1]
                    setattr(row, column, value)
                rows.append(row)

        grouped_rows = {str(row.key()): row for row in rows}
        output = [grouped_rows.get(key_string, None) for key_string in map(str, keys)]
        return output

    @classmethod
    def get_async(cls, keys):
        raise NotImplementedError("get_async not implemented")

    @classmethod
    def get_lazy(cls, keys):
        raise NotImplementedError("get_async not implemented")

    @classmethod
    def put(cls, models):
        cls.initalize_table()
        if not models:
            return []

        update_models = []
        insert_models = []
        for model in models:
            if '_key' in model.__dict__ and model._key:
                update_models.append(model)
            else:
                insert_models.append(model)

        columns = sorted(cls._properties.keys())

        if insert_models:
            row_values = ['%s' for _ in range(len(columns) + 1)]
            row_values = "({})".format(', '.join(row_values))
            values = [row_values for _ in range(len(insert_models))]

            args = []
            for model in models:
                model._key = db.Key.from_path(cls.kind(), simpleflake(), namespace='benchmark_test')
                row_args = [str(model.key())]
                row_args += [getattr(model, column) for column in columns]
                args.extend(row_args)
            args = tuple(args)
            sql = "INSERT INTO {table_name} (key_string, {columns}) VALUES {values}".format(
                table_name=cls.__name__,
                columns=', '.join(columns),
                values=', '.join(values),
            )
            with cursor() as db_cursor:
                try:
                    db_cursor.execute("BEGIN")
                    db_cursor.execute(sql, args)
                    db_cursor.execute("COMMIT")
                except Exception as e:
                    _logger.error("Failed to execute SQL: {}".format(sql))
                    _logger.exception(e.message)
                    db_cursor.execute("ROLLBACK")
                    raise NotImplementedError(sql)

        if update_models:
            for model in update_models:
                assignments = [
                    '{column} = %s'.format(column=column) for column in columns
                ]
                assignments = ', '.join(assignments)

                args = [getattr(model, column) for column in columns]
                args.append(str(model._key))
                args = tuple(args)
                sql = "UPDATE {table_name} SET {assignments} WHERE key_string = %s".format(
                    table_name=cls.__name__,
                    assignments=assignments,
                )
            with cursor() as db_cursor:
                try:
                    db_cursor.execute("BEGIN")
                    db_cursor.execute(sql, args)
                    db_cursor.execute("COMMIT")
                except Exception as e:
                    _logger.error("Failed to execute SQL: {}".format(sql))
                    _logger.exception(e.message)
                    db_cursor.execute("ROLLBACK")
                    raise NotImplementedError(sql)

    @classmethod
    def delete(cls, models):
        cls.initalize_table()
        if not models:
            return

        key_strings = map(str, map(lambda x: x.key(), models))
        key_strings = map(lambda key_string: "'{key_string}'".format(key_string=key_string), key_strings)
        key_strings = ','.join(key_strings)
        sql = "DELETE FROM {table_name} WHERE key_string IN ({key_strings})".format(
            table_name=cls.__name__,
            key_strings=key_strings
        )
        with cursor() as db_cursor:
            try:
                db_cursor.execute("BEGIN")
                db_cursor.execute(sql)
                db_cursor.execute("COMMIT")
            except Exception as e:
                _logger.error("Failed to execute SQL: {}".format(sql))
                _logger.exception(e.message)
                db_cursor.execute("ROLLBACK")
                raise NotImplementedError(sql)

    def key(self):
        if hasattr(self, '_key') and self._key:
            return self._key
        else:
            raise NotSavedError()

    def convert_to_proto(self):
        return self.convert_to_entity().ToPb()

    def convert_to_entity(self):
        return self._populate_entity()

    @classmethod
    def convert_from_binary(cls, binary):
        entity_proto = entity_pb.EntityProto(binary)
        return cls.convert_from_proto(entity_proto)

    @classmethod
    def convert_from_proto(cls, entity_proto):
        entity = datastore.Entity.FromPb(entity_proto)
        return cls.convert_from_entity(entity)

    @classmethod
    def convert_from_entity(cls, entity):
        return cls.from_entity(entity)


@contextmanager
def cursor():
    with closing(connection_pool().connection()) as conn:
        with closing(conn.cursor()) as new_cursor:
            yield new_cursor


def connection_pool():
    global pool
    if pool is not None:
        return pool

    if os.environ.has_key('DATABASE_PORT'):
        new_pool = _create_connection_pool_from_tcp_socket()
    else:
        new_pool = _create_connection_pool_from_unix_sock()

    # Test the current connection to verify it is healthy enough to reach the database
    with closing(new_pool.connection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('SELECT NOW() as now')
            result = cursor.fetchall()
            current_time = result[0][0]
            if not current_time:
                raise NotImplementedError("Failed to connect to database")

    # Store the connection and continue
    pool = new_pool
    return pool


def _create_connection_pool_from_tcp_socket():
    """
    Create a new instance of the connection pool using the TCP port
    :return: PooledDB
    """
    database_user = os.environ['DATABASE_USER']
    database_password = os.environ['DATABASE_PASSWORD']
    database_name = os.environ['DATABASE_NAME']
    database_host = os.environ['DATABASE_HOST']
    database_port = os.environ['DATABASE_PORT']

    pool = PooledDB(
        pg8000,
        mincached=0,
        maxcached=100,
        maxconnections=100,
        # Pass the credentials through to the caller
        user=database_user,
        password=database_password,
        database=database_name,
        unix_sock=None,
        # Explicitly set the host and port to None here to override the defaults
        host=database_host,
        port=int(database_port),
    )
    return pool


def _create_connection_pool_from_unix_sock():
    """
    Create a new instance of the connection pool.
    :return: PooledDB
    """
    database_id = os.environ['DATABASE_ID']
    database_user = os.environ['DATABASE_USER']
    database_password = os.environ['DATABASE_PASSWORD']
    database_name = os.environ['DATABASE_NAME']

    unix_sock = os.path.abspath(os.path.join("/cloudsql", database_id, '.s.PGSQL.5432'))
    pool = PooledDB(
        pg8000,
        mincached=0,
        maxcached=100,
        maxconnections=100,
        # Pass the credentials through to the caller
        user=database_user,
        password=database_password,
        database=database_name,
        # Connect using the local socket provided to us in App Engine
        unix_sock=unix_sock,
        # Explicitly set the host and port to None here to override the defaults
        host=None,
        port=None,
    )
    return pool
