import os
from pathlib import Path
import dos2de_common as common
import re
check_file_names = [
	"Character",
	#"Data",
	"Object",
	"Potion",
	# "Requirements",
	"Shield",
	"Skill_Cone",
	"Skill_Dome",
	"Skill_Jump",
	"Skill_Projectile",
	"Skill_ProjectileStrike",
	"Skill_Rain",
	"Skill_Rush",
	"Skill_Shout",
	"Skill_Summon",
	"Skill_Target",
	"Skill_Teleportation",
	"Skill_Tornado",
	"Status_CONSUME",
	"Status_DAMAGE",
	"Status_DAMAGE_ON_MOVE",
	"Status_DISARMED",
	"Status_FEAR",
	"Status_HEAL",
	"Status_HEALING",
	"Status_INCAPACITATED",
	"Status_KNOCKED_DOWN",
	"Status_MUTED",
	"Status_PLAY_DEAD",
	"Status_POLYMORPHED",
	"Weapon"
]

ignore_props = [
	("StatsDescriptionRef", "StatsDescription"),
]

redirect_props = [
	("DisplayNameRef", "DisplayName"),
	("DescriptionRef", "Description"),
]

FORBIDDEN = [
	"SkillProperties",
	"ExtraProperties",
	"Requirements",
	"MemorizationRequirements",
	"Flags",
	"TargetConditions",
	"AoEConditions",
	"CycleConditions",
	"ComboCategories",
]

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

modifiers_path = Path("D:\Modding\DOS2DE_Extracted\Public\Shared\Stats\Generated\Structure\Modifiers.txt")
modifiers = {}

class Modifier():
	def __init__(self, name, value):
		self.name = name
		self.value = value

class ModifierType():
	def __init__(self, name, export_type):
		self.name = name
		self.export_type = export_type
		self.modifiers = {}

def get_modifier(stattype, propname, subtype=""):
	for modtype in modifiers.values():
		#print("{} | {}".format(modtype.export_type, stattype))
		if modtype.export_type == stattype:
			if stattype == "SkillData" or stattype == "StatusData":
				
				if modtype.name == subtype:
					for mod in modtype.modifiers.values():
						if mod.name == propname:
							return mod.value
			else:
				for mod in modtype.modifiers.values():
					if mod.name == propname:
						return mod.value
		elif modtype.name == stattype:
			for mod in modtype.modifiers.values():
				if mod.name == propname:
					return mod.value
	return None

def get_attribute(node, id, fallback):
	try:
		return node[id]
	except: pass
	return fallback

