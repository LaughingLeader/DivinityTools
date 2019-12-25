import os
import sys
import pathlib
from pathlib import Path
import re

import dos2de_common as common

npc_weapon_template = """
new entry "_{stat}_NPC"
type "Weapon"
using "{stat}"
data "ObjectCategory" ""
data "Damage" "2"
data "Boosts" ""

"""
npc_shield_template = """
new entry "_{stat}_NPC"
type "Shield"
using "{stat}"
data "ObjectCategory" ""
data "Durability" "10"
data "Movement" "0"
"""

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

pattern_stat_entry = r"^new entry \"(.*?)\".*$"
unique_line = 'data "Unique" "1"'

weapons_file = Path("G:/Divinity Original Sin 2/DefEd/Data/Public/WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f/Stats/Generated/Data/LLWEAPONEX_Weapons.txt")
shields_file = Path("G:/Divinity Original Sin 2/DefEd/Data/Public/WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f/Stats/Generated/Data/LLWEAPONEX_Shields.txt")

class StatData():
	def __init__(self, name):
		self.name = name

ignored_names = [
	"Display",
	"Debug",
	"Crafted",
	"Preview",
	"UNIQUE",
	"NPC",
	"Npc",
	"Unarmed"
]

def ignore_entry(name : str):
	if name.startswith("_"):
		return True
	for s in ignored_names:
		if s in name:
			return True
	return False

def gen_file(file, template, output):
	stats = []
	with open(file) as f:
		entry = None
		lineNum = 1
		line = f.readline()
		while line:
			if common.is_empty(line):
				entry = None
			else:
				new_entry_math = re.search(pattern_stat_entry, line)
				if new_entry_math is not None:
					name = new_entry_math.group(1)
					if not ignore_entry(name):
						entry = StatData(name)
						stats.append(entry)
				elif entry is not None:
					pass
			lineNum += 1
			line = f.readline()

	output_str = ""
	names_str = ""
	output_path = Path(output)

	for stat in sorted(stats, key=lambda x: (x.name)):
		output_str += template.format(stat=stat.name)
		names_str += '_{}_NPC\n'.format(stat.name)
	
	common.export_file(output, output_str)
	common.export_file(output_path.with_name(output_path.name + "_List"), output_str)

	#import pyperclip
	#pyperclip.copy(output_str)

gen_file(weapons_file.absolute(), npc_weapon_template, Path("Generated/LLWEAPONEX_Z_Weapons_NPC.txt"))
gen_file(shields_file.absolute(), npc_shield_template, Path("Generated/LLWEAPONEX_Z_Shields_NPC.txt"))