import os
import sys
from pathlib import Path
from typing import List, Dict
import dos2de_common as Common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

handles:Dict[str,str] = {}
masteries = {}

tsvPath = Path("G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/WeaponExpansion/LocalKeys/LLWEAPONEX_Masteries_Names.tsv")
luaPath = Path("G:/Divinity Original Sin 2/DefEd/Data/Mods/WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f/Story/RawFiles/Lua/Shared/Data/MasteryData_Masteries.lua")

class MasteryRank():
    def __init__(self, masteryName, level, color, name):
        global handles
        self.level = level
        self.color = color
        self.name = name
        self.keyName = "{}_Rank{}_DisplayName".format(masteryName, level)
        #self.text = "<font color='{}'>{}</font>".format(self.color,self.name)
        self.text = self.name
        if self.keyName in handles.keys():
            self.handle = handles[self.keyName]
        else:
            self.handle = Common.NewHandle()
            handles[self.keyName] = self.handle
        self.localeOutput = "{}\t{}\t{}\n".format(self.keyName, self.text, self.handle)
        self.luaOutput = "\t[{}] = {{Name = TranslatedString:Create(\"{}\", \"{}\"), Color=\"{}\"}},\n".format(self.level, self.handle, self.text, self.color)

class Mastery():
    def __init__(self, masteryID, name, color, requirementText=None):
        global masteries
        global handles
        self.masteryID = masteryID
        self.name = name
        self.color = color
        self.ranks:Dict[int,MasteryRank] = {}
        if self.masteryID in handles.keys():
            self.handle = handles[masteryID]
        else:
            self.handle = Common.NewHandle()
            handles[self.masteryID] = self.handle
        self.localizedName = self.name#"<font color='{}'>{}</font>".format(self.color, self.name)
        self.requirementText = requirementText
        masteries[masteryID] = self

    def AddRank(self, level, color, name):
        self.ranks[level] = MasteryRank(self.masteryID, level, color, name)
    
    def ExportLocalization(self):
        masteryOutput = "{id}\t{name}\t{handle}\n".format(id=self.masteryID, name=self.localizedName, handle=self.handle)
        for level,rank in self.ranks.items():
            masteryOutput += rank.localeOutput
        return masteryOutput.strip() + "\n"
    
    def ExportLua(self):
        luaOutput = "[\"{id}\"] = MasteryData:Create(\"{id}\", TranslatedString:Create(\"{handle}\", \"{name}\"), \"{color}\", {{\n".format(id=self.masteryID, name=self.localizedName, color=self.color, handle=self.handle)
        for level,rank in self.ranks.items():
            luaOutput += rank.luaOutput
        luaOutput += "}),\n"
        return luaOutput.strip() + "\n"

def AddRank(masteryID, level, color, name):
    if masteryID in masteries.keys():
        mastery = masteries[masteryID]
        mastery.ranks[level] = MasteryRank(masteryID, level, color, name)
    else:
        print("No mastery for: {}".format(masteryID))

def GetHandles(outputFile:str):
    global handles
    if type(outputFile) == str:
        outputFilePath = Path(outputFile)
    else:
        outputFilePath = outputFile

    if outputFilePath.exists():
        tsv = open(outputFilePath, 'r')
        lines = tsv.readlines()
        tsv.close()
        lines.pop(0)
        for line in lines:
            entry = tuple(line.strip().split("\t"))
            if entry is not None and len(entry) >= 2:
                handle = entry[2]
                if handle is not None:
                    handles[entry[0]] = entry[2]

GetHandles(tsvPath)

