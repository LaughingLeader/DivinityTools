from bs4 import BeautifulSoup
from bs4 import Tag
import os
from pathlib import Path
import dos2de_common as Common
from typing import List, Dict

english_xml = Common.GetEnglishLocalization("D:/Modding/DOS2DE_Extracted/Localization/English/english.xml")
stringkeyfiles_dir = Path("D:/Modding/DOS2DE_Extracted/Public/Shared/Localization/Stats")

skilldata_path = Path("D:/Modding/DOS2DE_Extracted/SkillData.txt")
statusdata_path = Path("D:/Modding/DOS2DE_Extracted/StatusData.txt")

stringkey_data = {}

class LocaleEntry():
    def __init__(self, node:Tag):
        content_node = node.find("attribute", attrs={"id":"Content"})
        self.handle = content_node["handle"]
        self.key = Common.GetAttributeNodeValue(node, "UUID")
        self.stub_content = content_node["value"]
        self.content = ""
        if self.handle != "":
            self.content = english_xml.get(self.handle, self.stub_content)
        stringkey_data[self.key] = self

class LocaleFile():
    def __init__(self, path:Path):
        self.path = path
        self.name = path.stem
        self.entries: List[LocaleEntry] = []

def GetLocaleFiles()->List[LocaleFile]:
    lsx_files: List[Path] = list(stringkeyfiles_dir.rglob("*.lsx"))

    locale_files: List[LocaleFile] = []

    for p in lsx_files:
        file_entry = LocaleFile(p)
        locale_files.append(file_entry)

        print("Reading file '{}'".format(p))
        f = open(p, 'r', encoding='utf-8')
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

output_lines = []

for file_entry in locale_files:
    for entry in file_entry.entries:
        output_lines.append("{}\t{}\t{}\n".format(entry.key, entry.content, entry.handle))

output_lines = sorted(output_lines)
output_tsv += "".join(output_lines)

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir.resolve())

output_path = script_dir.joinpath("Generated_Localization").joinpath("Stats.tsv")
Common.export_file(output_path, output_tsv)

import re
displayname_pattern = re.compile('data "DisplayNameRef" "(.*)"', re.MULTILINE | re.IGNORECASE)

key_properties = {
    '"DisplayName"': '"DisplayNameRef"',
    '"Description"': '"DescriptionRef"',
}

def update_stats_text():
    files = [skilldata_path, statusdata_path]
    for p in files:
        with p.open(mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for i,line in enumerate(lines):
                if line != "":
                    for keyatt,refatt in key_properties.items():
                        if keyatt in line:
                            pattern = f'data {keyatt} "(.*)"'
                            m = re.match(pattern, line, re.IGNORECASE)
                            if m:
                                key = m.group(1)
                                print(key)
                                if key and key != "":
                                    entry = stringkey_data.get(key)
                                    if entry:
                                        ref = lines[i+1]
                                        if refatt in ref:
                                            #lines[i+1] = f'data {refatt} "{entry.content}"//{entry.handle}\n'
                                            lines[i+1] = f'data {refatt} "{entry.content}"\n'
            
            print(p.name)
            output_path = script_dir.joinpath("Generated_Localization").joinpath(p.name)
            Common.export_file(output_path, "".join(lines))

update_stats_text()