from argparse import Action
from typing import Iterable
import lxml.etree as ET
import os
from pathlib import Path
import dos2de_common as common
import timeit

displayDialogLinesAsComments = True

ENGLISH_LOCALE = common.GetEnglishLocalization("D:/Modding/DOS2DE_Extracted/Localization/English/english.xml")

metadata_master = "D:\Modding\DOS2DE_Extracted\Localization\English\Soundbanks\VoiceMetaData.lsx"
template_entry = "_a(guid, \"{handle}\", \"Localization/English/Soundbanks/{file}\", {length})\n"
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

class VoiceEntry():
    def __init__(self, handle, audioFile, length):
        self.handle = handle
        self.audioFile = audioFile
        self.length = length

    def Export(self, uuid):
        output = template_entry.format(handle=self.handle, file=self.audioFile, length=self.length)
        if displayDialogLinesAsComments:
            translated = ENGLISH_LOCALE.get(self.handle, "")
            if translated != "":
                output = f"--{translated}\n{output}"
        return output

def Run():
    print("Reading file '{}'".format(metadata_master))

    speaker_entries:dict[str, ET._Element] = {}
    
    def get_guid(elem:ET._Element)->str|None:
        for child in elem.iterchildren("attribute"):
            if child.get("id") == "MapKey":
                return child.get("value")
        return None

    with open(metadata_master, "rb") as f:
        action:str
        elem:ET._Element
        for action, elem in ET.iterparse(f, tag="node"):
            if elem.get("id") == "VoiceSpeakerMetaData":
                guid = get_guid(elem)
                if guid is not None:
                    speaker_entries[guid] = elem

    def get_data(lsx_path:str, speakerId:str, nextSpeaker:str)->str:
        voice_entries = []
        speaker_node = speaker_entries.get(speakerId)

        if speaker_node is not None:
            child:ET._Element
            for child in speaker_node.iterdescendants("node"):
                if child.get("id") == "VoiceTextMetaData":
                    line_data = {}
                    has_data = False
                    for n in child.iterdescendants():
                        if n.tag == "attribute" and n.get("id") == "MapKey":
                            handle = n.get("value")
                            line_data["Handle"] = handle
                            has_data = handle != None
                        if n.tag == "node" and n.get("id") == "MapValue":
                            for attribute in n.iterchildren():
                                attr_id = attribute.get("id")
                                if attr_id is not None:
                                    line_data[attr_id] = attribute.get("value")
                    if has_data:
                        voiceEntry = VoiceEntry(line_data.get("Handle"), line_data.get("Source", ""), line_data.get("Length", "0"))
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
        #"Djinn": "838283f5-a45f-4892-a4ac-fae2f99d4de0",
        #"SallowMan": "d07e0f6b-c473-47f2-9d1c-e1f6f0ef61af",
        # "Harken": "e446752a-13cc-4a88-a32e-5df244c90d8b",
        # "Korvash": "3f20ae14-5339-4913-98f1-24476861ebd6",
    }
    for k,v in Voices.items():
        entries = get_data(metadata_master, v, "")
        #entries = get_data(metadata_master, voice_scholar_male1, korvash)
        output = """---@diagnostic disable
local _a = Ext.Stats.AddVoiceMetaData
---@param uuid GUID
return function(uuid)
{entries}
end""".format(entries = entries.strip()).strip()
        output_path = script_dir.joinpath("Generated_VoiceMetaData").joinpath("{name}.lua".format(name=k))
        common.export_file(output_path, output)

print("Completed in {} seconds.".format(timeit.timeit(Run, number=1)))