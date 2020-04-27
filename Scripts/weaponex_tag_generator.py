import os
import sys
from pathlib import Path
from typing import List, Dict
import dos2de_common as Common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

tags = [
	#("LLGRIMOIRE_Grimoire", "Grimoire"),
	("LLWEAPONEX_Axe", "Axe", None, "#F5785A"),
	("LLWEAPONEX_Banner", "Banner", None, "#00FF7F"),
	("LLWEAPONEX_BattleBook", "Battle Book", "a Book", "#22AADD"),
	#("LLWEAPONEX_Blunderbuss", "Blunderbuss"),
	("LLWEAPONEX_Bludgeon", "Bludgeon", None, "#FFE7AA"),
	("LLWEAPONEX_Bow", "Bow", None, "#72EE34"),
	#("LLWEAPONEX_CombatShield", "#"),
	("LLWEAPONEX_Crossbow", "Crossbow", None, "#81E500"),
	("LLWEAPONEX_Dagger", "Dagger", None, "#5B40FF"),
	("LLWEAPONEX_DualShields", "Dual Shields", "Dual Shields", "#D9D9D9"),
	("LLWEAPONEX_Firearm", "Firearm", None, "#FD8826"),
	#("LLWEAPONEX_Glaive", "Glaive", None, "#FFAA29"),
	("LLWEAPONEX_Greatbow", "Greatbow", None, "#00FF7F"),
	#("LLWEAPONEX_Halberd", "Halberd", None, "#CCFF55"),
	("LLWEAPONEX_HandCrossbow", "Hand Crossbow", None, "#FF33FF"),
	("LLWEAPONEX_Katana", "Katana", None, "#FF2D2D"),
	("LLWEAPONEX_Pistol", "Pistol", None, "#FF337F"),
	("LLWEAPONEX_Polearm", "Polearm", None, "#FFCF29"),
	("LLWEAPONEX_Quarterstaff", "Quarterstaff", None, "#FD8826"),
	("LLWEAPONEX_Rapier", "Rapier", None, "#F8FF2D"),
	#("LLWEAPONEX_Rod", "Rod", None, "#B658FF"),
	("LLWEAPONEX_Runeblade", "Runeblade", None, "#40E0D0"),
	("LLWEAPONEX_Scythe", "Scythe", None, "#AA11CC"),
	("LLWEAPONEX_Shield", "Shield", None, "#AE9F95"),
	#("LLWEAPONEX_Spear", "Spear", None, "#FFCF29"),
	("LLWEAPONEX_Staff", "Arcane Staff", "a Staff", "#2EFFE9"),
	("LLWEAPONEX_Sword", "Sword", None, "#FF3E2A"),
	#("LLWEAPONEX_Throwing", "Throwing "),
	("LLWEAPONEX_ThrowingAbility", "Throwing Ability", "Throwing Ability", "#40E0D0"),
	("LLWEAPONEX_Unarmed", "Unarmed", "Empty Hands", "#FF44FF"),
	("LLWEAPONEX_Wand", "Wand", None, "#B658FF"),
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

lua_template = """
MasteryRankTagText = {{
{tags}
}}"""
lua_entry_template = "{tag} = TranslatedString:Create(\"{handle}\",\"{content}\"),\n"

luaEntries = []

def createMasteryTags(output,handles):
	for tag,name,equippedText,color in tags:
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
				content = "<font color='{}'>{} Mastery {}</font>".format(color,name,letter)
				output += "{}\t{}\t{}\n".format(tagName, content, handle)
				luaEntries.append(lua_entry_template.format(tag=tagName, handle=handle, content=content))
	return output

createFile("WeaponExpansion_Generated/LLWEAPONEX_Tags_MasteryRanks.tsv", createMasteryTags)

allLuaEntries = ""
for entry in luaEntries:
	allLuaEntries += entry

luaOutput = lua_template.format(tags=allLuaEntries)
outputFilePath = script_dir.joinpath("WeaponExpansion_Generated/LLWEAPONEX_Tags.lua")
Common.export_file(outputFilePath, luaOutput.strip())

def createEquipmentTags(output,handles):
	for tag,name,equippedText,color in tags:
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