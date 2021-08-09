import os
from pathlib import Path
from typing import List,Dict
import operator
from collections import OrderedDict
import re

import dos2de_common as Common

function_pattern = re.compile('^.*public function (?P<name>.*?)\((?P<params>.*?)\)\s*:?\s*(?P<returnType>\w+|\*?).*$', re.MULTILINE | re.IGNORECASE)
var_pattern = re.compile('(public|protected|private) var (?P<name>.*?)\s*:\s*(?P<varType>\w+\*?)', re.MULTILINE | re.IGNORECASE)
param_pattern = re.compile('\s*=\s*\w+')

type_map = {
	"Boolean" : "boolean",
	"Number" : "number",
	"uint" : "integer",
	"String" : "string",
	"*" : "any",
	"Array" : "table",
	"MovieClip" : "FlashMovieClip",
	"int" : "integer",
}

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

sheet_files = [
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/abilitiesholder_9.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/customStatsHolder_14.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/MainTimeline.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/minusButton_65.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/plusButton_62.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/pointsAvailable_56.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/stats_1.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/characterSheet_fla/talentsHolder_11.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/AbilityEl.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/CustomStat.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/InfoStat.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/SecStat.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/skillEl.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/Stat.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/StatCategory.as",
"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIOverrides/_Sheets/characterSheet/Talent.as",
]

combat_log = [
	"D:/Modding/DOS2DE/UI_Modding/_GUI_FLA/combatLog/Filter.as",
	"D:/Modding/DOS2DE/UI_Modding/_GUI_FLA/combatLog/combatLog_fla/Log_1.as",
	"D:/Modding/DOS2DE/UI_Modding/_GUI_FLA/combatLog/combatLog_fla/MainTimeline.as",
	"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIExtensions/src/LS_Classes/horizontalList.as",
	"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIExtensions/src/LS_Classes/listDisplay.as",
	"G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/LeaderLib/Flash/UIExtensions/src/LS_Classes/scrollList.as",
]

script_files = sheet_files

output_all = Path(script_dir.joinpath("Generated/EmmyLua/CharacterSheet/FlashCharacterSheet.lua"))
all_text = ""
for p in script_files:
	with open(p, 'r', encoding='utf-8') as f:
		fname = Path(p).stem
		#output_path = Path(script_dir.joinpath("Generated/EmmyLua/CombatLog/").joinpath(str(fname)).with_suffix('.lua'))
		output_path = Path(script_dir.joinpath("Generated/EmmyLua/CharacterSheet/").joinpath(str(fname)).with_suffix('.lua'))
		output_txt = "---@class {}\n".format(fname)
		input_txt = f.read()
		i = 0
		for m in var_pattern.finditer(input_txt):
			name = m.group('name').strip()
			vType = m.group('varType').strip()
			if vType in type_map.keys():
				vType = type_map[vType]
			output_txt = output_txt + str.format("---@field {} {}", name, vType)
			i = i + 1
			output_txt = output_txt + "\n"
		i = 0
		for m in function_pattern.finditer(input_txt):
			name = m.group('name').strip()
			if name == fname or name == "frame1":
				continue
			paramText = m.group('params').strip()
			returnType = m.group('returnType').strip()
			if paramText != "":
				params = str.split(paramText, ",")
				paramText = ""
				index = 0
				for param in params:
					for k,v in type_map.items():
						if k == "*":
							k = "\*"
						pat = "\\b"+k+"\\b"
						#print(param,k,v, re.sub('\b{}\b'.format(k), v, param, -1, re.IGNORECASE))
						param = re.sub(pat, v, param)
						#param = str.replace(param, k, v)
						#param = str.replace(param, k, v)
					param = param_pattern.sub("", param).strip()
					params[index] = param
					index = index + 1
				paramText = ', '.join(params)
					
			if returnType == "*":
				returnType = "void"
			elif returnType in type_map.keys():
				returnType = type_map[returnType]
			output_txt = output_txt + str.format("---@field {} fun({}):{}", name, paramText, returnType)
			i = i + 1
			output_txt = output_txt + "\n"
		all_text = "{}\n{}".format(all_text, output_txt)
		#all_text = str.join(all_text, output_txt)
		#Common.export_file(output_path, output_txt.strip())
Common.export_file(output_all, all_text.strip())