class CfgPatches {
	class H2_PythiaSQL {
        name = "Pythia MySQL";
		author = "GermanHydrogen";
        url = "https://github.com/GermanHydrogen/Pythia-MySQL";
		requiredVersion = 0.1;
		requiredAddons[]= {
            "CBA_MAIN",
			"CBA_Extended_EventHandlers"
        };
		units[] = {};
        weapons[] = {};
	};
};

/* CBA XEH */
class Extended_PreInit_EventHandlers {
    meineMod_preInit = "call compile preprocessFileLineNumbers '\PythiaMySQL\preInit.sqf'";
};
