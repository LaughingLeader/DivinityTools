import sys
from bs4 import BeautifulSoup,Tag
import os
from pathlib import Path
import glob
import dos2de_common as Common
from typing import List, Dict

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir.resolve())

file_top = "Name\tRegion\tID\tUUID\tRootTemplate\tLevel\tStats\tAlignment\tTrade Treasure\tTreasure\tTags\tSkills\tScripts\tIsGlobal\tIsBoss\tDefault State\tPosition\n"
data_template = '{name}\t{region}\t{id}\t{uuid}\t{template}\t{level}\t{stats}\t{alignment}\t{trade_treasure}\t{treasure}\t{tags}\t{skills}\t{scripts}\t{isGlobal}\t{boss}\t{default_state}\t{pos}\n'
#file_top = "UUID\tName\tAlignment\tDialog\tDefault State\tIsBoss\tTags\n"
#data_template = '{id}\t{name}\t{alignment}\t{dialog}\t{default_state}\t{boss}\t{tags}\n'

from enum import Enum

def get_attribute(xml, id):
	v = xml.find("attribute", attrs={"id":id})
	if v is not None:
		try:
			inner = v["value"]
			return inner
		except: pass
	return ""

script_data:dict[str,str] = {}
script_lsx_folders = [
	Path("D:/Modding/DOS2DE_Extracted/Public/Shared/Content/Assets/Scripts"),
	Path("D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Content/Assets/Scripts"),
]
for p in script_lsx_folders:
	for script_file in p.rglob("*.lsx"):
		with script_file.open('r') as f:
			lsx_xml = BeautifulSoup(f.read(), 'lxml')
			for script_bank in lsx_xml.find_all("node", attrs={"id":"ScriptBank"}):
				script_objects = list(script_bank.find_all("node", attrs={"id":"Resource"}))
				for obj in script_objects:
					uuid = get_attribute(obj, "ID")
					name = get_attribute(obj, "Name")
					if uuid and name:
						script_data[uuid] = name

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
		self.region = ""
		self.level = 1
		self.id = ""
		self.tags:List[str] = []
		self.alignment = ""
		self.defaultdialog = ""
		self.default_state = 0
		self.stats = ""
		self.trade_treasure:List[str] = []
		self.treasure:List[str] = []
		self.skills:List[str] = []
		self.scripts:List[str] = []

	def parse(self, xmlobj:Tag, template=""):
		self.template = template
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
		self.isGlobal = get_attribute(xmlobj, "IsGlobal") == "True"
		self.stats = get_attribute(xmlobj, "Stats")
		self.region = get_attribute(xmlobj, "LevelName")
		level_override = get_attribute(xmlobj, "LevelOverride")
		if level_override:
			self.level = int(level_override)

		if self.defaultdialog != "":
			print("{} has dialog {}".format(self.name, self.defaultdialog))

		transform_node = xmlobj.find("node", attrs={"id":"Transform"})
		if transform_node:
			self.pos = get_attribute(transform_node, "Position").replace(" ", ";")

		tags_xml = list(xmlobj.find_all("node", attrs={"id":"Tag"}))
		for x in tags_xml:
			tag_name = get_attribute(x, "Object")
			if tag_name is not None and tag_name != "" and not tag_name in self.tags:
				self.tags.append(tag_name)

		scripts_xml = list(xmlobj.find_all("node", attrs={"id":"Script"}))
		for script_node in scripts_xml:
			script_uuid = get_attribute(script_node, "UUID")
			if script_uuid is not None and script_uuid != "":
				script_name = script_data.get(script_uuid, script_uuid)
				if script_name != "DefaultCharacter" and not script_name in self.scripts:
					self.scripts.append(script_name)

		
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
				self.copy(template, "level")
				for ttag in template.tags:
					if not ttag in self.tags:
						self.tags.append(ttag)
				if len(self.trade_treasure) == 0:
					for treasure in template.trade_treasure:
						if not treasure in self.trade_treasure:
							self.trade_treasure.append(treasure)
				if len(self.treasure) == 0:
					for treasure in template.treasure:
						if not treasure in self.treasure:
							self.treasure.append(treasure)
				if len(self.scripts) == 0:
					for uuid in template.scripts:
						script_name = script_data.get(uuid, uuid)
						if script_name != "DefaultCharacter" and not script_name in self.scripts:
							self.scripts.append(script_name)

	def export_list(self, tbl, empty:str="❌"):
		tbl.sort(reverse=False)
		if len(tbl) == 0:
			return empty
		return ";".join(list(sorted(tbl)))

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

		return data_template.format(
			id=self.name,
			template=self.template,
			uuid=self.uuid,
			name=self.display_name,
			boss=self.boss and "√" or "❌",
			isGlobal=self.isGlobal and "√" or "❌",
			alignment=self.alignment,
			dialog=self.defaultdialog,
			stats=self.stats,
			tags=self.export_list(self.tags, " "),
			skills=self.export_list(self.skills, " "),
			default_state=self.get_default_state(),
			treasure=treasure_export,
			trade_treasure=trade_treasure_export,
			level=self.level,
			region=self.region,
			pos=self.pos,
			scripts=self.export_list(self.scripts, " ")
		)

