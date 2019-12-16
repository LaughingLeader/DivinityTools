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

def duplicate_entry(lineText, prop, lineNum, stat_properties, fileName):
	for checkLineNum,checkLineProp,checkLineText in stat_properties:
		if checkLineProp == prop:
			print("**DUPLICATE** property found! {}:{} - {}({})".format(fileName, lineNum, lineText, prop))
			print("**DUPLICATE** --- Match: {}:{} - {}({})".format(fileName, checkLineNum, checkLineText, prop))
			return True
	return False

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

pattern_stat_entry = r"^new entry \"(.*?)\".*$"
pattern_tags = r"Tag (\w*)"

input_path_txt = get_arg(1, "G:/Divinity Original Sin 2/DefEd/Data/Public/WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f/Stats/Generated/Data")

input_dir = Path(input_path_txt)
files = list(input_dir.glob("*Skill*.txt"))

print("Total files in '{}' - {}".format(input_path_txt, len(files)))

class SkillTagData():
	def __init__(self, skill):
		self.skill = skill
		self.tags = []

skill_entries = []

for file_path in files:
	with open(file_path.absolute()) as f:
		skill = None
		lineNum = 1
		line = f.readline()
		while line:
			if is_empty(line):
				skill = None
			else:
				skill_declaration_match = re.search(pattern_stat_entry, line)
				if skill_declaration_match is not None:
					skill = SkillTagData(skill_declaration_match.group(1))
					skill_entries.append(skill)
				elif skill is not None:
					matches = re.finditer(pattern_tags, line, re.MULTILINE)
					for matchNum, match in enumerate(matches, start=1):
						for groupNum in range(0, len(match.groups())):
							groupNum = groupNum + 1
							tag = match.group(groupNum)
							if tag is not None and tag != "":
								skill.tags.append(tag)
			lineNum += 1
			line = f.readline()

output_str = ""

for skill in skill_entries:
	for tag in skill.tags:
		db_str = "DB_LLWEAPONEX_Skills_TagRequirements(\"{}\", \"{}\");\n".format(skill.skill, tag)
		print(db_str)
		output_str += db_str

import pyperclip
pyperclip.copy(output_str)