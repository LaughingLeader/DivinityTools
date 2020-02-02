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

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

data_folder = Path("D:\Modding\DOS2DE_Extracted\Public\Shared\Stats\Generated\Data")
mod_folder = Path("G:\Divinity Original Sin 2\DefEd\Data\Public\Kalavinkas_Combat_Enhanced_e844229e-b744-4294-9102-a7362a926f71\Stats\Generated\Data")

all_game_files = list(data_folder.glob("*.txt"))
all_mod_files = list(mod_folder.glob("*.txt"))

game_files = [x for x in all_game_files if Path(x).stem in check_file_names]
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
					current_file.stats[stat_name] = current_stat
					if debug: print("Parsing stat entry {}".format(current_stat.name))
	return current_file

game_file_data = {}
mod_file_data = {}

for file_path in game_files:
	result = parse_file(file_path, False)
	game_file_data[Path(file_path).stem] = result

for file_path in mod_files:
	result = parse_file(file_path, False)
	mod_file_data[Path(file_path).stem] = result

all_overrides = []


localkeys = []

for file_data in mod_file_data.values():
	#print("File: {}".format(file_data.name))
	if file_data.name in game_file_data.keys():
		base_data = game_file_data[file_data.name]
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
				if isnum(override.new):
					output += '["{}"] = {},'.format(override.name, override.new)
				else:
					output += '["{}"] = "{}",'.format(override.name, override.new)
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