def export(key, level_data):
	output_str = file_top
	for character in level_data:
		output_str += character.export()
	output_path = script_dir.joinpath("Generated_CharacterData").joinpath("{}.txt".format(key))
	Common.export_file(output_path, output_str)
	print("Saved character data to '{}'".format(output_path.name))

english_xml_path = Path("D:/Modding/DOS2DE_Extracted/Localization/English/english.xml")
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
template_lsx_files = [
	Path("D:/Modding/DOS2DE_Extracted/Public/Shared/RootTemplates/_merged.lsx"),
	Path("D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/RootTemplates/_merged.lsx"),
]
for p in template_lsx_files:
	print("Reading file '{}'".format(p))
	f = open(p, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	game_objects:List[Tag]

	game_objects = list(lsx_xml.find_all("node", attrs={"id":"GameObjects"}))
	for obj in game_objects:
		root_type = get_attribute(obj, "Type")
		if root_type == "character":
			character = Character()
			character.parse(obj)
			root_templates[character.uuid] = character

character_data_folders = [
	Path("D:/Modding/DOS2DE_Extracted/Mods/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Levels/"),
	Path("D:/Modding/DOS2DE_Extracted/Mods/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Globals/"),
	Path("D:/Modding/DOS2DE_Extracted/Mods/ArmorSets/Levels/"),
	Path("D:/Modding/DOS2DE_Extracted/Mods/ArmorSets/Globals/"),
]

main_levels = [
	"TUT_Tutorial_A",
	"FJ_FortJoy_Main",
	"LV_HoE_Main",
	"LV_Topdeck_A",
	"LV_Deck-1_A",
	"LV_Deck-2_A",
	"RC_Main",
	"CoS_Main",
	"ARX_Main",
	"ARX_Endgame",
]

def get_region_order(region):
	try:
		return main_levels.index(region)
	except:
		return 999

ALL_LEVELS = False

data_dir = Path("D:/Modding/DOS2DE_Extracted/Mods/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4")
lsx_files = []
for p in character_data_folders:
	files = list(p.rglob("**/Characters/_merged.lsx"))
	lsx_files.extend(files)

all_characters:dict[str, Character] = {}

for p in lsx_files:
	level_name = p.parent.parent.name
	if not ALL_LEVELS and not level_name in main_levels:
		continue

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
		character.parse(obj, root_template)
		if root_template is not None:
			character.load_from_root(root_template, root_templates)
		all_characters[character.id] = character

output_path = script_dir.joinpath("Generated_CharacterData").joinpath("AllCharacters.tsv")

characters = list(all_characters.values())
characters.sort(key=lambda x: (get_region_order(x.region), x.display_name), reverse=False)

output_str = file_top
for character in characters:
	output_str += character.export()
Common.export_file(output_path, output_str)
print("Saved character data to '{}'".format(output_path.name))
