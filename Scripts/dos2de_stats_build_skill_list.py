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
pattern_requirement_property = r"^data \"Requirement\" \"(.*?)\"$"
pattern_ability_property = r"^data \"Ability\" \"(.*?)\"$"
pattern_inheritance = r"^using \"(.*?)\"$"

ignored_skills = [
	"Turret",
	"Projectile_Grenade_",
	"Dummy",
	"NULL",
]

input_path_txt = get_arg(1, "D:/Modding/DOS2DE_Extracted/_AllSkillData")

input_dir = Path(input_path_txt)
files = list(input_dir.glob("*Skill*.txt"))

print("Total files in '{}' - {}".format(input_path_txt, len(files)))

def ignore_skill(name):
	for s in ignored_skills:
		if s in name:
			return True
	return False

class SkillData():
	def __init__(self, skill):
		self.name = skill
		self.requirement = ""
		self.ability = ""
		self.parent = ""

skill_entries = {}
requirements = {}
abilities = {}

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
					skillname = skill_declaration_match.group(1)
					if not ignore_skill(skillname):
						skill = SkillData(skillname)
						skill_entries[skillname] = skill
				elif skill is not None:
					requirement_match = re.search(pattern_requirement_property, line)
					if requirement_match is not None:
						skill.requirement = requirement_match.group(1)
						if skill.requirement != "" and skill.requirement != "None":
							requirements[skill.requirement] = True
					ability_match = re.search(pattern_ability_property, line)
					if ability_match is not None:
						skill.ability = ability_match.group(1)
						if skill.ability != "" and skill.ability != "None":
							abilities[skill.ability] = True
					parent_match = re.search(pattern_inheritance, line)
					if parent_match is not None:
						skill.parent = parent_match.group(1)
			lineNum += 1
			line = f.readline()

def update_missing_values(skill : SkillData):
	if skill.parent != "":
		if skill.parent in skill_entries.keys():
			parent_skill = skill_entries[skill.parent]
			update_missing_values(parent_skill)
			if skill.requirement == "":
				skill.requirement = parent_skill.requirement
			if skill.ability == "":
				skill.ability = parent_skill.ability

for skill in skill_entries.values():
	update_missing_values(skill)

output_str = ""

for s in sorted(requirements.keys()):
	output_str += "DB_LLWEAPONEX_WeaponSwapper_SkillRequirements(\"{}\");\n".format(s)

output_str += "\n"

for s in sorted(abilities.keys()):
	output_str += "DB_LLWEAPONEX_WeaponSwapper_SkillAbilities(\"{}\");\n".format(s)

output_str += "\n"

#sorted_skills = sorted(skill_entries.values(), key=lambda x: (x.requirement, x.ability, x.name), reverse=True)
sorted_skills = sorted(skill_entries.values(), key=lambda x: (x.requirement, x.name))

for skill in sorted_skills:
	if skill.requirement == "" or skill.requirement == "None":
		pass
	else:	
		output_str += "DB_LLWEAPONEX_WeaponSwapper_SkillData(\"{}\", \"{}\", \"{}\");\n".format(skill.name, skill.requirement, skill.ability)

import pyperclip
pyperclip.copy(output_str)