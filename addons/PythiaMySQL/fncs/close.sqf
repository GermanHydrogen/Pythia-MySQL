/**
* Closes a connection to a database.
* 
* Example:
*	['myto0ken'] call H2_PythiaMySQL_fnc_close;
* 
* Parameters:
*		_token: Database connection token [string]
*
* Return Value:
*		Nothing
*/
params['_token'];

private _result = ["pythiaMySQL.connector.close", [_token]] call py3_fnc_callExtension;

if(!(_result select 0)) then
{
	throw _result select 1;
}