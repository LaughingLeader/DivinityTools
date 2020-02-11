import os
from pathlib import Path
import dos2de_common_stats_modifiers as StatModifiers
import dos2de_common as common
import re
from typing import List, Dict

class StatOverride():
	def __init__(self, propertyname:str, base:str, new:str):
		self.name = propertyname
		self.base = base
		self.new = new

class StatProperty():
	def __init__(self, name:str, value:str):
		self.name = name
		self.value = value
		self.is_override = False

class StatEntry():
	def __init__(self, name:str):
		self.name = name
		self.properties:Dict[str, StatProperty] = {}
		self.type = ""
		self.parent = ""
		self.overrides:List[StatOverride] = []
		self.lines:List[str] = []

class StatFile():
	def __init__(self, source:Path):
		self.name = Path(source).stem
		self.source = source
		self.stats:Dict[str, StatEntry] = {}

modifiers = StatModifiers.Build_StatDefinitions()

regex_entry_start = re.compile('^.*?new\s*entry.*?\"(.*?)\".*$', re.IGNORECASE | re.MULTILINE)
regex_entry_data = re.compile('^.*?data\s*?\"(.*?)\"\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)
regex_entry_using = re.compile('^.*?using\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)
regex_entry_type = re.compile('^.*?type\s*?\"(.*?)\".*?$', re.IGNORECASE | re.MULTILINE)

def has_line(stat, line):
	for x in stat.lines:
		if x.strip() == line.strip():
			return True
	return False

def ParseFile(file_path:str, debug=False)->StatFile:
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
					current_stat.properties[prop_name] = StatProperty(prop_name, prop_val)
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
					current_stat = StatEntry(stat_name)
					current_stat.lines.append(line)
					current_file.stats[stat_name] = current_stat
					if debug: print("Parsing stat entry {}".format(current_stat.name))
			elif current_stat is not None:
				current_stat.lines.append(line)
	return current_file

