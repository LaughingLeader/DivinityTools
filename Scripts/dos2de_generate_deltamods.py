from typing import List, Dict
import os
from pathlib import Path
import glob
import dos2de_common as Common

deltamods = {
    "Weapon": [
        "_LLENEMY_Boost_Weapon_Damage_Shadow_Small",
        "_LLENEMY_Boost_Weapon_Damage_Shadow_Medium",
        "_LLENEMY_Boost_Weapon_Damage_Shadow_Large",
    ],
    "Shield": [
        "_LLENEMY_Boost_Shield_Reflect_As_Shadow_Damage",
        "_LLENEMY_Boost_Shield_Reflect_As_Shadow_Damage_Medium",
        "_LLENEMY_Boost_Shield_Reflect_As_Shadow_Damage_Large",
    ],
    "Armor": [
        "_Boost_Armor_Amulet_Ability_Sneaking",
        "_Boost_Armor_Amulet_Ability_Sneaking_Medium",
        "_Boost_Armor_Amulet_Ability_Sneaking_Large",
        "_Boost_Armor_Amulet_Ability_Lockpicking",
        "_Boost_Armor_Amulet_Ability_Lockpicking_Medium",
        "_Boost_Armor_Amulet_Ability_Lockpicking_Large",
        "_LLENEMY_Boost_Armor_PhysicalResistance",
        "_LLENEMY_Boost_Armor_PhysicalResistance_Medium",
        "_LLENEMY_Boost_Armor_PhysicalResistance_Large",
    ]
}

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

deltamod_template = """
new deltamod "{deltaName}"
param "BoostType" "ItemCombo"
param "Frequency" "1"
param "ModifierType" "{statType}"
new boost "{boost}",1
"""
deltamods_output = ""

lua_template = """
table.insert(EnemyUpgradeOverhaul.{table}.{statType}, ItemBoost:Create("{deltaName}", {{MinLevel={minLevel}, Chance={chance}}}))"""

lua_output = ""

for statType,boosts in deltamods.items():
	#boosts.sort()
	for stat in boosts:
		deltamods_output = deltamods_output + deltamod_template.format(deltaName=stat[1:], statType=statType,boost=stat)

		chance = 100
		minLevel = 1
		if "Medium" in stat:
			minLevel = 6
			chance = 30
		if "Large" in stat:
			minLevel = 10
			chance = 15

		if "Negative" in stat:
			lua_output = lua_output + lua_template.format(deltaName=stat[1:], statType=statType,table="NegativeCorruptionBoosts",minLevel=minLevel,chance=chance)
		else:
			#lua_output = lua_output + lua_template.format(deltaName=stat[1:], statType=statType,table="CorruptionBoosts",minLevel=minLevel)
			pass

Common.export_file(Path("Generated_EnemyUpgradeOverhaul").joinpath("LLENEMY_Deltamods_AllDeltamods.txt"), deltamods_output.strip())
Common.export_file(Path("Generated_EnemyUpgradeOverhaul").joinpath("LLENEMY_Deltamods.lua"), lua_output.strip())

# Negative boosts apparently don't work :(
def CreateNegativeDeltamods():
	template_negative_resistance = """
	new entry "_LLENEMY_Boost_Armor_Negative{stat}Resistance{statName}"
	type "Armor"
	using "_BOOSTS_Armor"
	data "Value" "{gold}"
	data "{stat}" "-{val}"
	"""

	resistances = [
		"Fire",
		"Air",
		"Water",
		"Earth",
		"Poison",
		"Piercing",
		"Physical",
	]

	statNameMod = {
		0: "",
		1: "_Medium",
		2: "_Large",
	}

	stats_output = ""
	for stat in resistances:
		for i in range(0,3):
			goldValue = 12 + (i * 4)
			statValue = 10 + (i * 5)
			stats_output = stats_output + template_negative_resistance.format(stat=stat,gold=goldValue,val=statValue,statName=statNameMod[i])
			deltamods["Armor"].append("_LLENEMY_Boost_Armor_Negative{stat}Resistance{statName}".format(stat=stat,statName=statNameMod[i]))

	template_negative_weapon = """
	new entry "_LLENEMY_Boost_Weapon_Negative{stat}{statName}"
	type "Weapon"
	using "_BOOSTS_Weapon"
	data "Value" "{gold}"
	data "{stat}" "-{val}"
	"""

	weapon_stats = [
		"AccuracyBoost",
		"CriticalChance",
		"Initiative",
		"DodgeBoost",
	]

	for stat in weapon_stats:
		for i in range(0,3):
			goldValue = 6 + (i * 4)
			statValue = 2 + (i * 4)
			stats_output = stats_output + template_negative_weapon.format(stat=stat,gold=goldValue,val=statValue,statName=statNameMod[i])
			deltamods["Weapon"].append("_LLENEMY_Boost_Weapon_Negative{stat}{statName}".format(stat=stat,statName=statNameMod[i]))


	template_negative_shield = """
	new entry "_LLENEMY_Boost_Shield_Negative{stat}{statName}"
	type "Shield"
	using "_BOOSTS_Shield"
	data "Value" "{gold}"
	data "{stat}" "-{val}"
	"""

	shield_stats = [
		"Blocking",
		"Movement",
		"Initiative",
		"DodgeBoost",
	]

	for stat in shield_stats:
		for i in range(0,3):
			goldValue = 6 + (i * 4)
			statValue = 2 + (i * 4)
			stats_output = stats_output + template_negative_shield.format(stat=stat,gold=goldValue,val=statValue,statName=statNameMod[i])
			deltamods["Shield"].append("_LLENEMY_Boost_Shield_Negative{stat}{statName}".format(stat=stat,statName=statNameMod[i]))
	
	Common.export_file(Path("Generated_EnemyUpgradeOverhaul").joinpath("LLENEMY_Deltamods_NegativeBoosts.txt"), stats_output.strip())