from datetime import datetime
import sys
from bs4 import BeautifulSoup,Tag
import os
from pathlib import Path
from typing import List, Dict
import traceback
import argparse
import dos2de_common as common

script_name = Path(__file__).stem
common.clear_log(script_name)

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
    resourceNode = xmlobj.find("node", attrs={"id":"Resource"})
    if resourceNode != None:
        uuid = get_attribute(xmlobj, "ID")
    else:
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
                common.log(script_name, f"'{finalName}' already exists. Skipping.")
    except Exception as e:
        common.log(script_name, f"Error renaming file:\n{e}")

common.log(script_name, f"Checking args. {sys.argv}")

try:
    parser = argparse.ArgumentParser(description='Rename lsx files to their Name_UUID.')
    parser.add_argument("-f", "--files", type=str, help='Selection of files to include, separated with ;')
    parser.add_argument("--cwd", type=str, help='The working directory.')
    args = parser.parse_args()
    
    cwd:Path = Path(os.getcwd())
    cwd_set = False
    
    if args.cwd:
        cwd:Path = Path(args.cwd)
        if not cwd.is_dir():
            cwd = cwd.parent
        os.chdir(cwd)
        common.log(script_name, f"Setting working directory to:\n{cwd}")
        cwd_set = True
        
    if args.files is not None:
        common.log(script_name, f"Processing files:\n{args.files}")
        if cwd_set:
            files:List[Path] = [cwd.joinpath(s) for s in args.files.split(";")]
        else:
            files:List[Path] = [Path(s) for s in args.files.split(";")]
        for filePath in files:
            common.log(script_name, f"File:\n{filePath}")
            if filePath.exists():
                if filePath.is_dir():
                    template_lsx_files:List[Path] = list(filePath.rglob("*.lsx"))
                    for f in template_lsx_files:
                        try:
                            rename(f)
                        except Exception as e:
                            common.log(script_name, f"Error renaming file:\n{e}")
                elif filePath.is_file() and filePath.suffix.lower() == ".lsx":
                    try:
                        rename(filePath)
                    except Exception as e:
                        common.log(script_name, f"Error renaming file:\n{e}")
            else:
                common.log(script_name, f"File does not exist:\n{filePath}")
    else:
        common.log(script_name, "No files passed. Skipping.")
except Exception as e:
    common.log(script_name, f"Error renaming files:\n{e}")

common.log(script_name, "All done.")