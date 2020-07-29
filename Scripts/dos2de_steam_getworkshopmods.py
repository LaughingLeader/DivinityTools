import requests
import os
from pathlib import Path
import glob
import dos2de_common as Common

def GetData():
	api_url = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=A810B264F5E4DFAB251E78048750F6D7&appid=435150&return_tags=true&return_details=true&return_metadata=true&return_short_description=true&numperpage=20000&requiredtags[0]=Definitive+Edition"
	response = requests.get(api_url)

	script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
	os.chdir(script_dir.resolve())

	output_path = script_dir.joinpath("WorkshopData").joinpath("Data.json")
	Common.export_file(output_path, response.text)
	try:
		output_path.parent.mkdir(parents=True, exist_ok=True)
		f = open(str(output_path.absolute()), 'w', encoding='utf-8')
		f.write(response.text)
		f.close()
	except Exception as e:
		print("Erroring writing '{}': {}".format(output_path.name, e))

def CreateWorkshopIDtoGUID():
	f = open(str(output_path.absolute()), 'w', encoding='utf-8')
	f.write(response.text)
	f.close()