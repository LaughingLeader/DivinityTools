import os
import sys
import pathlib
from pathlib import Path
import re

def get_arg(arg, fallback):
	if len(sys.argv) > arg:
		val = sys.argv[arg]
		if val != None:
			return val
	return fallback

def is_empty(line):
	return line in ['\n', '\r\n']

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

pattern_stat_entry = r"^new entry \"(.*?)\".*$"
pattern_stat_type = r"^type \"(.*?)\".*$"
pattern_props = r"^.*?(LeaveAction|ExplodeRadius|using).*?\"((?!data)[^\"\s]+)\".*?$"

input_path_txt = get_arg(1, "G:/Divinity Original Sin 2/DefEd/Data/Public/WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f/Stats/Generated/Data")

input_dir = Path(input_path_txt)
files = list(input_dir.glob("*.txt"))

print("Total files in '{}' - {}".format(input_path_txt, len(files)))

class StatEntry():
	def __init__(self, name):
		self.name = name
		self.props = {}
		self.type = ""

stat_entries = []

for file_path in files:
	with open(file_path.absolute()) as f:
		stat = None
		lineNum = 1
		line = f.readline()
		while line:
			if is_empty(line):
				stat = None
			else:
				stat_declaration_match = re.search(pattern_stat_entry, line)
				if stat_declaration_match is not None:
					stat = StatEntry(stat_declaration_match.group(1))
					stat_entries.append(stat)
				elif stat is not None:
					type_match = re.search(pattern_stat_type, line)
					if type_match is not None:
						stat.type = type_match.group(1)
						#print("Stat '{}' Type = '{}'".format(stat.name, stat.type))

					matches = re.finditer(pattern_props, line, re.MULTILINE)
					for matchNum, match in enumerate(matches, start=1):
						prop_name = match.group(1)
						prop = match.group(2)
						if prop_name is not None and prop_name != "":
							stat.props[prop_name] = prop
							#print("Added prop '{}' for stat '{}' = '{}'".format(prop_name, stat.name, prop))
							#if prop_name == "ExplodeRadius":
							#	print("Added prop '{}' for stat '{}' = '{}'".format(prop_name, stat.name, prop))
							
			lineNum += 1
			line = f.readline()

output_str = ""

def get_stat(name):
	for stat in stat_entries:
		if stat.name == name:
			return stat
	return None

def parse_parent(stat, target):
	if "using" in stat.props.keys():
		parent_name = stat.props["using"]
		parent = get_stat(parent_name)
		if parent:
			for p in parent.props.keys():
				if not p in stat.props.keys():
					stat.props[p] = parent.props[p]
			parse_parent(parent, stat)

for stat in stat_entries:
	parse_parent(stat, stat)

skill_entries = [x for x in stat_entries if x.type == "SkillData"]
status_entries = [x for x in stat_entries if x.type == "StatusData"]

db_str = 'LeaderLib_Statuses_Register_LeaveActionStatus("WeaponExpansion_LeaveActionStatuses", "{name}", "{skill}", {radius});'

for status in status_entries:
	if "LeaveAction" in status.props.keys():
		skill_name = status.props["LeaveAction"]
		#print("Looking for skill '{}' for '{}'".format(skill_name, status.name))
		skill = get_stat(skill_name)
		#if skill is not None: print("Looking for ExplodeRadius in stat '{}' for '{}'".format(skill.name, status.name))
		if skill and "ExplodeRadius" in skill.props.keys():
			status.props["ExplodeRadius"] = skill.props["ExplodeRadius"]				

output_entries = [x for x in status_entries if "LeaveAction" in x.props.keys()]

i = 0
count = len(output_entries)
for status in output_entries:
	if "LeaveAction" in status.props.keys():
		explode_radius = "0"
		if "ExplodeRadius" in status.props.keys():
			explode_radius = status.props["ExplodeRadius"]
		entry = db_str.format(name=status.name, skill=status.props["LeaveAction"], radius=explode_radius)
		if i < count: entry += '\n'
		print(entry)
		output_str += entry
	i += 1

import pyperclip
pyperclip.copy(output_str)