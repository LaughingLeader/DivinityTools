
templates = [
	"WPN_UNIQUE_LLGRIMOIRE_Grimoire_Death_3ef2d9c5-13e3-48a2-ab11-36f118ec7e67"
	"WPN_UNIQUE_LLGRIMOIRE_Grimoire_Fire_3d834205-a88b-459b-8e83-f44fbb166011",
	"WPN_UNIQUE_LLGRIMOIRE_Grimoire_Mimicry_c9fcc947-4423-40b9-9629-ae2d1e156dfc",
	"WPN_UNIQUE_LLGRIMOIRE_Grimoire_Swap_f4227e7f-86df-498f-817c-fc00896eb040",
	"WPN_UNIQUE_LLGRIMOIRE_Grimoire_Wind_c12e4d82-a6a5-4b3b-b29d-9e7810ff3216",
]

unequip_template = """
IF
ItemTemplateUnEquipped({template}, _Char)
THEN
LLGRIMOIRE_Grimoire_OnGrimoireUnEquipped(_Char, {template});
"""

equip_template = """
IF
ItemTemplateEquipped({template}, _Char)
AND
CharacterGetEquippedShield(_Char, (ITEMGUID)_Grimoire)
THEN
LLGRIMOIRE_Grimoire_OnGrimoireEquipped(_Char, _Grimoire, {template});
"""

final_template = """
//REGION TEMPLATE_EQUIP_EVENTS
{unequip}
{equip}
//END_REGION
"""

output_str = ""
unequip_str = ""
equip_str = ""

for template in templates:
	unequip_str += unequip_template.format(template=template)
	equip_str += equip_template.format(template=template)

output_str += final_template.format(unequip=unequip_str, equip=equip_str)

import pyperclip
pyperclip.copy(output_str)