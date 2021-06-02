/**
* Closes a database cursor.
* 
* Example:
*		['CursorToken'] call H2_PythiaMySQL_fnc_close_cursor;
* 
* Parameters:
*		_token: Database cursor token [string]
*
* Return Value:
*		Nothing
*/
params['_token'];

private _result = ["pythiaMySQL.connector.close_cursor", [_token]] call py3_fnc_callExtension;

if(!(_result select 0)) then
{
	throw _result select 1;
}