Mastery("LLWEAPONEX_Axe", "Axe", "#F5785A")
Mastery("LLWEAPONEX_Banner", "Banner", "#F8FF2D")
Mastery("LLWEAPONEX_BattleBook", "Battle Book", "#22AADD", "a Book")
Mastery("LLWEAPONEX_Bludgeon", "Bludgeon", "#FFE7AA")
Mastery("LLWEAPONEX_Bow", "Bow", "#72EE34")
Mastery("LLWEAPONEX_Crossbow", "Crossbow", "#81E500")
Mastery("LLWEAPONEX_Dagger", "Dagger", "#5B40FF")
Mastery("LLWEAPONEX_DualShields", "Dual Shields", "#D9D9D9", "Dual Shields")
Mastery("LLWEAPONEX_Firearm", "Firearm", "#FD8826")
Mastery("LLWEAPONEX_Greatbow", "Greatbow", "#00FF7F")
Mastery("LLWEAPONEX_HandCrossbow", "Hand Crossbow", "#FF33FF")
Mastery("LLWEAPONEX_Katana", "Katana", "#FF2D2D")
Mastery("LLWEAPONEX_Pistol", "Pistol", "#FF337F")
Mastery("LLWEAPONEX_Polearm", "Polearm", "#FFCF29")
Mastery("LLWEAPONEX_Quarterstaff", "Quarterstaff", "#FD8826")
Mastery("LLWEAPONEX_Rapier", "Rapier", "#00FF7F")
Mastery("LLWEAPONEX_Runeblade", "Runeblade", "#40E0D0")
Mastery("LLWEAPONEX_Scythe", "Scythe", "#AA11CC")
Mastery("LLWEAPONEX_Shield", "Shield", "#AE9F95")
Mastery("LLWEAPONEX_Staff", "Staff", "#2EFFE9", "a Staff")
Mastery("LLWEAPONEX_Sword", "Sword", "#FF3E2A")
Mastery("LLWEAPONEX_ThrowingAbility", "Throwing", "#40E0D0", "Throwing Ability")
Mastery("LLWEAPONEX_Unarmed", "Unarmed", "#FF44FF", "Empty Hands")
Mastery("LLWEAPONEX_Wand", "Wand", "#B658FF")

