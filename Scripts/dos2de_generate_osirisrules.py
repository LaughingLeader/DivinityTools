

templates = [
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Air_72a7d3aa-02d7-4c9b-a565-d94c8a5664b0",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Corrosive_598b8cb5-7f76-4c50-a609-2a3cd0aa0415",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Earth_8a29169a-e73d-4878-9769-8b4555140fb0",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Fire_1fe1e11c-2e54-4104-b80a-b6fa0b4b8e99",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Normal_baf9826a-abe8-4bc8-8c56-b68b5611c223",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Poison_c3f61b7d-5183-4664-9773-0b630374b7c9",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Shadow_7dcb9e1f-b807-4321-8408-c66f833ae73c",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_Water_40af98d5-3584-40cc-8c9f-e3a49564f365",
	"LOOT_Rune_LLWEAPONEX_Crossbow_Bolt_WeaponProxy_8c1da19c-02e9-4a6c-b253-1b3e31b7740f"
]

osiris_rules_template = """
IF
ItemTemplateAddedToCharacter({template}, _Item, _Char)
THEN
LLWEAPONEX_HandCrossbow_TryInsertBolt(_Char, _Item, \"{template}\", 0);

IF
CharacterUsedItemTemplate(_Char, \"{template}\", _Item)
THEN
LLWEAPONEX_HandCrossbow_TryInsertBolt(_Char, _Item, \"{template}\", 1);

IF
RuneInserted(_Char, _HandCrossbow, \"{template}\", _Slot)
THEN
LLWEAPONEX_HandCrossbow_OnBoltInserted(_Char, _HandCrossbow, \"{template}\", _Slot);
"""

elemental_arrowhead_template = """
IF
CharacterStatusRemoved(_Char, "{status}", _)
THEN
NOT DB_MyMod_Temp_ElementalArrowheadUsers(_Char, "{status}");
MyMod_ToggleScript_Disable("MyMod_TS_ElementalArrowheads");

IF
CharacterStatusApplied(_Char, "{status}", _)
THEN
DB_MyMod_Temp_ElementalArrowheadUsers(_Char, "{status}");
MyMod_ToggleScript_Enable("MyMod_TS_ElementalArrowheads");
"""

statuses = [
	"ARROWHEAD_BLOOD",
	"ARROWHEAD_ELECTRIC",
	"ARROWHEAD_FIRE",
	"ARROWHEAD_OIL",
	"ARROWHEAD_POISON",
	"ARROWHEAD_WATER"
]

runeblade_statuses = [
"LLWEAPONEX_ACTIVATE_RUNEBLADE_AVALANCHE",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_BLOOD_AIR",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_BLOOD_EARTH",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_BLOOD_FIRE",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_BLOOD_POISON",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_BLOOD_WATER",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_CONDUCTION",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_CONTAMINATION",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_DUST",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_EXPLOSIVE",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_GAS",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_HEATWAVE",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_LAVA",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_SEARING",
"LLWEAPONEX_ACTIVATE_RUNEBLADE_TAR"
]

runeblade_status_template = """
IF
CharacterStatusApplied(_Char, "{status}", _)
THEN
LLWEAPONEX_Runeblades_OnBonusDamageStatusApplied(_Char, "{status}");
"""

import pyperclip

output_str = ""

for t in runeblade_statuses:
	output_str += runeblade_status_template.format(status=t)

pyperclip.copy(output_str)