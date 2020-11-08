from bs4 import BeautifulSoup
import os
from pathlib import Path
import glob
import dos2de_common as common
import timeit

metadata_master = "D:\Modding\DOS2DE_Extracted\Localization\English\Soundbanks\VoiceMetaData.lsx"
template_entry = "Ext.AddVoiceMetaData(uuid, \"{handle}\", \"Localization/English/Soundbanks/{file}\", {length})\n"
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

def get_attribute(xml:BeautifulSoup, id, node="attribute", attid="id", valueid="value", recursive=True):
	v = xml.find(node, attrs={attid:id}, recursive=recursive)
	if v is not None:
		try:
			inner = v[valueid]
			return inner
		except: pass
	return ""

class VoiceEntry():
	def __init__(self, handle, audioFile, length):
		self.handle = handle
		self.audioFile = audioFile
		self.length = length

	def Export(self, uuid):
		return template_entry.format(handle=self.handle, file=self.audioFile, length=self.length)

print("Reading file '{}'".format(metadata_master))
lsx_xml = None
f = open(metadata_master, 'r')
lsx_xml = BeautifulSoup(f.read(), 'lxml')
f.close()
speaker_entries = list(lsx_xml.find_all("node", attrs={"id":"VoiceSpeakerMetaData"}))

def get_data(lsx_path:str, speakerId:str, nextSpeaker:str)->str:
	# print("Reading file '{}'".format(lsx_path))
	# lsx_xml = None
	# f = open(lsx_path, 'r')
	# lsx_xml = BeautifulSoup(f.read(), 'lxml')
	# f.close()
	voice_entries = []
	speaker_node = None
	# speaker_entries = list(lsx_xml.find_all("node", attrs={"id":"VoiceSpeakerMetaData"}))
	for node in speaker_entries:
		mapKey = get_attribute(node, "MapKey", recursive=False)
		if mapKey == speakerId:
			speaker_node = node
			break

	if speaker_node is not None:
		nodes = list(speaker_node.find_all("node", attrs={"id":"VoiceTextMetaData"}))
		for node in nodes:
			handle = get_attribute(node, "MapKey", recursive=False)
			audioFile = get_attribute(node, "Source")
			length = get_attribute(node, "Length")
			voiceEntry = VoiceEntry(handle, audioFile, length)
			voice_entries.append(voiceEntry)

	output = ""
	for entry in voice_entries:
		output = output + entry.Export(nextSpeaker)
	return output

Voices = {
	"Warrior_Male": "7b6c1f26-fe4e-40bd-a5d0-e6ff58cef4fe",
	"Warrior_Female": "3fa5bdba-c232-430e-a8ba-b8577ac6e131",
	"Adventurer_Male": "c451954c-73bf-46ce-a1d1-caa9bbdc3cfd",
	"Adventurer_Female": "0ad5969c-d7d3-471c-a029-d268d0de43ef",
	"Scholar_Male": "41a06985-7851-4c29-8a78-398ccb313f39",
	"Scholar_Female": "be402c2a-f28c-4a33-9256-c17a42b23212",
	"Trickster_Female": "db6d2c35-6f52-4115-a460-30e9bb1b2eb5",
	"Trickster_Male": "41a594ed-b768-4289-9f17-59f701cc6910",
}
harken = "e446752a-13cc-4a88-a32e-5df244c90d8b" # Harken
korvash = "3f20ae14-5339-4913-98f1-24476861ebd6" # Korvash
def Run():
	for k,v in Voices.items():
		entries = get_data(metadata_master, v, "")
		#entries = get_data(metadata_master, voice_scholar_male1, korvash)
		output = """return function(uuid)
{entries}
end""".format(entries = entries.strip()).strip()

		output_path = script_dir.joinpath("Generated_VoiceMetaData").joinpath("{name}.lua".format(name=k))
		common.export_file(output_path, output)

print("Completed in {} seconds.".format(timeit.timeit(Run, number=1)))