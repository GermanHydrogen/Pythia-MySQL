#define DEC(FNCNAME) H2_PythiaMySQL_fnc_##FNCNAME = compile preprocessFileLineNumbers '\PythiaMySQL\fncs\##FNCNAME##.sqf';

DEC(connect);
DEC(close);

DEC(execute);
DEC(close_cursor);
DEC(fetchone);
DEC(fetchall);
DEC(with_cursor)