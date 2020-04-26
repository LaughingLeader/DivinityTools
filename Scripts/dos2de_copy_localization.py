import os
import sys
from pathlib import Path
import shutil

def get_arg(arg, fallback):
	if len(sys.argv) > arg:
		val = sys.argv[arg]
		if val != None:
			return val
	return fallback

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

input_english_file = get_arg(1, None)
output_dir = get_arg(2, None)

languages = [
	"{root}/Amlatspanish/amlatspanish.xml",
	"{root}/Chinese/chinese.xml",
	"{root}/Chinesetraditional/chinesetraditional.xml",
	"{root}/Czech/czech.xml",
	"{root}/French/french.xml",
	"{root}/German/german.xml",
	"{root}/Italian/italian.xml",
	"{root}/Japanese/japanese.xml",
	"{root}/Korean/korean.xml",
	"{root}/Polish/polish.xml",
	"{root}/Russian/russian.xml",
	"{root}/Spanish/spanish.xml"
]

if input_english_file != None and output_dir != None:
	input_english_file = Path(input_english_file)
	output_dir = Path(output_dir)
	
	output_dir.mkdir(parents=True, exist_ok=True)

	for f in languages:
		output_path = Path(f.format(root=output_dir))
		output_path.parent.mkdir(parents=True, exist_ok=True)
		print("Copying '{}' to {}".format(input_english_file.absolute(), output_path.absolute()))
		if shutil.copy(input_english_file.absolute(), output_path.absolute()):
			print("Copied '{}' to {}".format(input_english_file.name, output_path.absolute()))
else:
	print("[ERROR] - Input file and output directory arguments are not set correctly. Skipping.")