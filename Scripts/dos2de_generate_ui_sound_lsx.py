import os
from pathlib import Path
from typing import List, Dict
import dos2de_common as Common
from bs4 import BeautifulSoup
from bs4 import Tag
import subprocess

entry_template = """
				<node id="Resource">
					<attribute id="ID" value="{resourceuuid}" type="22" />
					<attribute id="Localized" value="False" type="19" />
					<attribute id="SourceFile" value="{bankpath}" type="30" />
					<attribute id="Name" value="{displayname}" type="23" />
					<attribute id="SoundEventID" value="{hash}" type="5" />
					<attribute id="SoundEvent" value="{name}" type="22" />
					<attribute id="SoundBank" value="{bankname}" type="22" />
					<attribute id="SoundEventUUID" value="{uuid}" type="31" />
					<attribute id="MaxDistance" value="{attenuation}" type="6" />
					<attribute id="Duration" value="{duration}" type="6" />
					<attribute id="Preload" value="False" type="19" />
					<attribute id="Internal" value="True" type="19" />
					<attribute id="SoundCodec" value="7" type="27" />
					<attribute id="GMSoundCategory" value="0" type="27" />
					<attribute id="SoundCategory" value="0" type="27" />
					<attribute id="DisplayName" value="" type="30" />
					<attribute id="GMSubSection" value="" type="30" />
				</node>
"""

class SoundEntry():
	def __init__(self):
		self.uuid = ""
		self.name = ""
		self.displayname = ""
		self.hash = ""
		self.duration = ""
		self.attenuation = ""
		self.resourceuuid = ""

	def FromNode(self, node:Tag):
		self.displayname = Common.GetAttributeNodeValue(node, "Name")
		self.name = Common.GetAttributeNodeValue(node, "SoundEvent")
		self.hash = Common.GetAttributeNodeValue(node, "SoundEventID")
		self.uuid = Common.GetAttributeNodeValue(node, "SoundEventUUID")
		self.attenuation = Common.GetAttributeNodeValue(node, "MaxDistance")
		self.duration = Common.GetAttributeNodeValue(node, "Duration")
		self.resourceuuid = Common.GetAttributeNodeValue(node, "ID")
		return self

	def FromTuple(self, obj:tuple):
		#UUID Name	Hash	Duration	Attenuation
		self.uuid = obj[0]
		self.name = obj[1]
		self.displayname = self.name
		self.hash = obj[2]
		self.duration = obj[3]
		self.attenuation = obj[4]
		if self.attenuation is None:
			self.attenuation = "-1.0"
		self.resourceuuid = Common.NewUUID()
		return self

	def __str__(self):
		return "{} {} {} {} {}".format(self.displayname, self.uuid, self.hash, self.duration, self.attenuation)
	def export(self, bankname, bankpath):
		return entry_template.format(name=self.name, displayname=self.displayname, resourceuuid=self.resourceuuid, hash=self.hash, 
			bankname=bankname, bankpath=bankpath, uuid=self.uuid, 
				attenuation=self.attenuation, duration=self.duration)

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

base_resources_dir = Path("D:/Modding/DOS2DE_Extracted/Public/Shared/Content/Assets/Sound_DOS2")
lsx_files:List[str] = list(base_resources_dir.rglob("*.lsx"))

