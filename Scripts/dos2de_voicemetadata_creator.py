from bs4 import BeautifulSoup
import os
from pathlib import Path
import glob
import dos2de_common as common
import timeit

metadata_master = "D:\Modding\DOS2DE_Extracted\Localization\English\Soundbanks\VoiceMetaData.lsx"
template_entry = "Ext.AddVoiceMetaData(\"{speaker}\", \"{handle}\", \"Localization/English/Soundbanks/{file}\", {length})\n"
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
		return template_entry.format(speaker=uuid, handle=self.handle, file=self.audioFile, length=self.length)

voice_entries = []

def get_data(lsx_path:str, speakerId:str, nextSpeaker:str)->str:
	print("Reading file '{}'".format(lsx_path))
	lsx_xml = None
	f = open(lsx_path, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	speaker_node = None
	speaker_entries = list(lsx_xml.find_all("node", attrs={"id":"VoiceSpeakerMetaData"}))
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

def Run():
	voice_warrior_male1 = "7b6c1f26-fe4e-40bd-a5d0-e6ff58cef4fe"
	voice_scholar_male1 = "41a06985-7851-4c29-8a78-398ccb313f39"

	harken = "e446752a-13cc-4a88-a32e-5df244c90d8b" # Harken
	korvash = "3f20ae14-5339-4913-98f1-24476861ebd6" # Korvash

	entries = get_data(metadata_master, voice_scholar_male1, korvash)
	output = """function Init()
	{entries}
	end
	return Init
	""".format(entries = entries)

	output_path = script_dir.joinpath("Generated_VoiceMetaData").joinpath("VoiceMetaDataEntries_{uuid}.lua".format(uuid=korvash))
	common.export_file(output_path, output)

print("Completed in {} seconds.".format(timeit.timeit(Run, number=1)))