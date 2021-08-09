from bs4 import BeautifulSoup,Tag
import os
from pathlib import Path
import glob
from typing import List, Dict
import sys
import traceback
import argparse

parser = argparse.ArgumentParser(description='Rename lsx files to their Name_UUID.')
parser.add_argument("-f", "--files", type=str, help='Selection of files to include, separated with ;')
args = parser.parse_args()

def get_attribute(xml, id):
    v = xml.find("attribute", attrs={"id":id})
    if v is not None:
        try:
            inner = v["value"]
            return inner
        except: pass
    return ""

def parse(xmlobj):
    name = get_attribute(xmlobj, "Name")
    materialName = get_attribute(xmlobj, "MaterialName")
    if materialName != "":
        name = materialName
    uuid = get_attribute(xmlobj, "MapKey")
    if uuid == "" or uuid == "-1":
        uuid = get_attribute(xmlobj, "ID")
    newName = "{}_{}".format(name, uuid)
    return newName

def rename(p:Path):
    try:
        #print("Reading file '{}'".format(p))
        lsx_xml = ""
        with p.open('r', encoding='utf-8') as f:
            lsx_xml = BeautifulSoup(f.read(), 'lxml')
        #game_object = next(iter(list(lsx_xml.find_all("node", attrs={"id":"GameObjects"}))))
        newName = parse(lsx_xml)
        if newName is not None:
            finalName = p.with_name(newName).with_suffix(".lsx")
            if not Path(finalName).exists():
                #print("Renaming '{}' => '{}'".format(p, finalName))
                os.rename(p.absolute(),finalName)
            else:
                print("'{}' already exists. Skipping.".format(p, finalName))
    except Exception as e:
        print("Error renaming file:\n")
        traceback.print_exc()

try:
    if args.files is not None:
        files:List[Path] = [Path(s) for s in args.files.split(";")]
        for filePath in files:
            if filePath.exists():
                if filePath.is_dir():
                    template_lsx_files:List[Path] = list(filePath.rglob("*.lsx"))
                    for f in template_lsx_files:
                        try:
                            rename(f)
                        except Exception as e:
                            print("Error renaming file '{}':".format(f))
                            traceback.print_exc()
                elif filePath.is_file() and filePath.suffix.lower() == ".lsx":
                    try:
                        rename(filePath)
                    except Exception as e:
                        print("Error renaming file '{}':".format(filePath))
                        traceback.print_exc()
except Exception as e:
    print("Error renaming files:\n")
    traceback.print_exc()