base_entries:Dict[str, SoundEntry] = {}
for p in lsx_files:
	f = open(p, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()
	nodes:List[Tag] = list(lsx_xml.find_all("node", attrs={"id":"Resource"}))
	for node in nodes:
		entry = SoundEntry().FromNode(node)
		base_entries[entry.name] = entry

resource_uuids:Dict[str,str] = {}
resource_list_path = Path(script_dir.joinpath("Generated_LeaderLib_SoundResources").joinpath("ResourceUUIDs.tsv"))
if resource_list_path.exists():
	print("Reading file '{}'".format(resource_list_path.absolute()))
	f = open(resource_list_path.absolute(), 'r')
	lines = f.readlines()
	f.close()
	lines.pop(0)
	for line in lines:
		obj = tuple(line.strip().split("\t"))
		name = obj[0]
		uuid = obj[1]
		resource_uuids[name] = uuid


#ui_txt = Path("D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/UI.txt")
def ParseBankFile(path:str, nameprefix="LeaderLib_")->List[SoundEntry]:
	print("Reading file '{}'".format(path))
	f = open(path, 'r', encoding='utf-8')
	lines = f.readlines()
	f.close()
	lines.pop(0)

	sound_entries:List[SoundEntry] = []
	for line in lines:
		obj = tuple(line.strip().split("\t"))
		entry = SoundEntry().FromTuple(obj)
		if not entry.name in base_entries.keys():
			entry.displayname = nameprefix + entry.name
			sound_entries.append(entry)
			if entry.displayname in resource_uuids.keys():
				entry.resourceuuid = resource_uuids[entry.displayname]
			else:
				resource_uuids[entry.displayname] = entry.resourceuuid
		else:
			#print("Sound event already used in a Shared asset: {}".format(entry))
			pass

	sound_entries.sort(key=lambda x: x.name, reverse=False)
	return sound_entries
#print("Loaded sound entries: {}".format("\n".join([str(x) for x in sound_entries])))

lsx_template = """
<?xml version="1.0" encoding="utf-8"?>
<save>
	<header version="2" time="0" />
	<version major="54" minor="6" revision="0" build="0" />
	<region id="SoundBank">
		<node id="SoundBank">
			<children>
				{}
			</children>
		</node>
	</region>
</save>
"""

bank_files = [
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Items_Containers.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Items_Inventory.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Items_Objects.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Music.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Music_GM.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Player.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Rumble.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Scripted.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Skills.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Status_FX.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Surfaces.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/UI.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Vocals_Combat.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Weapons.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/Weather_FX.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Assets/Sound/z_TESTS.txt",
]

conversion_export = Path("G:/Divinity Original Sin 2/DefEd/Data/Public/LeaderLib_543d653f-446c-43d8-8916-54670ce24dd9/Content/LeaderLib_Sounds/Shared")
divine_path = Path("G:/Modding/DOS2DE/ConverterApp/divine.exe")

for s in bank_files:
	path = Path(s)
	if path.exists():
		bankpath = Path(s.replace("D:/Modding/DOS2DE_Extracted/", "")).with_suffix(".bnk")
		bankname = path.stem
		sound_entries = ParseBankFile(path.absolute(), "LeaderLib_" + bankname + "_")

		pak_folder_export = conversion_export.joinpath("[PAK]_{}".format(bankname))

		count = len(sound_entries)
		if count > 0:
			entry_text = ""
			i = 0
			end = len(sound_entries) - 1
			for entry in sound_entries:
				entry_text += entry.export(bankname, bankpath).strip()
				if i < end:
					entry_text += "\n\t\t\t\t"
				i = i + 1

			output_str = lsx_template.format(entry_text).strip()
			export_path = script_dir.joinpath("Generated_LeaderLib_SoundResources").joinpath("LeaderLib_{}_Sounds.lsx".format(bankname))
			if Common.export_file(export_path, output_str):
				print("Exported '{}' sound events to {}".format(count, export_path))
				if pak_folder_export.exists() == False:
					pak_folder_export.mkdir(parents=True, exist_ok=True)
				base_name = Path(export_path).stem
				file_output = Path(pak_folder_export.joinpath(base_name))
				lsf_export = str(file_output.with_suffix(".lsf").absolute())
				#%divine% -l all -s "%~1" -a convert-resource -d "%~2" -i %~3 -o %~4
				p = subprocess.run([str(divine_path.absolute()), 
					"-l", 
					"all",
					"-s",
					str(export_path),
					"-a",
					"convert-resource",
					"-d",
					lsf_export,
					"-i",
					"lsx",
					"-o",
					"lsf"
					], 
					universal_newlines=True, 
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
				print(p.stdout)
				print(p.stderr)

resource_list_str = "Name\tUUID\n"
i = 0
count = len(resource_uuids) - 1
for displayname,uuid in resource_uuids.items():
	resource_list_str += "{}\t{}".format(displayname, uuid)
	if i < count:
		resource_list_str += "\n"
	i = i + 1
Common.export_file(resource_list_path, resource_list_str)