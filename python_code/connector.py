import mysql.connector
import random
import string


def generate_token(length: int = 8):
    return "".join([random.choice(string.printable) for _ in range(0, length)])


class Manageable(object):
    def __init__(self):
        self.data = {}

    def _create_obj(self, *args):
        raise NotImplemented

    def _del_obj(self, obj):
        raise NotImplemented

    def new(self, *args) -> (str, any):
        key = generate_token()
        self.data[key] = self._create_obj(*args)
        return key, self.data[key]

    def get(self, key: str) -> any:
        return self.data[key]

    def delete(self, obj):
        key = list(self.data.keys())[list(self.data.values()).index(obj)]
        self._del_obj(obj)
        del self.data[key]


class Connections(Manageable):
    def _create_obj(self, host, user, passwd, database, port):
        db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database,
            port=port
        )
        db.autocommit = True
        return db

    def _del_obj(self, db):
        db.close()


class Cursors(Manageable):
    def add(self, cursor):
        key = generate_token()
        self.data[key] = cursor
        return key

    def _create_obj(self, db):
        return db.cursor()

    def _del_obj(self, cursor):
        cursor.close()


connections = Connections()
cursors = Cursors()


def get_connection(func):
    def wrapper(token, *args, **kwargs):
        try:
            db = connections.get(token)
        except KeyError:
            return False, "Invalid Token!"

        return func(db, *args, **kwargs)

    return wrapper


def get_cursor(func):
    def wrapper(token, *args, **kwargs):
        try:
            cursor = cursors.get(token)
        except KeyError:
            return False, "Invalid Token!"

        return func(cursor, *args, **kwargs)

    return wrapper


def connect(host: str = '', user: str = '', passwd: str = '', database: str = '', port: int = 3306) -> (bool, str):
    """
    Initialises the database connection.
    :param host: Hostname or IP
    :param user: Database user
    :param passwd: Password
    :param database: Database
    :param port: Port of the database server
    :return: (Success, Connection Token or Error)
    """

    global connections
    token, _ = connections.new(host, user, passwd, database, port)
    return True, token


@get_connection
def close(db: mysql.connector.MySQLConnection) -> (bool, str):
    """
    Closes the database connection
    :param db: Database connection to use
    :return:
    """
    try:
        connections.delete(db)
    except mysql.connector.Error as e:
        return False, str(e)

    return True, ''


@get_connection
def execute(db: mysql.connector.MySQLConnection, query: str,
            arguments: list = [], cursor_token: str = '') -> (bool, str):
    """
    Executes a database query
    :param db: Database connection to use
    :param query: MySQL query string.
    :param arguments: Arguments for the query
    :param cursor_token: Token for a existing token
    :return:
    """
    global cursors
    if cursor_token == '':
        cursor = db.cursor()
    else:
        try:
            cursor = cursors.get(cursor_token)
        except KeyError:
            return False, "Invalid Token!"

    try:
        cursor.execute(query, arguments)
    except mysql.connector.Error as e:
        if cursor_token == "":
            cursor.close()
        return False, e

    if cursor_token == '':
        cursor_token = cursors.add(cursor)

    return True, cursor_token


@get_cursor
def close_cursor(cursor: mysql.connector.connection.MySQLCursor) -> (bool, str):
    """
    Close the cursor.
    :param cursor:
    :return: if successful
    """
    try:
        cursors.delete(cursor)
    except mysql.connector.Error as e:
        return False, e
    return True, ''


@get_cursor
def fetchone(cursor: mysql.connector.connection.MySQLCursor) -> (bool, any):
    """
    Returns next row of a query result set.
    :param cursor: Database cursor
    :return:
    """
    try:
        return True, cursor.fetchone()
    except mysql.connector.Error as e:
        return False, e


@get_cursor
def fetchall(cursor: mysql.connector.connection.MySQLCursor) -> (bool, any):
    """
    Returns all rows of a query result set.
    :param cursor: Database cursor
    :return:
    """
    try:
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        return False, e

    return True, result


@get_cursor
def lastrowid(cursor: mysql.connector.connection.MySQLCursor) -> int:
    """
    Returns the value generated for an AUTO_INCREMENT column.
    Returns the value generated for an AUTO_INCREMENT column by
    the previous INSERT or UPDATE statement or None when there is no such value available.
    :param cursor: Database cursor
    :return:
    """
    return cursor.lastrowid


if __name__ == '__main__':
    result = connect('localhost', 'root', '', 'arma', 3306)
    token = result[1]
    result = execute(token, "SELECT * FROM instances;")
    result = fetchall(result[1])
    print(result)

