import os
from pathlib import Path
from typing import List, Dict

import dos2de_common as Common
from dos2de_common_stats_parser import StatEntry
import dos2de_common_stats_parser as StatParser

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

stats_path = Path("G:\Divinity Original Sin 2\DefEd\Data\Public\EnemyUpgradeOverhaul_046aafd8-ba66-4b37-adfb-519c1a5d04d7\Stats\Generated\Data\LLENEMY_Statuses_Main.txt")
tsv_path = Path("G:\SourceControlGenerator\Data\Divinity Original Sin 2 - Definitive Edition\Projects\EnemyUpgradeOverhaul\LocalKeys\LLENEMY_Statuses.tsv")

statfile = StatParser.ParseFile(stats_path.absolute())

print("Reading file '{}'".format(tsv_path.absolute()))
f = open(tsv_path.absolute(), 'r')
lines = f.readlines()
f.close()
lines.pop(0)

tsv_entries = {}
for line in lines:
	entry = tuple(line.strip().split("\t"))
	tsv_entries[entry[0]] = entry

#print("TSV Entries:\n{}".format("\n".join(tsv_entries.keys())))

statuses:List[StatEntry] = sorted(list([x for x in statfile.stats.values() if x.type == "StatusData"]), key=lambda x: {x.name})

lua_template = """
local upgrade_info_statuses = {{
	{output}
}}

local upgrade_colors = {{
	{output2}
}}
"""

osiris_template = "LLENEMY_UpgradeInfo_Register(\"{status}\", \"{name}\", \"{description}\");\n"

lua_str = ""
lua_str2 = ""
osiris_str = ""

custom_colors = {
	"LLENEMY_TALENT_LEECH" : "#C80030",
	"LLENEMY_TALENT_LIGHTNINGROD" : "#7D71D9",
	"LLENEMY_TALENT_LONEWOLF" : "#DC0015",
	"LLENEMY_TALENT_NATURALCONDUCTOR" : "#7D71D9",
	"LLENEMY_TALENT_RESISTDEAD2" : "#f5ff83",
	"LLENEMY_TALENT_UNSTABLE" : "#9c3c8f",
	"LLENEMY_TALENT_WEATHERPROOF" : "#4197E2",
	"LLENEMY_TALENT_WHATARUSH": "#47e982",
	"LLENEMY_TALENT_TORTURER" : "#960000",
	"LLENEMY_TALENT_COUNTER" : "#57ff7c",
	"LLENEMY_TALENT_SADIST" : "#ff5771",
	"LLENEMY_TALENT_HAYMAKER" : "#b083ff",
	"LLENEMY_TALENT_GLADIATOR" : "#f59b00",
	"LLENEMY_TALENT_INDOMITABLE" : "#e94947",
	"LLENEMY_TALENT_SOULCATCHER" : "#73F6FF",
	"LLENEMY_TALENT_MASTERTHIEF" : "#C9AA58",
	"LLENEMY_TALENT_GREEDYVESSEL" : "#e9d047",
	"LLENEMY_TALENT_MAGICCYCLES" : "#22c3ff",
	"LLENEMY_INF_NECROFIRE" : "#7F00FF",
	"LLENEMY_INF_WATER" : "#188EDE",
	"LLENEMY_INF_BLESSED_ICE" : "#CFECFF",
	"LLENEMY_INF_POISON" : "#65C900",
	"LLENEMY_INF_ACID" : "#81AB00",
	"LLENEMY_INF_ELECTRIC" : "#7D71D9",
	"LLENEMY_INF_CURSED_ELECTRIC" : "#7F25D4",
	"LLENEMY_INF_BLOOD" : "#AA3938",
	"LLENEMY_INF_OIL" : "#C7A758",
	"LLENEMY_INF_FIRE" : "#FE6E27",
	"LLENEMY_BONUS_TREASURE_ROLL" : "#D040D0",
	"LLENEMY_IMMUNITY_LOSECONTROL" : "#FFAB00",
	"LLENEMY_DOUBLE_DIP" : "#7F00FF",
	"LLENEMY_PERSEVERANCE_MASTERY" : "#E4CE93",
	"LLENEMY_BONUSSKILLS_SINGLE" : "#F1D466",
	"LLENEMY_BONUSSKILLS_SET_NORMAL" : "#B823CB",
	"LLENEMY_BONUSSKILLS_SOURCE" : "#46B195",
	"LLENEMY_BONUSSKILLS_SET_ELITE" : "#73F6FF",
}

