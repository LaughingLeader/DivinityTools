from bs4 import BeautifulSoup
from PIL import Image
import os
from pathlib import Path
import glob

class Data():
	def __init__(self, name, folder, uuid):
		self.name = name
		self.folder = folder
		self.uuid = uuid

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir.resolve())

metafiles_dir = "D:/Modding/DOS2DE_Extracted/Mods"

mod_dirs = [x for x in os.listdir(metafiles_dir)
            if os.path.isdir(os.path.join(metafiles_dir, x))]

metafiles = []

for mod_dir in mod_dirs:
	p = os.path.join(metafiles_dir, mod_dir)
	for file in os.listdir(p):
		if file == "meta.lsx":
			metafiles.append(os.path.join(p, file))

metadata = []

def get_attribute(xml, id):
	v = xml.find("attribute", attrs={"id":id})
	if v is not None:
		try:
			inner = v["value"]
			return inner
		except: pass
	return None

for p in metafiles:
	#meta_path = p.absolute()
	meta_path = p
	print("Reading file '{}'".format(meta_path))
	meta_xml = None
	f = open(meta_path, 'r')
	meta_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	meta_name = Path(meta_path).stem

	module_info = meta_xml.find("node", attrs={"id":"ModuleInfo"})
	if module_info != None:
		name = get_attribute(module_info, "Name")
		larianmod_display_name = get_attribute(module_info, "DisplayName")
		description = get_attribute(module_info, "Description")
		larianmod_description = get_attribute(module_info, "DescriptionName")
		folder = get_attribute(module_info, "Folder")
		uuid = get_attribute(module_info, "UUID")
		version = get_attribute(module_info, "Version")
		mod_type = get_attribute(module_info, "Type")
		md5 = get_attribute(module_info, "MD5")
		target = "Story"

		if larianmod_display_name is not None:
			name = larianmod_display_name

		if larianmod_description is not None:
			description = larianmod_description

		if uuid is not None:
			d = Data(name, folder, uuid)
			d.description = description
			d.version = version
			d.mod_type = mod_type
			d.target = target
			d.md5 = md5
			metadata.append(d)

output_str = ""

for data in sorted(metadata, key=lambda x: {x.name}):
	output_str += 'new DivinityModData{{ Name = \"{}\", UUID = \"{}\", Folder=\"{}\", Version=DivinityModVersion.FromInt({}), Type=\"{}\", Targets=\"{}\", Author=\"Larian\", Description=\"{}\", MD5=\"{}\"}},\n'.format(data.name, data.uuid, data.folder, data.version, data.mod_type, data.target, data.description, data.md5)
	print(output_str)

import pyperclip
pyperclip.copy(output_str)