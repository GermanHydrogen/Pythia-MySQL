/**
* Establishes a connection to a database.
* 
* Example:
*		['MyServer', 'MyUser', 'MyPasswd', 'MyDatabase', 3306] call H2_PythiaMySQL_fnc_connect;
* 
* Parameters:
*		_url: MYSQL url [string]
*		_username: MYSQL username [string]
*		_password: User's password [string]
*		_database: Database to use [string]
*		_port: MYSQL port [integer]
*
* Return Value:
*		Database handle
*/

params["_url", "_username", "_password", "_database", "_port"];

private _result = ["pythiaMySQL.connector.connect", [_url, _username, _password, _database, _port]] call py3_fnc_callExtension;

diag_log str _result;


if(!(_result select 0)) then
{
	throw _result select 1;
}else
{
	_result select 1;
};
