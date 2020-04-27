import os
import sys
from pathlib import Path
from typing import List, Dict
import dos2de_common as Common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

handles:Dict[str,str] = {}
masteries:List[Mastery] = []

class MasteryRank():
    def __init__(self, masteryName, level, color, name):
		self.level = level
		self.color = color
		self.name = name
		self.keyName = "{}Rank".format(masteryName, level)
		self.text = "<font color='#{}'>{}</font>".format(color,name)
		if self.keyName in handles.keys():
			self.handle = handles[keyName]
		else:
			self.handle = handle = Common.NewHandle()
		self.localeOutput = "{}\t{}\t{}\n".format(self.keyName, self.text, self.handle)

class Mastery():
	def __init__(self, masteryID):
		self.masteryID = masteryID
		self.ranks:Dict[int,MasteryRank] = {}
		masteries.append(self)

	def AddRank(self, level, color, name):
		self.ranks[level] = MasteryRank(self.masteryID, level, color, name)
	
	def ExportLocalization(self, output):
		masteryOutput = ""
		for level,rank in self.ranks.items():
			masteryOutput += rank.localeOutput
		output += masteryOutput.strip() + "\n"
	
	def ExportLua(self, output):
		luaOutput = "{} = {{\n".format(self.masteryID)
		for level,rank in self.ranks.items():
			luaOutput += "[{}] = TranslatedString:Create(\"{}\", \"{}\"),\n".format(level, rank.handle, rank.text)
		luaOutput += "}}\n"
		output += luaOutput.strip() + "\n"

Mastery("LLWEAPONEX_Axe")

tags = [
	("LLWEAPONEX_Axe", "Axe", None, "#F5785A"),
	("LLWEAPONEX_Banner", "Banner", None, "#00FF7F"),
	("LLWEAPONEX_BattleBook", "Battle Book", "a Book", "#22AADD"),
	("LLWEAPONEX_Bludgeon", "Bludgeon", None, "#FFE7AA"),
	("LLWEAPONEX_Bow", "Bow", None, "#72EE34"),
	("LLWEAPONEX_Crossbow", "Crossbow", None, "#81E500"),
	("LLWEAPONEX_Dagger", "Dagger", None, "#5B40FF"),
	("LLWEAPONEX_DualShields", "Dual Shields", "Dual Shields", "#D9D9D9"),
	("LLWEAPONEX_Firearm", "Firearm", None, "#FD8826"),
	("LLWEAPONEX_Greatbow", "Greatbow", None, "#00FF7F"),
	("LLWEAPONEX_HandCrossbow", "Hand Crossbow", None, "#FF33FF"),
	("LLWEAPONEX_Katana", "Katana", None, "#FF2D2D"),
	("LLWEAPONEX_Pistol", "Pistol", None, "#FF337F"),
	("LLWEAPONEX_Polearm", "Polearm", None, "#FFCF29"),
	("LLWEAPONEX_Quarterstaff", "Quarterstaff", None, "#FD8826"),
	("LLWEAPONEX_Rapier", "Rapier", None, "#F8FF2D"),
	("LLWEAPONEX_Runeblade", "Runeblade", None, "#40E0D0"),
	("LLWEAPONEX_Scythe", "Scythe", None, "#AA11CC"),
	("LLWEAPONEX_Shield", "Shield", None, "#AE9F95"),
	("LLWEAPONEX_Staff", "Arcane Staff", "a Staff", "#2EFFE9"),
	("LLWEAPONEX_Sword", "Sword", None, "#FF3E2A"),
	("LLWEAPONEX_ThrowingAbility", "Throwing Ability", "Throwing Ability", "#40E0D0"),
	("LLWEAPONEX_Unarmed", "Unarmed", "Empty Hands", "#FF44FF"),
	("LLWEAPONEX_Wand", "Wand", None, "#B658FF"),
]