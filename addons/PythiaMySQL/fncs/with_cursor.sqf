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
*			The return value of _code [any]
*
*/

params [
	["_query", [], [[]]],
	["_code", {}, [{}]],
	["_args", [], [[]]]
];

try
{
	private _cursor = _query call H2_PythiaMySQL_fnc_execute;
	private _ret = _args call _code;
	[_cursor] call H2_PythiaMySQL_fnc_close_cursor;
	_ret;
} catch
{
	throw _exception;
}