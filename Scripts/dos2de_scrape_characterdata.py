from bs4 import BeautifulSoup
import os
from pathlib import Path
import glob
import dos2de_common as Common
from typing import List, Dict

file_top = "Name\tUUID\tStats\tAlignment\tTrade Treasure\tTreasure\tTags\tIsBoss\tSkills\tDefault State\n"
data_template = '{name}\t{id}\t{stats}\t{alignment}\t{trade_treasure}\t{treasure}\t{tags}\t{boss}\t{skills}\t{default_state}\n'
entry_template = 'LLENEMY_Elites_AddUpgradeChance("{level}", {id});\n'
entry_template2 = 'LLENEMY_Elites_AddUpgradeChance("{level}", {id}, "{group}", "{type}");\n'
#file_top = "UUID\tName\tAlignment\tDialog\tDefault State\tIsBoss\tTags\n"
#data_template = '{id}\t{name}\t{alignment}\t{dialog}\t{default_state}\t{boss}\t{tags}\n'

from enum import Enum

class DefaultState(Enum):
	Idle = 0
	Dead_Physical = 1
	Dead_Piercing = 2
	Dead_Arrow = 3
	Dead_DoT = 4
	Dead_Incinerate = 5
	Dead_Acid = 6
	Dead_Electrocution = 7
	Dead_FrozenShatter = 8
	Dead_PetrifiedShatter = 9
	Dead_Explode = 10
	Dead_Surrender = 11
	Dead_Hang = 12
	Dead_KnockedDown = 13
	Dead_Lifetime = 14
	Dead_Sulfur = 15
	Sentinel = 16

class Character():
	def __init__(self):
		self.name = ""
		self.uuid = ""
		self.boss = False
		self.display_name = ""
		self.id = ""
		self.tags:List[str] = []
		self.alignment = ""
		self.defaultdialog = ""
		self.default_state = 0
		self.stats = ""
		self.trade_treasure:List[str] = []
		self.treasure:List[str] = []
		self.skills:List[str] = []

	def parse(self, xmlobj):
		default_state = get_attribute(xmlobj, "DefaultState")
		is_boss = get_attribute(xmlobj, "IsBoss")
		display_name = get_attribute(xmlobj, "DisplayName")
		try:
			handle = xmlobj.find("attribute", attrs={"id":"DisplayName"})["handle"]
			if handle in english_entries.keys():
				locale_name = english_entries[handle]
				if locale_name != "" and locale_name != None:
					display_name = locale_name
		except: pass

		self.name = get_attribute(xmlobj, "Name")
		self.uuid = get_attribute(xmlobj, "MapKey")
		self.id = "{}_{}".format(self.name, self.uuid)

		if default_state != None and default_state != "":
			try:
				self.default_state = int(default_state.strip("'"))
			except:
				print("Default State:{}".format(default_state))
				self.default_state = 0
				self.set_default_state(default_state)
		if display_name != None:
			self.display_name = display_name
		else:
			self.display_name = self.name
		self.boss = is_boss == "True"
		self.alignment = get_attribute(xmlobj, "Alignment")
		self.defaultdialog = get_attribute(xmlobj, "DefaultDialog")
		self.stats = get_attribute(xmlobj, "Stats")

		if self.defaultdialog != "":
			print("{} has dialog {}".format(self.name, self.defaultdialog))

		tags_xml = list(xmlobj.find_all("node", attrs={"id":"Tag"}))
		for x in tags_xml:
			tag_name = get_attribute(x, "Object")
			if tag_name is not None and tag_name != "" and not tag_name in self.tags:
				self.tags.append(tag_name)
		
		trade_treasure_xml = list(xmlobj.find_all("node", attrs={"id":"TradeTreasures"}))
		for x in trade_treasure_xml:
			treasure_name = get_attribute(x, "TreasureItem")
			if treasure_name is not None and treasure_name != "":
				self.trade_treasure.append(treasure_name)
		
		treasure_xml = list(xmlobj.find_all("node", attrs={"id":"Treasures"}))
		for x in treasure_xml:
			treasure_name = get_attribute(x, "TreasureItem")
			if treasure_name is not None and treasure_name != "":
				self.treasure.append(treasure_name)	
			
		skills_xml = list(xmlobj.find_all("node", attrs={"id":"Skill"}))
		for x in skills_xml:
			skill_name = get_attribute(x, "Skill")
			if skill_name is not None and skill_name != "":
				self.skills.append(skill_name)

	def copy(self, obj, prop):
		try:
			val = getattr(obj, prop)
			if val is not None:
				self_val = getattr(self, prop, "")
				if self_val == "":
					setattr(self, prop, val)
		except Exception as ex:
			print("*ERROR*: {}".format(str(ex)))

	def load_from_root(self, template_name, templates):
		if template_name in templates.keys():
			template = templates[template_name]
			if template != None:
				self.copy(template, "display_name")
				self.copy(template, "alignment")
				self.copy(template, "boss")
				self.copy(template, "stats")
				for tag in template.tags:
					if not tag in self.tags:
						self.tags.append(tag)
				if len(self.trade_treasure) == 0:
					for treasure in template.trade_treasure:
						if not treasure in self.trade_treasure:
							self.trade_treasure.append(treasure)
				if len(self.treasure) == 0:
					for treasure in template.treasure:
						if not treasure in self.treasure:
							self.treasure.append(treasure)

	def export_list(self, tbl, repl="", repl_with=""):
		tbl.sort(reverse=False)
		return str(tbl).strip('[]').replace("'", "").replace(repl, repl_with)

	def get_default_state(self):
		try:
			state = DefaultState(self.default_state)
			return state.name
		except: pass
		return "Idle"
	
	def set_default_state(self, val):
		try:
			state = DefaultState(val)
			self.default_state = state.value
		except:
			self.default_state = 0
	
	def export(self):
		treasure_export = "Empty"
		if len(self.treasure) > 0:
			treasure_export = self.export_list(self.treasure)
		trade_treasure_export = "Empty"
		if len(self.trade_treasure) > 0:
			trade_treasure_export = self.export_list(self.trade_treasure)

		if treasure_export == "Empty": treasure_export = ""
		if trade_treasure_export == "Empty": trade_treasure_export = ""

		return data_template.format(id=self.id, name=self.display_name,
			boss=self.boss,alignment=self.alignment,dialog=self.defaultdialog,stats=self.stats,
				tags=self.export_list(self.tags),skills=self.export_list(self.skills), default_state=self.get_default_state(),
					treasure=treasure_export,trade_treasure=trade_treasure_export)

