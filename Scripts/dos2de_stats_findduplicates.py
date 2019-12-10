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

pattern_stat_data_property = r"^data \"(.*?)\".*$"

input_path_txt = get_arg(1, "G:/Divinity Original Sin 2/DefEd/Data/Public/WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f/Stats/Generated/Data")

input_dir = Path(input_path_txt)
files = list(input_dir.glob("*.txt"))

print("Total files in '{}' - {}".format(input_path_txt, len(files)))

for file_path in files:
	#print("Reading file: {}".format(file_path.name))

	with open(file_path.absolute()) as f:
		stat_properties = []
		lineNum = 1
		line = f.readline()
		while line:
			if is_empty(line):
				stat_properties.clear()
			else:
				m = re.search(pattern_stat_data_property, line)
				if m is not None and m.group() is not None:
					prop = m.group(1)
					if duplicate_entry(line, prop, lineNum, stat_properties, file_path.name):
						pass	
					stat_properties.append((lineNum, prop, line))
			lineNum += 1
			line = f.readline()
