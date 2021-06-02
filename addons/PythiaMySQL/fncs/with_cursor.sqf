/**
*
*	Execute a query in the given database and store the result (if available).
*	Then, execute some code. After the code is done, free the variable. Code
*	executed can reference the variable _cursor (variable handle). In case of
*	an error, callback will not be executed.
*
*	Example:
*	private _result = [
*		['myTo0ken', "SELECT * FROM %s;", [_tableName]],
*		{
*			[_cursor] call H2_PythiaMySQL_fnc_fetchall;
*		}
*	] call H2_PythiaMySQL_fnc_with_cursor;
*
*	Parameters:
*			_query: Database query; arguments to H2_PythiaMySQL_fnc_execute [list]
*			_code: Code to be executed on a successful query; can reference _cursor. [code]
			_args: Arguments to the _code [list]
*	Return Value:
*			Error in case there was one or the return value of _code [string|any]
*
*/

params [
	["_query", [], [[]]],
	["_code", {}, [{}]],
	["_args", [], [[]]]
];

private _cursor = _query call H2_PythiaMySQL_fnc_execute;
private _ret = _args call _code;
[_cursor] call H2_PythiaMySQL_fnc_close_cursor;
_ret;