import os
import sys
from pathlib import Path
from typing import List, Dict
import dos2de_common as Common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

tags = [
	#("LLGRIMOIRE_Grimoire", "Grimoire"),
	("LLWEAPONEX_Axe", "Axe", None),
	("LLWEAPONEX_Banner", "Banner", None),
	("LLWEAPONEX_BattleBook", "Battle Book", "a Book"),
	#("LLWEAPONEX_Blunderbuss", "Blunderbuss"),
	("LLWEAPONEX_Blunt", "Blunt Weapon", None),
	("LLWEAPONEX_Bow", "Bow", None),
	#("LLWEAPONEX_CombatShield", ""),
	("LLWEAPONEX_Crossbow", "Crossbow", None),
	("LLWEAPONEX_Dagger", "Dagger", None),
	("LLWEAPONEX_DualShields", "Dual Shields", "Dual Shields"),
	("LLWEAPONEX_Firearm", "Firearm", None),
	("LLWEAPONEX_Glaive", "Glaive", None),
	("LLWEAPONEX_Greatbow", "Greatbow", None),
	("LLWEAPONEX_Halberd", "Halberd", None),
	("LLWEAPONEX_HandCrossbow", "Hand Crossbow", None),
	("LLWEAPONEX_Katana", "Katana", None),
	("LLWEAPONEX_Pistol", "Pistol", None),
	("LLWEAPONEX_Polearm", "Polearm", None),
	("LLWEAPONEX_Quarterstaff", "Quarterstaff", None),
	("LLWEAPONEX_Rapier", "Rapier", None),
	("LLWEAPONEX_Rod", "Rod", None),
	("LLWEAPONEX_Runeblade", "Runeblade", None),
	("LLWEAPONEX_Scythe", "Scythe", None),
	("LLWEAPONEX_Shield", "Shield", None),
	("LLWEAPONEX_Spear", "Spear", None),
	("LLWEAPONEX_Staff", "Arcane Staff", "a Staff"),
	("LLWEAPONEX_Sword", "Sword", None),
	#("LLWEAPONEX_Throwing", "Throwing "),
	("LLWEAPONEX_ThrowingAbility", "Throwing Ability", "Throwing Ability"),
	("LLWEAPONEX_Unarmed", "Unarmed", "Empty Hands"),
	("LLWEAPONEX_Wand", "Wand", None),
]

def getValueLetter(i):
	if i == 1:
		return "I"
	elif i == 2:
		return "II"
	elif i == 3:
		return "III"
	elif i == 4:
		return "IV"
	elif i == 5:
		return "V"
	return None

def createFile(outputFile:str, entryFunc):
	handles:Dict[str,str] = {}

	outputFilePath = script_dir.joinpath(outputFile)
	if outputFilePath.exists():
		tsv = open(outputFilePath, 'r')
		lines = tsv.readlines()
		tsv.close()
		lines.pop(0)
		for line in lines:
			entry = tuple(line.strip().split("\t"))
			if entry is not None and len(entry) >= 2:
				handle = entry[2]
				handles[entry[0]] = entry[2]

	output = entryFunc("Key\tContent\tHandle\n", handles)
	Common.export_file(outputFilePath, output.strip())

def createMasteryTags(output,handles):
	for tag,name,equippedText in tags:
		for i in range(5):
			rank = i + 1
			letter = getValueLetter(rank)
			if letter is not None:
				tagName = "{}_Mastery{}".format(tag,rank)
				handle = ""
				if tagName in handles.keys():
					handle = handles[tagName]
				else:
					handle = handle = Common.NewHandle()
				output += "{}\t{} {}\t{}\n".format(tagName, name + " Mastery", letter, handle)
	return output

createFile("WeaponExpansion_Generated/LLWEAPONEX_Tags_MasteryRanks.tsv", createMasteryTags)

def createEquipmentTags(output,handles):
	for tag,name,equippedText in tags:
		tagName = "{}_Equipped".format(tag)
		handle = ""
		if tagName in handles.keys():
			handle = handles[tagName]
		else:
			handle = handle = Common.NewHandle()
		if equippedText is None:
			equippedText = "a " + name
		output += "{}\t{}\t{}\n".format(tagName, equippedText, handle)
	return output
createFile("WeaponExpansion_Generated/LLWEAPONEX_Tags_WeaponRequirement.tsv", createEquipmentTags)

# output = "Key\tContent\tHandle\n"
# for tag,name in tags:
# 	for i in range(5):
# 		rank = i + 1
# 		letter = getValueLetter(rank)
# 		if letter is not None:
# 			tagName = "{}_Mastery{}".format(tag,rank)
# 			handle = Common.NewHandle()
# 			output += "{}\t{} {}\t{}\n".format(tagName, name, letter, handle)
# Common.export_file(script_dir.joinpath("WeaponExpansion_Generated/LLWEAPONEX_Tags_EquippedWeapons.tsv"), output.strip())