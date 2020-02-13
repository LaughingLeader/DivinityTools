from typing import List, Dict

class TalentEntry():
	def __init__(self, status, talent):
		self.status = status
		self.talent = talent

talents:List[TalentEntry] = [
TalentEntry("LLENEMY_TALENT_GLADIATOR", "Gladiator"),
TalentEntry("LLENEMY_TALENT_GREEDYVESSEL", "GreedyVessel"),
TalentEntry("LLENEMY_TALENT_HAYMAKER", "Haymaker"),
TalentEntry("LLENEMY_TALENT_INDOMITABLE", "Indomitable"),
TalentEntry("LLENEMY_TALENT_LEECH", "Leech"),
TalentEntry("LLENEMY_TALENT_LONEWOLF", "LoneWolf"),
TalentEntry("LLENEMY_TALENT_MAGICCYCLES", "MagicCycles"),
TalentEntry("LLENEMY_TALENT_QUICKSTEP", "QuickStep"),
TalentEntry("LLENEMY_TALENT_SADIST", "Sadist"),
TalentEntry("LLENEMY_TALENT_SOULCATCHER", "Soulcatcher"),
TalentEntry("LLENEMY_TALENT_TORTURER", "Torturer"),
TalentEntry("LLENEMY_TALENT_UNSTABLE", "Unstable"),
TalentEntry("LLENEMY_TALENT_WHATARUSH", "WhatARush"),
]

status_template = """
IF
CharacterStatusApplied(_Char, "{status}", _)
THEN
NRD_CharacterSetPermanentBoostTalent(_Char, "{talent}");
CharacterAddAttribute(_Character, "Dummy", 0);
"""

final_template = """
//REGION EXTENDER_TALENT_ADDING
/*
{rules}
*/
//END_REGION
"""

block_status_template = """
PROC
LLENEMY_Upgrades_CanRollForStatusUpgrade((CHARACTERGUID)_Character, (STRING)_Group, (STRING)_Type, "{status}")
AND
CharacterHasTalent(_Character, "{talent}", 1)
THEN
DB_LLENEMY_StatusUpgradeBlocked(_Character, _Group, _Type, "{status}");
"""

block_final_template = """
//REGION TALENT_BLOCKING
{rules}
//END_REGION
"""

output_str = ""
rules_str = ""

for entry in sorted(talents, key=lambda x: {x.talent, x.status}, reverse=False):
	#rules_str += status_template.format(status=entry[0], talent=entry[1])
	rules_str += block_status_template.format(status=entry.status, talent=entry.talent)

#output_str += final_template.format(rules=rules_str.strip())
output_str += block_final_template.format(rules=rules_str.strip())

import pyperclip
pyperclip.copy(output_str)