statobdefinitins_path = Path("G:\Divinity Original Sin 2\DefEd\Data\Editor\Config\Stats\StatObjectDefinitions.sod")
from bs4 import BeautifulSoup
def build_statdefinitions(file_path, debug=False):
	print("Reading file '{}'".format(file_path))
	f = open(file_path, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	obj_definitions = list(lsx_xml.find_all("stat_object_definition"))
	for node in obj_definitions:
		mod_type_name = node["name"]
		mod_export_type = get_attribute(node, "export_type", mod_type_name)
		if debug: print("Parsing modifier type {}".format(mod_type_name))
		modifier_type = ModifierType(mod_type_name, mod_export_type)
		modifiers[mod_type_name] = modifier_type
		field_definitions = list(node.find_all("field_definition"))
		for defnode in field_definitions:
			#<field_definition name="Strength" display_name="Strength" export_name="Strength" type="Enumeration" enumeration_type_name="PreciseQualifier" description="Enter a value in [0,10] range. Code will turn it into level-appropriate amount of attribute. 10 is roughly the amount that a dedicated player can gather at that level." />
			def_name = defnode["export_name"]
			def_type = defnode["type"]
			mod = Modifier(def_name, def_type)
			modifier_type.modifiers[def_name] = mod
			if debug: print("---- Found modifier {} with value {}".format(def_name, def_type))

	print("Modifier types: {}".format("\n".join(modifiers.keys())))

regex_modifier_type = re.compile('^.*?modifier\s+type\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)
regex_modifier_data = re.compile('^.*?modifier\s*?\"(.*?)\"\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)

def build_modifiers(file_path, debug=True):
	print("Reading file '{}'".format(file_path))
	f = open(file_path, 'r')
	modifierlines = f.readlines()
	f.close()

	current_modifier_type = None

	for line in modifierlines:
		if line != "":
			if current_modifier_type is not None:
				data_match = regex_modifier_data.match(line)
				if data_match is not None:
					prop_name = data_match.group(1)
					prop_val = data_match.group(2)
					modifier = Modifier(prop_name, prop_val)
					current_modifier_type.modifiers[prop_name] = modifier
					if debug: print("---- Found modifier {} with value {}".format(prop_name, prop_val))
				else:
					if current_stat.type == "":
						type_match = regex_entry_type.match(line)
						if type_match is not None:
							current_stat.type = type_match.group(1)
					elif current_stat.parent == "":
						using_match = regex_entry_using.match(line)
						if using_match is not None:
							current_stat.parent = using_match.group(1)
			match = regex_modifier_type.match(line)
			if match is not None:
				type_name = match.group(1)
				if type_name is not None and type_name != "":
					current_modifier_type = ModifierType(type_name)
					modifiers[type_name] = current_modifier_type
					if debug: print("Parsing modifier type {}".format(type_name))

build_statdefinitions(statobdefinitins_path)
#build_modifiers(modifiers_path)

data_folder = Path("D:\Modding\DOS2DE_Extracted\Public\Shared\Stats\Generated\Data")
origins_folder = Path("D:\Modding\DOS2DE_Extracted\Public\DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4\Stats\Generated\Data")
mod_folder = Path("G:\Divinity Original Sin 2\DefEd\Data\Public\Kalavinkas_Combat_Enhanced_e844229e-b744-4294-9102-a7362a926f71\Stats\Generated\Data")

all_game_files = list(data_folder.glob("*.txt"))
all_origins_files = list(origins_folder.glob("*.txt"))
all_mod_files = list(mod_folder.glob("*.txt"))

game_files = [x for x in all_game_files if Path(x).stem in check_file_names]
origins_files = [x for x in all_origins_files if Path(x).stem in check_file_names]
mod_files = [x for x in all_mod_files if Path(x).stem in check_file_names]

class StatProperty():
	def __init__(self, parent, name, value):
		self.name = name
		self.value = value
		self.is_override = False
		self.parent = parent

class StatEntry():
	def __init__(self, file, name):
		self.file = file
		self.name = name
		self.properties = {}
		self.type = ""
		self.parent = ""
		self.overrides = []
		self.lines = []

class StatFile():
	def __init__(self, source):
		self.name = Path(source).stem
		self.source = source
		self.stats = {}

class Override():
	def __init__(self, propertyname, base, new):
		self.name = propertyname
		self.base = base
		self.new = new

regex_entry_start = re.compile('^.*?new\s*entry.*?\"(.*?)\".*$', re.IGNORECASE | re.MULTILINE)
regex_entry_data = re.compile('^.*?data\s*?\"(.*?)\"\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)
regex_entry_using = re.compile('^.*?using\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)
regex_entry_type = re.compile('^.*?type\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)

def has_line(stat, line):
	for x in stat.lines:
		if x.strip() == line.strip():
			return True
	return False

def parse_file(file_path, debug=False):
	print("Reading file '{}'".format(file_path))
	f = open(file_path, 'r')
	lines = f.readlines()
	f.close()
	current_file = StatFile(file_path)
	current_stat = None
	for line in lines:
		if line != "":
			if current_stat is not None:
				data_match = regex_entry_data.match(line)
				if data_match is not None:
					prop_name = data_match.group(1)
					prop_val = data_match.group(2)
					if not prop_name in ignore_props:
						current_stat.properties[prop_name] = StatProperty(current_stat, prop_name, prop_val)
						if debug: print("---- Found property {} with value {}".format(prop_name, prop_val))
				else:
					if current_stat.type == "":
						type_match = regex_entry_type.match(line)
						if type_match is not None:
							current_stat.type = type_match.group(1)
					elif current_stat.parent == "":
						using_match = regex_entry_using.match(line)
						if using_match is not None:
							current_stat.parent = using_match.group(1)
			match = regex_entry_start.match(line)
			if match is not None:
				stat_name = match.group(1)
				if stat_name is not None and stat_name != "":
					current_stat = StatEntry(current_file, stat_name)
					current_stat.lines.append(line)
					current_file.stats[stat_name] = current_stat
					if debug: print("Parsing stat entry {}".format(current_stat.name))
			elif current_stat is not None:
				current_stat.lines.append(line)
	return current_file

game_file_data = []
mod_file_data = {}

for file_path in game_files:
	result = parse_file(file_path, False)
	game_file_data.append(result)

for file_path in origins_files:
	result = parse_file(file_path, False)
	game_file_data.append(result)

for file_path in mod_files:
	result = parse_file(file_path, False)
	mod_file_data[Path(file_path).stem] = result

all_overrides = []
localkeys = []

def file_in_base(name):
	for file in game_file_data:
		if file.name == name:
			return True
	return False

def stat_in_base(name):
	for file in game_file_data:
		for entry in file.stats.values():
			if entry.name == name:
				return True
	return False

for file_data in mod_file_data.values():
	#print("File: {}".format(file_data.name))
	if file_in_base(file_data.name):
		all_base = [x for x in game_file_data if x.name == file_data.name]
		for base_data in all_base:
			for stat_name,stat_entry in file_data.stats.items():
				base_stat = None
				if stat_name in base_data.stats.keys():
					base_stat = base_data.stats[stat_name]
				if base_stat is not None:
					#print("Analyzing overrides for {} ({})".format(stat_name, base_stat.type))
					overrides = [x for x in stat_entry.properties.values() if x.name in base_stat.properties.keys()]
					for override_prop in overrides:
						base_prop = base_stat.properties[override_prop.name]
						#print("***** {} | Original: {}".format(override_prop.value, base_prop.value))
						if override_prop.value != base_prop.value:
							redirected = False
							for prop in redirect_props:
									if prop[0] == override_prop.name:
										redirected_prop_new = stat_entry.properties[prop[1]]
										if redirected_prop_new is not None:
											stat_entry.overrides.append(Override(redirected_prop_new.name, base_prop.value, redirected_prop_new.value))
											redirected = True
											localkeys.append(redirected_prop_new.value)
											break
							if redirected == False:
								stat_entry.overrides.append(Override(override_prop.name, base_prop.value, override_prop.value))
							override_prop.is_override = True

					#if len(stat_entry.overrides) > 0:
						#all_overrides.append(stat_entry)

def isnum(s):
    try:
        float(s)
    except:
        return(False)
    else:
        return(True)

export_template = """
KCE_Overrides = {{
{data}
}}
"""
file_template = """
	{name} = {{
		{stats}
	}},
"""
stat_template = """
		["{stat}"] = {{
			{props}
		}},
"""

def get_output_value(override_stat, override):
	subtype = ""
	if override_stat.type == "SkillData":
		subtype = override_stat.properties["SkillType"].value
	elif override_stat.type == "StatusData":
		subtype = override_stat.properties["StatusType"].value
	mod_type = get_modifier(override_stat.type, override.name, subtype)
	#if override_stat.type == "SkillData": print("{} | {} {} | {}".format(mod_type, override_stat.type, override.name, subtype))
	if mod_type == "Enumeration":
		return '"{}"'.format(override.new)
	elif mod_type == "Integer" or mod_type == "Float":
		return override.new
	else:
		return '"{}"'.format(override.new)

output_str = ""
data_str = ""
for file in mod_file_data.values():
	overrides = [x for x in file.stats.values() if len(x.overrides) > 0]
	if (len(overrides) > 0):
		stats_str = ""
		for override_stat in overrides:
			props_str = ""
			count = len(override_stat.overrides)
			i = 0
			for override in override_stat.overrides:
				comment = override.name == "DisplayName" or override.name == "Description"
				output = "--" if comment else ""
				output += '["{}"] = {},'.format(override.name, get_output_value(override_stat, override))
				i = i + 1
				if i < count:
					output += "\n\t\t\t"
				props_str += output
			stats_str += stat_template.format(stat=override_stat.name, props=props_str)
		data_str += file_template.format(name=file.name,stats=stats_str)
output_str = export_template.format(data=data_str).strip()
output_str = "".join([s for s in output_str.splitlines(True) if s.strip()])

#import pyperclip
#pyperclip.copy(output_str)

common.export_file(Path("Generated_StatScraper").joinpath("StatOverride_Generated.lua"), output_str)
common.export_file(Path("Generated_StatScraper").joinpath("LocalKeys_Needed.txt"), "\n".join(localkeys))

output_str = ""
for file in mod_file_data.values():
	output_str += "File: {}\n".format(file.source)
	for entry in file.stats.values():
		if(len(entry.overrides) == 0):
			if stat_in_base(entry.name):
				output_str += "Duplicate: {}\n".format(entry.name)
			else:
				output_str += "New: {}\n".format(entry.name)
		else:
			output_str += "Override: {}\n".format(entry.name)
	output_str += "\n"

common.export_file(Path("Generated_StatScraper").joinpath("StatEntries_Reference.txt"), output_str)

dir_output = Path("Generated_StatScraper").joinpath("Data")

def has_forbidden_override(entry):
	for prop in FORBIDDEN:
		if prop in entry.properties.keys():
			return True
	return False

for file in mod_file_data.values():
	output_str = ""
	for entry in file.stats.values():
		if(len(entry.overrides) == 0):
			if stat_in_base(entry.name):
				pass
			else:
				output_str += "".join(entry.lines)
		else:
			if has_forbidden_override(entry):
				output_str += "".join(entry.lines)

	if output_str != "":
		common.export_file(dir_output.joinpath("{}.txt".format(file.name)), output_str)