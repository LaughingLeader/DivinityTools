
talents = [
("LLENEMY_TALENT_LONEWOLF", "LoneWolf"),
("LLENEMY_TALENT_TORTURER", "Torturer"),
("LLENEMY_TALENT_UNSTABLE", "Unstable"),
("LLENEMY_TALENT_WHATARUSH", "WhatARush"),
("LLENEMY_TALENT_LEECH", "Leech"),
("LLENEMY_TALENT_QUICKSTEP", "QuickStep"),
("LLENEMY_TALENT_SADIST", "Sadist"),
("LLENEMY_TALENT_GLADIATOR", "Gladiator"),
("LLENEMY_TALENT_HAYMAKER", "Haymaker"),
("LLENEMY_TALENT_INDOMITABLE", "Indomitable"),
("LLENEMY_TALENT_SOULCATCHER", "Soulcatcher"),
("LLENEMY_TALENT_MAGICCYCLES", "MagicCycles"),
("LLENEMY_TALENT_GREEDYVESSEL", "GreedyVessel"),
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

output_str = ""
rules_str = ""

for entry in talents:
	rules_str += status_template.format(status=entry[0], talent=entry[1])

output_str += final_template.format(rules=rules_str.strip())

import pyperclip
pyperclip.copy(output_str)