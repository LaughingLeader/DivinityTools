from bs4 import BeautifulSoup
from bs4 import Tag
import os
from pathlib import Path
import glob
import dos2de_common as Common
from typing import List, Dict

english = Common.GetEnglishLocalization("G:/Modding/DOS2DE/Projects_Source/DivinityTools/Scripts/_Data_Characters/english.xml")

class LocaleEntry():
    def __init__(self, node:Tag):
        content_node = node.find("attribute", attrs={"id":"Content"})
        self.handle = content_node["handle"]
        self.key = Common.GetAttributeNodeValue(node, "UUID")
        self.stub_content = content_node["value"]
        self.content = ""
        if self.handle != "" and self.handle in english.keys():
            self.content = english[self.handle]

class LocaleFile():
    def __init__(self, path:Path):
        self.path = path
        self.name = path.stem
        self.entries: List[LocaleEntry] = []

def GetLocaleFiles()->List[LocaleFile]:
    lsx_files: List[Path] = list(Path("G:\Modding\DOS2DE\Projects_Source\DivinityTools\Scripts\_Data_Localization").rglob("*.lsx"))

    locale_files: List[LocaleFile] = []

    for p in lsx_files:
        file_entry = LocaleFile(p)
        locale_files.append(file_entry)

        print("Reading file '{}'".format(p))
        f = open(p, 'r')
        lsx_xml = BeautifulSoup(f.read(), 'lxml')
        f.close()

        nodes:List[Tag] = list(lsx_xml.find_all("node", attrs={"id":"TranslatedStringKey"}))
        for node in nodes:
            entry = LocaleEntry(node)
            file_entry.entries.append(entry)
    return locale_files

def GetLocaleEntries()->List[LocaleEntry]:
    locale_files = GetLocaleFiles()
    entries = [x.entries for x in locale_files.values()]
    return entries

locale_files = GetLocaleFiles()
output_tsv = "Key\tContent\tHandle\n"

for file_entry in locale_files:
    for entry in file_entry.entries:
        output_tsv += "{}\t{}\t{}\n".format(entry.key, entry.content, entry.handle)

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir.resolve())

output_path = script_dir.joinpath("Generated_Localization").joinpath("Stats.tsv")
Common.export_file(output_path, output_tsv)