# Pythia-MySQL
A simple MySQL connector for ArmA 3 build with Pythia. 
Used and maintained by [Rosenrudel](https://discord.com/invite/ep8FcXT).

## Installation
- Get the latest version of [Pythia](https://github.com/overfl0/Pythia/releases)
- Install pythia on your arma server as a normal mod
- Get the latest version of [Pythia-MySQL](https://github.com/GermanHydrogen/Pythia-MySQL/releases)
- Install Pythia-MySQL on your arma server as a normal mod
- Open both mods in the explorer and drag the 'requirements.txt' from Pythia-MySQL onto the 'install_requirements' from Pythia

In a production env. it is recommended to use Pythia-Mysql as a server mod only.

## Usage Example
Example function, which loads the last player position from the database
and then teleports the player to this position.

```sqf
params['_player'];

// Connect to the db
private _db = [
                '127.0.0.1', 
                'MyUser', 
                'MyPasswd', 
                'MyDatabase', 
                3306
                ] call H2_PythiaMySQL_fnc_connect;

// Get the players uid, 
// which in this case is the primary ident. for the table players
private _uid = getPlayerUID _player;

// Get the position from the table 'players'
private _pos = [
                    [
                        _db, 
                        "SELECT xPos, yPos, zPos FROM players WHERE uid = %s", 
                        [_uid]
                    ],
                    {
                        [_cursor] call H2_PythiaMySQL_fnc_fetchone;
                    }
                ] call H2_PythiaMySQL_fnc_with_cursor;

// Teleports the player
_player setPos _pos;
// Close db
[_db] call H2_PythiaMySQL_fnc_close;
```

## Functions
### Connect
`H2_PythiaMySQL_fnc_connect`


| Arguments | Name | Type | Optional (default value)|
| -------- | -------- | -------- | -------- |
| 0     | Url     | string     | required |
| 1     | Username     | string     | required |
| 2     | Password     | string     | required |
| 3     | Database     | string     | required |
| 4     | Port     | integer     | required |
| R     | Database handle     | string     | Return value |


Establishes a connection to a database and returns a database handle.
The handle is needed for all further commands.

**Example:**
```sqf
private _handle = ['127.0.0.1', 
                   'MyUser', 
                   'MyPasswd', 
                   'MyDatabase', 
                   3306
                  ] call H2_PythiaMySQL_fnc_connect;
```

### Close
`H2_PythiaMySQL_fnc_close`


| Arguments | Name | Type | Optional (default value)|
| -------- | -------- | -------- | -------- |
| 0     | Database handle     | string     | required |
| R     | None     | None     | Return value |

Closes a previously established connection.

**Example:**
```sqf
[_handle] call H2_PythiaMySQL_fnc_close;
```

### Execute
`H2_PythiaMySQL_fnc_execute`

| Arguments | Name | Type | Optional (default value)|
| -------- | -------- | -------- | -------- |
| 0     | Database handle     | string     | required |
| 1     | Query     | string     | required |
| 2     | Query Arguments     | string     | optional (default: []) |
| 3     | Cursor handle     | string     | optional (default: "") |
| R     | Cursor handle     | string     | Return value |

Executes a MySQL query. In the query '%s' can be used as a placeholder for arguments.
If no cursor handle is supplied in the arguments a new cursor handle is created and
returned.
The cursor is needed to later retrieve the query results.

**Example:**
```sqf
private _cursor = [
                    "SELECT * FROM players WHERE name = %s", 
                    ["Dieter"]
                  ] call H2_PythiaMySQL_fnc_execute;
```

### Fetch one
`H2_PythiaMySQL_fnc_fetchone`

| Arguments | Name | Type | Optional (default value)|
| -------- | -------- | -------- | -------- |
| 0     | Cursor handle     | string     | required |
| R     | Query Result    | [any]     | Return value |

Fetches the next row of a query result set after a query with *execute* was processed.

**Example:**
```sqf
private _result = [_cursor] call H2_PythiaMySQL_fnc_fetchone;
```

### Fetch all
`H2_PythiaMySQL_fnc_fetchall`

| Arguments | Name | Type | Optional (default value)|
| -------- | -------- | -------- | -------- |
| 0     | Cursor handle     | string     | required |
| R     | Query Result    | [[any]]     | Return value |

Fetches all rows of a query result set after a query with *execute* was processed.

**Example:**
```sqf
private _results = [_cursor] call H2_PythiaMySQL_fnc_fetchall;
```

### Close Cursor
`H2_PythiaMySQL_fnc_close_cursor`

| Arguments | Name | Type | Optional (default value)|
| -------- | -------- | -------- | -------- |
| 0     | Cursor handle     | string     | required |
| R     | None    | None    | Return value |

Closes a database cursor. Should be done for every unnecessary cursor, because to
many open cursors could lead to a failure of the database connection.

**Example:**
```sqf
[_cursor] call H2_PythiaMySQL_fnc_close_cursor;
```

### With Cursor
`H2_PythiaMySQL_fnc_with_cursor`

| Arguments | Name | Type | Optional (default value)|
| -------- | -------- | -------- | -------- |
| 0     | Arguments to  `H2_PythiaMySQL_fnc_execute`   | list     | required |
| 1     | Code to be executed on a successful query   | string     | optional (default: {}) |
| 2     | Arguments to the code     | string     | optional (default: []) |
| R     | Results from the given code | any  | Return value |

Executes a query in the given database and store the result (if available).
Then, execute some code. After the code is done, free the variable. Code
executed can reference the variable `_cursor` (variable handle). In case of
an error, callback will not be executed.
So this is more or less a wrapper which handles the opening and closing of the
cursor for you.

**Example:**
```sqf
private _result = [
                    [_handle, "SELECT * FROM players where name = %s;", ['alice']],
		            {
			            [_cursor] call H2_PythiaMySQL_fnc_fetchall;
                    }
                  ] call H2_PythiaMySQL_fnc_with_cursor;
```