AddRank("LLWEAPONEX_Axe", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Axe", 1, "#FFAAAA", "Novice")
AddRank("LLWEAPONEX_Axe", 2, "#D46A6A", "Journeyman Axefighter")
AddRank("LLWEAPONEX_Axe", 3, "#DD3939", "Expert Axefighter")
AddRank("LLWEAPONEX_Axe", 4, "#FF1515", "Warmaster, Axe of Legend")
AddRank("LLWEAPONEX_Banner", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Banner", 1, "#DDFFB3", "Novice")
AddRank("LLWEAPONEX_Banner", 2, "#94E963", "Journeyman Bannerman")
AddRank("LLWEAPONEX_Banner", 3, "#52D43A", "Expert Bannerkeeper")
AddRank("LLWEAPONEX_Banner", 4, "#28FF00", "Banner Lord")
AddRank("LLWEAPONEX_BattleBook", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_BattleBook", 1, "#DDFFB3", "Novice")
AddRank("LLWEAPONEX_BattleBook", 2, "#94E9FF", "Journeyman Bookkeeper")
AddRank("LLWEAPONEX_BattleBook", 3, "#52D4FF", "Expert Bookkeeper")
AddRank("LLWEAPONEX_BattleBook", 4, "#28FFFF", "Pagemaster")
AddRank("LLWEAPONEX_Bludgeon", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Bludgeon", 1, "#FFE7AA", "Novice")
AddRank("LLWEAPONEX_Bludgeon", 2, "#D4B76A", "Journeyman Smasher")
AddRank("LLWEAPONEX_Bludgeon", 3, "#AA8B39", "Expert Smasher")
AddRank("LLWEAPONEX_Bludgeon", 4, "#A57C5B", "Master of Smashing")
AddRank("LLWEAPONEX_Bow", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Bow", 1, "#CAEA9C", "Novice")
AddRank("LLWEAPONEX_Bow", 2, "#9BC362", "Journeyman Archer")
AddRank("LLWEAPONEX_Bow", 3, "#AAFF14", "Expert Archer")
AddRank("LLWEAPONEX_Bow", 4, "#4DFF14", "Eagle Eye, Master Archer")
AddRank("LLWEAPONEX_Crossbow", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Crossbow", 1, "#B5D48D", "Novice")
AddRank("LLWEAPONEX_Crossbow", 2, "#A6D569", "Journeyman Crossbowman")
AddRank("LLWEAPONEX_Crossbow", 3, "#95D83F", "Expert Crossbowman")
AddRank("LLWEAPONEX_Crossbow", 4, "#88E213", "Master Marksman of Crossbows")
AddRank("LLWEAPONEX_Dagger", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Dagger", 1, "#CDBCF0", "Novice")
AddRank("LLWEAPONEX_Dagger", 2, "#A17EE8", "Journeyman Thief")
AddRank("LLWEAPONEX_Dagger", 3, "#8756EB", "Expert Rogue")
AddRank("LLWEAPONEX_Dagger", 4, "#6827EC", "Master Shadowdancer")
AddRank("LLWEAPONEX_DualShields", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_DualShields", 1, "#FFDA9E", "Novice")
AddRank("LLWEAPONEX_DualShields", 2, "#FFC973", "Journeyman Dual Shieldsman")
AddRank("LLWEAPONEX_DualShields", 3, "#FFB94A", "Expert Dual Shieldsman")
AddRank("LLWEAPONEX_DualShields", 4, "#FF9E03", "Dual Shieldmaster")
AddRank("LLWEAPONEX_Firearm", 0, "#FDC89B", "Beginner")
AddRank("LLWEAPONEX_Firearm", 1, "#FBBC7F", "Novice")
AddRank("LLWEAPONEX_Firearm", 2, "#F5A36C", "Journeyman Firearm Enthusiast")
AddRank("LLWEAPONEX_Firearm", 3, "#F49C4E", "Expert Firearm Lunatic")
AddRank("LLWEAPONEX_Firearm", 4, "#FF9D33", "Master of Firearms")
AddRank("LLWEAPONEX_Greatbow", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Greatbow", 1, "#DDFFB3", "Novice")
AddRank("LLWEAPONEX_Greatbow", 2, "#94E963", "Journeyman Slayer")
AddRank("LLWEAPONEX_Greatbow", 3, "#52D43A", "Expert Slayer")
AddRank("LLWEAPONEX_Greatbow", 4, "#28FF00", "Master Dragonslayer")
AddRank("LLWEAPONEX_HandCrossbow", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_HandCrossbow", 1, "#FFDA9E", "Novice")
AddRank("LLWEAPONEX_HandCrossbow", 2, "#FFC973", "Journeyman Spy")
AddRank("LLWEAPONEX_HandCrossbow", 3, "#FFB94A", "Expert Spy")
AddRank("LLWEAPONEX_HandCrossbow", 4, "#FF9E03", "Spymaster, Elite Assassin")
AddRank("LLWEAPONEX_Katana", 0, "#FFEAEA", "Beginner")
AddRank("LLWEAPONEX_Katana", 1, "#FF9D9D", "Novice")
AddRank("LLWEAPONEX_Katana", 2, "#F56C6C", "Journeyman Bladesman")
AddRank("LLWEAPONEX_Katana", 3, "#F44E4E", "Expert Blademaster")
AddRank("LLWEAPONEX_Katana", 4, "#FF3333", "Blademaster")
AddRank("LLWEAPONEX_Pistol", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Pistol", 1, "#DDFFB3", "Novice")
AddRank("LLWEAPONEX_Pistol", 2, "#94E963", "Journeyman Gunslinger")
AddRank("LLWEAPONEX_Pistol", 3, "#52D43A", "Expert Gunslinger")
AddRank("LLWEAPONEX_Pistol", 4, "#4CFF00", "Master Gunslinger")
AddRank("LLWEAPONEX_Quarterstaff", 0, "#FDC89B", "Beginner")
AddRank("LLWEAPONEX_Quarterstaff", 1, "#FBBC7F", "Novice")
AddRank("LLWEAPONEX_Quarterstaff", 2, "#F5A36C", "Journeyman Staff Monk")
AddRank("LLWEAPONEX_Quarterstaff", 3, "#F49C4E", "Expert Staff Monk")
AddRank("LLWEAPONEX_Quarterstaff", 4, "#FF9D33", "Master Monk of Staves")
AddRank("LLWEAPONEX_Rapier", 0, "#FEFFEA", "Beginner")
AddRank("LLWEAPONEX_Rapier", 1, "#FFF59D", "Novice")
AddRank("LLWEAPONEX_Rapier", 2, "#F5F06C", "Journeyman Fencer")
AddRank("LLWEAPONEX_Rapier", 3, "#F5E06C", "Expert Fencer")
AddRank("LLWEAPONEX_Rapier", 4, "#FFE933", "Master Fencer")
AddRank("LLWEAPONEX_Runeblade", 0, "#EAFFFE", "Beginner")
AddRank("LLWEAPONEX_Runeblade", 1, "#9DFCFF", "Novice")
AddRank("LLWEAPONEX_Runeblade", 2, "#6CE3F5", "Journeyman Runekeeper")
AddRank("LLWEAPONEX_Runeblade", 3, "#6CF5E9", "Expert Runekeeper")
AddRank("LLWEAPONEX_Runeblade", 4, "#33FFB8", "Runemaster")
AddRank("LLWEAPONEX_Polearm", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Polearm", 1, "#FFF2C6", "Novice")
AddRank("LLWEAPONEX_Polearm", 2, "#FFE899", "Journeyman Polearmsman")
AddRank("LLWEAPONEX_Polearm", 3, "#FFE178", "Expert Polearmsman")
AddRank("LLWEAPONEX_Polearm", 4, "#FFC154", "Polearm Master")
AddRank("LLWEAPONEX_Scythe", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Scythe", 1, "#CCDA9E", "Novice")
AddRank("LLWEAPONEX_Scythe", 2, "#C8FBFF", "Journeyman Reaper")
AddRank("LLWEAPONEX_Scythe", 3, "#96F8FF", "Expert Reaper")
AddRank("LLWEAPONEX_Scythe", 4, "#73FFCC", "Reaper of Souls")
AddRank("LLWEAPONEX_Shield", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Shield", 1, "#CCDA9E", "Novice")
AddRank("LLWEAPONEX_Shield", 2, "#CCC973", "Journeyman Shieldsman")
AddRank("LLWEAPONEX_Shield", 3, "#CCB94A", "Expert Shieldsman")
AddRank("LLWEAPONEX_Shield", 4, "#CC9E03", "Shieldmaster")
AddRank("LLWEAPONEX_Staff", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Staff", 1, "#D1F8FF", "Novice")
AddRank("LLWEAPONEX_Staff", 2, "#9BF0FF", "Journeyman Staff Acolyte")
AddRank("LLWEAPONEX_Staff", 3, "#77E9FE", "Expert Staffmeister")
AddRank("LLWEAPONEX_Staff", 4, "#5EDBFF", "Sage of Staves")
AddRank("LLWEAPONEX_Sword", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Sword", 1, "#FFAC99", "Novice")
AddRank("LLWEAPONEX_Sword", 2, "#FF9178", "Journeyman Swordsman")
AddRank("LLWEAPONEX_Sword", 3, "#FF7251", "Expert Swordsman")
AddRank("LLWEAPONEX_Sword", 4, "#FF662A", "Swordmaster")
AddRank("LLWEAPONEX_ThrowingAbility", 0, "#FFEAEA", "Beginner")
AddRank("LLWEAPONEX_ThrowingAbility", 1, "#FF9D9D", "Novice")
AddRank("LLWEAPONEX_ThrowingAbility", 2, "#F56CA3", "Journeyman Thrower")
AddRank("LLWEAPONEX_ThrowingAbility", 3, "#F56C8C", "Expert Thrower")
AddRank("LLWEAPONEX_ThrowingAbility", 4, "#FF3376", "Master Thrower")
AddRank("LLWEAPONEX_Unarmed", 0, "#EAFFFE", "Beginner")
AddRank("LLWEAPONEX_Unarmed", 1, "#9DFCFF", "Novice")
AddRank("LLWEAPONEX_Unarmed", 2, "#6CE3F5", "Scrapper")
AddRank("LLWEAPONEX_Unarmed", 3, "#6CF5E9", "Elite Brawler")
AddRank("LLWEAPONEX_Unarmed", 4, "#33FFB8", "Master Pugilist")
AddRank("LLWEAPONEX_Wand", 0, "#FDFFEA", "Beginner")
AddRank("LLWEAPONEX_Wand", 1, "#D8BAFD", "Novice")
AddRank("LLWEAPONEX_Wand", 2, "#C596FE", "Journeyman of Wands")
AddRank("LLWEAPONEX_Wand", 3, "#B274FF", "Expert of Wands")
AddRank("LLWEAPONEX_Wand", 4, "#D258FF", "Master Wandweaver")

tsvOutput = "Key\tContent\tHandle\nLLWEAPONEX_Mastery\tMastery\thd84bd8c4gb25fg46bagbbf9ga3d43b8bfacc\n"
luaOutput = """
---@class TranslatedString
local TranslatedString = LeaderLib.Classes["TranslatedString"]

WeaponExpansion.Masteries = {\n"""
for masteryName,mastery in masteries.items():
    tsvOutput += mastery.ExportLocalization()
    luaOutput += mastery.ExportLua()
luaOutput += "}"
Common.export_file(tsvPath, tsvOutput.strip())
Common.export_file(luaPath, luaOutput.strip())