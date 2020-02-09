templates = [
	("FarahGlow", "S_FARAH_Gloves_ec267978-6679-410d-9e81-3e83c1b0f396"),
	("FarahGlow", "S_FARAH_Boots_828ef4ae-98b4-4912-a6c2-f0d92afa40eb"),
	("FarahGlow", "S_FARAH_Leggings_e684304e-7f0f-43ac-9523-67fb2d4917d5"),
	("FarahGlow", "S_FARAH_Cleavage_4b7dd558-7a23-4855-8c14-387a48ca27be"),
	("FarahGlow", "S_FARAH_Cowl_d2ef56d2-5bc6-4758-b58a-b5850fdc1acf"),
	("Inquisitor", "EQ_Armor_Inquisitor_Arms_A_3805738a-63a2-4204-9f61-37e0524e68b7"),
	("Inquisitor", "EQ_Armor_Inquisitor_Helmet_A_ba0c20a3-0a54-4d55-b17a-c37d69f2d554"),
	("Inquisitor", "EQ_Armor_Inquisitor_Legs_A_8566f04e-b7dc-4c97-bbe5-1d586434f2d2"),
	("Inquisitor", "EQ_Armor_Inquisitor_Lowerbody_A_fd342b33-f8c3-425a-b3f7-11b16a4f2535"),
	("Inquisitor", "EQ_Armor_Inquisitor_Upperbody_A_7bd4666b-9cbe-4bbd-b377-5997a34e4ae9"),
]

osiris_rules_template = """
IF
ItemTemplateUnEquipped("{template}", _Character)
THEN
DARKLIGHT_TRIFORCE_ChangeSetCount(_Character, "{set}", -1);

IF
ItemTemplateEquipped("{template}", _Character)
THEN
DARKLIGHT_TRIFORCE_ChangeSetCount(_Character, "{set}", 1);
"""

region_template = """
//REGION EQUIP_EVENTS
{rules}
//END_REGION
"""

rules_str = ""
output_str = ""

for setid,template in templates:
	rules_str += osiris_rules_template.format(template=template, set=setid)

output_str += region_template.format(rules=rules_str.strip()).strip()

import pyperclip
pyperclip.copy(output_str)