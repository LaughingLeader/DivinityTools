import os
from pathlib import Path
from typing import List, Dict
import subprocess
from bs4 import BeautifulSoup,Tag
import sys
import traceback

divine_path = Path("G:/Modding/DOS2DE/ConverterApp/divine.exe")

def get_attribute(xml, id):
	v = xml.find("attribute", attrs={"id":id})
	if v is not None:
		try:
			inner = v["value"]
			return inner
		except: pass
	return ""

validTypes = [
	"lsx",
	"lsb",
	"lsf",
]

def convertFile(filePath:Path):
	if type(filePath) == str:
		filePath = Path(filePath)
	inType = filePath.suffix.lower().replace(".", "")
	if inType in validTypes:
		outType = "lsx"
		if inType == "lsx":
			try:
				f = open(file, 'r')
				lsx_xml = BeautifulSoup(f.read(), 'lxml')
				f.close()
				shouldBeLSB = lsx_xml.find("region", attrs={"id":"TranslatedStringKeys"}) is not None
				if shouldBeLSB:
					outType = "lsb"
				else:
					outType = "lsf"
			except Exception as e:
				print("Error opening file '{}':".format(file))
				traceback.print_exc()
				outType = "lsf"

		p = subprocess.run([str(divine_path.absolute()), 
			"-l", 
			"all",
			"-s",
			str(filePath.absolute()),
			"-a",
			"convert-resource",
			"-d",
			str(filePath.with_suffix("." + outType)),
			"-i",
			inType,
			"-o",
			outType
			], 
			universal_newlines=True, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE)
		print("Converted {}.".format(filePath))

try:
	if len(sys.argv) > 1:
		sys.argv.pop(0)
		for file in sys.argv:
			if file is not None:
				filePath = Path(file)
				if filePath.is_dir():
					subFiles:List[Path] = []
					subFiles.extend(filePath.rglob("*.lsx"))
					subFiles.extend(filePath.rglob("*.lsb"))
					subFiles.extend(filePath.rglob("*.lsf"))
					for f in subFiles:
						try:
							convertFile(f)
						except Exception as e:
							print("Error converting file '{}':".format(f))
							traceback.print_exc()
				else:
					try:
						convertFile(filePath)
					except Exception as e:
						print("Error converting file '{}':".format(filePath))
						traceback.print_exc()
except Exception as e:
	print("Error converting files:\n")
	traceback.print_exc()