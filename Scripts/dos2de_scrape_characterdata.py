from bs4 import BeautifulSoup
import os
from pathlib import Path
import glob
import dos2de_common as Common

file_top = "UUID\tName\tAlignment\tDefault State\tIsBoss\tTags\n"
data_template = '{id}\t{name}\t{alignment}\t{default_state}\t{boss}\t{tags}\n'
entry_template = 'LLENEMY_Elites_AddUpgradeChance("{level}", {id});\n'
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
		self.tags = []
		self.alignment = ""
		self.defaultdialog = ""
		self.default_state = 0

	def parse(self, xmlobj):
		default_state = get_attribute(xmlobj, "DefaultState")
		is_boss = get_attribute(xmlobj, "IsBoss")
		display_name = get_attribute(xmlobj, "DisplayName")

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

		if self.defaultdialog != "":
			print("{} has dialog {}".format(self.name, self.defaultdialog))

		tags_xml = list(xmlobj.find_all("node", attrs={"id":"Tag"}))
		for x in tags_xml:
			tag_name = get_attribute(x, "Object")
			if tag_name is not None and tag_name != "":
				self.tags.append(tag_name)

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
				for tag in template.tags:
					if not tag in self.tags:
						self.tags.append(tag)

	def export_tags(self):
		self.tags.sort(reverse=False)
		return str(self.tags).strip('[]').replace("'", "")

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
		return data_template.format(id=self.id, name=self.display_name,
			boss=self.boss,alignment=self.alignment,dialog=self.defaultdialog,
				tags=self.export_tags(),default_state=self.get_default_state())

def get_attribute(xml, id):
	v = xml.find("attribute", attrs={"id":id})
	if v is not None:
		try:
			inner = v["value"]
			return inner
		except: pass
	return ""

elite_tags = [
	"BADASSCIVILIAN",
	"NOT_MESSING_AROUND",
	"PALADIN",
	"AGGRESSIVEANIMAL",
]

def has_elite_tag(x):
	for tag in elite_tags:
		if tag in x.tags:
			return True
	return False

def export(key, level_data):
	output_str = file_top

	bosses = list([x for x in level_data if (x.boss == True or has_elite_tag(x)) and x.default_state == 0])
	for character in bosses:
		output_str += character.export()
	if output_str != "":
		output_str += '\n'
		for character in bosses:
			bonus_comment = "// {}\n".format(character.display_name)
			if character.boss:
				bonus_comment = "// Boss: {}\n".format(character.display_name)
			output_str += bonus_comment
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