def write_locale(stat:StatEntry):
	global osiris_str,lua_str2
	try:
		displayname_key = stat.properties["DisplayName"].value if "DisplayName" in stat.properties.keys() else ""
		description_key = stat.properties["Description"].value if "Description" in stat.properties.keys() else ""

		displayname = ""
		description = ""

		if displayname_key != "" and displayname_key in tsv_entries.keys():
			displayname = tsv_entries[displayname_key][1]
		
		if description_key != "" and description_key in tsv_entries.keys():
			description = tsv_entries[description_key][1]

		if displayname != "" or description != "":
			color = ""
			if stat.name in custom_colors.keys():
				color = custom_colors[stat.name]
			else:
				if "TALENT" in stat.name:
					color = "#AABB00"
				elif "BONUSSKILLS" in stat.name:
					color = "#73F6FF"
				elif "INF" in stat.name:
					color = "#FE6E27"
				else:
					color = "#FFFFFF"
			#print("{},{}".format(displayname_key, description_key))
			# if stat.name in custom_colors.keys():
			# 	color = custom_colors[stat.name]
			# 	displayname = "<font color='{}'>{}</font>".format(color, displayname)
			# else:
			# 	if "TALENT" in stat.name:
			# 		displayname = "<font color='#FFAB00'>{}</font>".format(displayname)
			# 	elif "BONUSSKILLS" in stat.name:
			# 		displayname = "<font color='#73F6FF'>{}</font>".format(displayname)
			# 	elif "INF" in stat.name:
			# 		displayname = "<font color='#FE6E27'>{}</font>".format(displayname)
			# 	else:
			# 		displayname = "<font color='#FFFFFF'>{}</font>".format(displayname)
			osiris_str += osiris_template.format(status=stat.name, name=displayname, description=description)
			lua_str2 += "\t[\"{}\"] = \"{}\",\n".format(displayname, color)
			return True
	except Exception as e:
		print("Error: {}".format(e))
	return False

ignored_statuses = [
	"LLENEMY_UPGRADE_INFO",
	"LLENEMY_FAKE_DYING",
	"LLENEMY_DUPLICANT",
	"LLENEMY_CHICKEN_OVERLORD",
	"LLENEMY_GRANADA",
	"LLENEMY_INFUSION_INFO",
	"LLENEMY_INFUSION_INFO_ELITE",
	# Talents with custom mechanics
	"LLENEMY_TALENT_COUNTER",
	"LLENEMY_TALENT_BULLY",
	"LLENEMY_TALENT_BULLY_DAMAGEBONUS",
	"LLENEMY_TALENT_LIGHTNINGROD",
	"LLENEMY_TALENT_NATURALCONDUCTOR",
	"LLENEMY_TALENT_RESISTDEAD",
	"LLENEMY_TALENT_RESISTDEAD2",
	"LLENEMY_TALENT_WEATHERPROOF",
	"LLENEMY_TALENT_UNSTABLE",
]

for stat in statuses:
	if stat.name.startswith("_") or stat.name in ignored_statuses:
		pass
	else:
		if write_locale(stat) == True:
			lua_str += "\t\"{}\",\n".format(stat.name)

lua_output = lua_template.format(output=lua_str.strip(),output2=lua_str2.strip())

Common.export_file(Path("Generated_EnemyUpgradeOverhaul").joinpath("Lua_UpgradeInfoStatuses.lua"), lua_output.strip())
Common.export_file(Path("Generated_EnemyUpgradeOverhaul").joinpath("Osiris_UpgradeInfoStatuses.txt"), osiris_str.strip())