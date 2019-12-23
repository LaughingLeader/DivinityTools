import os
import sys
import pathlib
from pathlib import Path
import re

npc_weapon_template = """
new entry "_{stat}_NPC"
type "Weapon"
using "{stat}"
data "ObjectCategory" ""
data "Damage" "2"
data "Boosts" ""
"""

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

pattern_stat_entry = r"^new entry \"(.*?)\".*$"
unique_line = 'data "Unique" "1"'

weapons_file = Path("G:/Divinity Original Sin 2/DefEd/Data/Public/WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f/Stats/Generated/Data/LLWEAPONEX_Weapons.txt")

class WeaponData():
	def __init__(self, name):
		self.name = name

weapons = []

def is_empty(line):
	return line in ['\n', '\r\n']

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

with open(weapons_file.absolute()) as f:
	entry = None
	lineNum = 1
	line = f.readline()
	while line:
		if is_empty(line):
			entry = None
		else:
			new_entry_math = re.search(pattern_stat_entry, line)
			if new_entry_math is not None:
				name = new_entry_math.group(1)
				if not ignore_entry(name):
					entry = WeaponData(name)
					weapons.append(entry)
			elif entry is not None:
				pass
		lineNum += 1
		line = f.readline()

output_str = ""
names_str = ""

for weapon in sorted(weapons, key=lambda x: (x.name)):
	output_str += npc_weapon_template.format(stat=weapon.name)
	names_str += '_{}_NPC\n'.format(weapon.name)

import pyperclip
pyperclip.copy(output_str)
#pyperclip.copy(names_str)