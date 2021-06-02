/**
* Executes a MySQL query. In the query '%s' can be used as placeholder for arguments.
* 
* Example:
*		["SELECT * FROM players WHERE name == %s", ["Dieter"]] call H2_PythiaMySQL_fnc_execute;
* 
* Parameters:
*		_db_token: Token for the database connection [string]
*		_query:	MySQL query to execute [string]
*		_args: Arguments for the query (opt)[list]
*		_cursor_token: Database cursor token (opt)[string]
*
* Return Value:
*		Token for the cursor created for the query
*/
params['_db_token', '_query', ['_args', []], ['_cursor_token', '']];

private _result = ["pythiaMySQL.connector.execute", [_db_token, _query, _args, _cursor_token]] call py3_fnc_callExtension;

if(!(_result select 0)) then
{
	throw _result select 1;
}else
{
	_result select 1;
};