def get_attribute(xml, id):
	v = xml.find("attribute", attrs={"id":id})
	if v is not None:
		try:
			inner = v["value"]
			return inner
		except: pass
	return ""

elite_tags = {
	"TUT_Tutorial_A" : [
		"BADASSCIVILIAN",
		"NOT_MESSING_AROUND",
		"PALADIN",
		#"AGGRESSIVEANIMAL",
	],
	"FJ_FortJoy_Main" : [
		"BADASSCIVILIAN",
		"NOT_MESSING_AROUND",
		"PALADIN",
	],
	"LV_HoE_Main" : [
		"BADASSCIVILIAN",
		"NOT_MESSING_AROUND"
	],
	"RC_Main" : [
		"NOT_MESSING_AROUND",
		"BLOODSPAWN",
	],
	"CoS_Main" : [
		"NOT_MESSING_AROUND",
		"Orc",
		"DEMON",
		"AUTOMATON",
	],
	"Arx_Main" : [
		"NOT_MESSING_AROUND",
		"INFERNAL_LIZARD",
		"ARX_GARDENBOSS",
	]
}

def has_elite_tag(x:Character, key:str)->bool:
	if "GHOST" in x.tags:
		return False
	if key in elite_tags.keys():
		group = elite_tags[key]
		for tag in group:
			if tag in x.tags:
				return True
	return False

def is_elite_tag(tag:str, key:str)->bool:
	if key in elite_tags.keys():
		group = elite_tags[key]
		if tag in group:
			return True
	return False

def has_elite_treasure(x:Character, key:str)->bool:
	for name in x.treasure:
		if "boss" in name.lower():
			return True
	return False

guaranteed_upgrades = {
	"S_FTJ_SW_FinalBattle_Voidwoken_7dcf3cc2-d015-4aff-9949-71fc539fcc73": [
		("Immunities", "Immunity"),
		("Bonus", "Infusion_Elite"),
		("Bonus", "Special"),
	],
	"S_GLO_Alexandar_03e6345f-1bd3-403c-80e2-a443a74f6349": [
		("Auras", "Auras_Main"),
		("Immunities", "Immunity"),
	],
	"S_GLO_Dallis_69b951dc-55a4-44b8-a2d5-5efedbd7d572": [
		("Talents", "Elite"),
		("Auras", "Auras_Main"),
	],
	"S_FTJ_GhettoBoss_84758f75-01a3-4cce-9922-f42ffc4afddd": [
		("Bonus", "Infusion_Elite"),
		("Auras", "Auras_Main"),
	],
	"S_FTJ_MagisterTorturer_1d1c0ba0-a91e-4927-af79-6d8d27e0646b": [
		("Bonus", "Infusion_Elite")
	],
	"S_FTJ_SW_Witch_4014aee0-56f1-47e0-a8eb-89c4b5a1da83": [
		("Talents", "Elite")
	],
	"S_GLO_PurgedDragon_c099caa6-1938-4b4f-9365-d0881c611e71": [
		("Immunities", "Immunity"),
		("Bonus", "Infusion_Elite"),
		("Bonus", "Special"),
	],
	"S_RC_DW_SourceLich_Stronger_2c8d84ef-bfd0-4ff7-93fe-b3728d05ee87": [
		("Immunities", "Immunity"),
		("Buffs", "Elite"),
	],
	"S_RC_BF_Ferryman_6d4270d3-2f01-4674-8668-396ac0a4c703": [
		("Immunities", "Immunity")
	],
	"S_CoS_Temples_Orc_CampBlackRing_Captain_1eceaf90-79a6-4d36-9360-975f1464b0e3": [
		("Auras", "Auras_Main")
	],
}

