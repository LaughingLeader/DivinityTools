import os
from pathlib import Path
from typing import List, Dict
import subprocess
from bs4 import BeautifulSoup,Tag
import sys
import traceback
import argparse

parser = argparse.ArgumentParser(description='Convert files to lsf/lsx and back.')
parser.add_argument("-f", "--files", type=str, help='Selection of files to include, separated with ;')
args = parser.parse_args()

divine_path = Path("G:/Modding/DOS2DE/ConverterApp/divine.exe")

def get_attribute(xml, id):
    v = xml.find("attribute", attrs={"id":id})
    if v is not None:
        try:
            inner = v["value"]
            return inner
        except: pass
    return ""

validTypes = [
    "lsx",
    "lsb",
    "lsf",
]

def convertFile(filePath:Path):
    if type(filePath) == str:
        filePath = Path(filePath)
    inType = filePath.suffix.lower().replace(".", "")
    if inType in validTypes:
        outType = "lsx"
        if inType == "lsx":
            try:
                with filePath.open('r', encoding='utf-8') as f:
                    lsx_xml = BeautifulSoup(f.read(), 'lxml')
                    shouldBeLSB = lsx_xml.find("region", attrs={"id":"TranslatedStringKeys"}) is not None
                    if shouldBeLSB:
                        outType = "lsb"
                    else:
                        outType = "lsf"
            except Exception as e:
                print("Error opening file '{}':".format(filePath))
                traceback.print_exc()
                outType = "lsf"

        output_name = str(filePath.with_suffix("." + outType).absolute())
        p = subprocess.run([str(divine_path.absolute()), 
            "-g", 
            "dos2de",
            "-l", 
            "all",
            "-s",
            str(filePath.absolute()),
            "-a",
            "convert-resource",
            "-d",
            output_name,
            "-i",
            inType,
            "-o",
            outType
            ], 
            universal_newlines=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        if p.returncode == 0 and Path(output_name).exists():
            print("Converted {} to {}.".format(filePath, output_name))
        print("Result: ({}):\n{}".format(p.returncode, p.stdout))

try:
    if args.files is not None:
        files:List[Path] = [Path(s) for s in args.files.split(";")]
        for filePath in files:
            if filePath.is_dir():
                subFiles:List[Path] = []
                subFiles.extend(filePath.rglob("*.lsx"))
                subFiles.extend(filePath.rglob("*.lsb"))
                subFiles.extend(filePath.rglob("*.lsf"))
                for f in subFiles:
                    try:
                        convertFile(f)
                    except Exception as e:
                        print("Error converting file '{}':".format(f))
                        traceback.print_exc()
            else:
                try:
                    convertFile(filePath)
                except Exception as e:
                    print("Error converting file '{}':".format(filePath))
                    traceback.print_exc()
except Exception as e:
    print("Error converting files:\n")
    traceback.print_exc()