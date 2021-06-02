/**
* Fetches the next row of a query result set.
* 
* Example:
*		['CursorToken'] call H2_PythiaMySQL_fnc_fetchone;
* 
* Parameters:
*		_token: Database cursor token [string]
*
* Return Value:
*		[list]
*/
params['_token'];

private _result = ["pythiaMySQL.connector.fetchone", [_token]] call py3_fnc_callExtension;

if(!(_result select 0)) then
{
	throw _result select 1;
}else
{
	_result select 1;
};