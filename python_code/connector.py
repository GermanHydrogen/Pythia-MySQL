import mysql.connector
import random
import string

connections = {}
cursors = {}


def get_connection(func):
    def wrapper(token, *args, **kwargs):
        try:
            db = connections[token]
        except KeyError:
            return ''

        return func(db, *args, **kwargs)

    return wrapper


def get_cursor(func):
    def wrapper(token, *args, **kwargs):
        try:
            cursor = cursors[token]
        except KeyError:
            return ''

        return func(cursor, *args, **kwargs)

    return wrapper


def generate_token(length: int = 8):
    return "".join([random.choice(string.printable) for _ in range(0, length)])


def init(host: str = '', user: str = '', passwd: str = '', database: str = '') -> str:
    """
    Initialises the database connection.
    :param host: Hostname or IP
    :param user: Database user
    :param passwd: Password
    :param database: Database
    :return: Connection Token
    """
    try:
        db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        db.autocommit = True
    except mysql.connector.Error as e:
        return str(e)

    token = generate_token()

    global connections
    connections[token] = db

    return token


@get_connection
def close(db: mysql.connector.MySQLConnection) -> None:
    """
    Closes the database connection
    :param db: Database connection to use
    :return:
    """
    db.close()


@get_connection
def execute(db: mysql.connector.MySQLConnection, query: str, arguments: list = [], close: bool = False):
    """
    Executes a database query
    :param db: Database connection to use
    :param query: MySQL query string.
    :param arguments: Arguments for the query
    :param close: If the db cursor is closed after completion. If false, its token returned
    :return:
    """
    cursor = db.cursor()
    try:
        cursor.execute(query, arguments)
    except mysql.connector.Error:
        return

    if close:
        cursor.close()
        return
    else:
        global cursors
        token = generate_token()
        cursors[token] = cursor

        return token


@get_cursor
def close_cursor(cursor: mysql.connector.connection.MySQLCursor) -> bool:
    """
    Close the cursor.
    :param cursor:
    :return: if successful
    """
    return cursor.close()


@get_cursor
def fetchone(cursor: mysql.connector.connection.MySQLCursor) -> tuple:
    """
    Returns next row of a query result set.
    :param cursor: Database cursor
    :return:
    """
    try:
        return cursor.fetchone()
    except mysql.connector.Error:
        return None


@get_cursor
def fetchall(cursor: mysql.connector.connection.MySQLCursor) -> [tuple]:
    """
    Returns all rows of a query result set and closes the cursor.
    :param cursor: Database cursor
    :return:
    """
    try:
        result = cursor.fetchall()
    except mysql.connector.Error:
        return None

    cursor.close()
    return result


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
    token = init('localhost', 'root', '', 'arma')
    cursor = execute(token, "SELECT * FROM instances;")
    print(fetchall(cursor))