def export(key, level_data):
	output_str = file_top
	bosses = list([x for x in level_data if x.default_state == 0 and (x.boss == True or has_elite_tag(x, key) or has_elite_treasure(x, key))])
	bosses.sort(key=lambda x: (x.display_name.strip()), reverse=False)
	for character in bosses:
		output_str += character.export()
	if output_str != "":
		output_str += '\n'
		for character in bosses:
			elite_comment = character.export_list([x for x in character.tags if is_elite_tag(x, key)])
			if elite_comment == "":
				elite_comment = "Treasure: {}".format(character.export_list(list([x for x in character.treasure if "boss" in x.lower()])))
			else:
				elite_comment = "Tags: " + elite_comment
			bonus_comment = "// {} | {}\n".format(character.display_name, elite_comment)
			if character.boss:
				bonus_comment = "// Boss: {}\n".format(character.display_name)
			output_str += bonus_comment
			if character.id in guaranteed_upgrades.keys():
				for upgrade_group,upgrade_type in guaranteed_upgrades[character.id]:
					output_str += entry_template2.format(level=key, id=character.id, 
					group=upgrade_group, type=upgrade_type)
			else:
				output_str += entry_template.format(level=key, id=character.id)

	if output_str != "":
		output_path = script_dir.joinpath("Generated_CharacterData").joinpath("Bosses_{}.txt".format(key))
		Common.export_file(output_path, output_str)
		print("Saved boss character data to '{}'".format(output_path.name))

	output_str = file_top
	for character in level_data:
		output_str += character.export()
	output_path = script_dir.joinpath("Generated_CharacterData").joinpath("{}.txt".format(key))
	Common.export_file(output_path, output_str)
	print("Saved character data to '{}'".format(output_path.name))

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir.resolve())

english_xml_path = Path("G:/Modding/DOS2DE/Projects_Source/DivinityTools/Scripts/_Data_Characters/english.xml")
english_entries = {}

def parse_english_xml():
	f = open(english_xml_path.absolute(), 'r', encoding='utf8')
	english_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()
	content_nodes = list(english_xml.find_all("content"))
	for node in content_nodes:
		try:
			handle = node["contentuid"]
			contents = node.text
			english_entries[handle] = contents
		except Exception as e:
			print("Error parsing content node: \n{}".format(e))

parse_english_xml()

root_templates = {}
data_templates_dir = Path("G:/Modding/DOS2DE/Projects_Source/DivinityTools/Scripts/_Data_RootTemplates")
template_lsx_files = list(data_templates_dir.rglob("*.lsx"))
for p in template_lsx_files:
	print("Reading file '{}'".format(p))
	f = open(p, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	game_objects = list(lsx_xml.find_all("node", attrs={"id":"GameObjects"}))
	for obj in game_objects:
		root_type = get_attribute(obj, "Type")
		if root_type == "character":
			character = Character()
			character.parse(obj)
			root_templates[character.uuid] = character

data_dir = Path("G:/Modding/DOS2DE/Projects_Source/DivinityTools/Scripts/_Data_Characters")
lsx_files = list(data_dir.rglob("*.lsx"))
all_levels = {}

for p in lsx_files:
	level_name = p.parent.name

	if not level_name in all_levels.keys():
		all_levels[level_name] = []

	level_data = all_levels[level_name]

	lsx_path = p
	print("Reading file '{}'".format(lsx_path))
	lsx_xml = None
	f = open(lsx_path, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	lsx_name = Path(lsx_path).stem

	game_objects = list(lsx_xml.find_all("node", attrs={"id":"GameObjects"}))

	for obj in game_objects:
		root_template = get_attribute(obj, "TemplateName")
		character = Character()
		character.parse(obj)
		if root_template is not None:
			character.load_from_root(root_template, root_templates)
		level_data.append(character)

for level_name,level_data in all_levels.items():
	level_data.sort(key=lambda x: x.id, reverse=False)
	export(level_name, level_data)
