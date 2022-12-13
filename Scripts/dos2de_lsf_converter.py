import os
from pathlib import Path
from typing import List, Dict
import subprocess
from bs4 import BeautifulSoup,Tag
import sys
import traceback
import argparse

import dos2de_common as common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

script_name = Path(__file__).stem
common.clear_log(script_name)

common.log(script_name, f"Processing args: {';'.join(sys.argv)}")

parser = argparse.ArgumentParser(description='Convert files to lsf/lsx and back.')
parser.add_argument("-f", "--files", type=str, help='Selection of files to include, separated with ;')
args = parser.parse_args()

divine_path = Path(os.environ.get("LSLIB_PATH", __file__)).joinpath("divine.exe")


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

def convertFile(filePath:Path, game:str="dos2de")->bool|None:
    if type(filePath) == str:
        filePath = Path(filePath)
    inType = filePath.suffix.lower().replace(".", "")
    if inType in validTypes:
        outType = "lsx"
        if inType == "lsx":
            try:
                with filePath.open('r', encoding='utf-8') as f:
                    lsx_xml = BeautifulSoup(f.read(), 'lxml')
                    shouldBeLSB = lsx_xml.find("region", attrs={"id":"TranslatedStringKeys"}) is not None or Path(filePath.with_suffix(".lsb")).exists()
                    if shouldBeLSB:
                        outType = "lsb"
                    else:
                        outType = "lsf"
            except Exception as e:
                common.log(script_name, "Error opening file '{}':".format(filePath))
                traceback.print_exc()
                outType = "lsf"

        output_name = str(filePath.with_suffix("." + outType).absolute())
        success = False
        p = subprocess.run([str(divine_path.absolute()), 
            "-g", 
            game,
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
            common.log(script_name, common.trim(p.stdout))
            common.log(script_name, "Converted {} to {}.".format(filePath, output_name))
            success = True
        else:
            common.log(script_name, f"Error({p.returncode}):\n{common.trim(p.stdout)}")
        return success

def get_game(f:Path):
    for p in f.parents:
        if "Baldur's Gate 3" in p.name or "BG3" in p.name:
            return "bg3"
    return "dos2de"

try:
    common.log(script_name, f"Processing args: {args.files}")
    if args.files is not None:
        files:List[Path] = [Path(s) for s in args.files.split(";")]
        for filePath in files:
            if filePath.is_dir():
                common.log(script_name, f"Converting directory {filePath.name}")
                subFiles:List[Path] = []
                subFiles.extend(filePath.rglob("*.lsx"))
                subFiles.extend(filePath.rglob("*.lsb"))
                subFiles.extend(filePath.rglob("*.lsf"))
                for f in subFiles:
                    try:
                        convertFile(f)
                    except Exception as e:
                        common.log(script_name, "Error converting file '{}':".format(f))
                        traceback.print_exc()
            else:
                common.log(script_name, f"Converting {filePath.name}")
                game = get_game(filePath)
                try:
                    convertFile(filePath, game)
                except Exception as e:
                    common.log(script_name, "Error converting file '{}':".format(filePath))
                    traceback.print_exc()
except Exception as e:
    common.log(script_name, "Error converting files:\n")
    traceback.print_exc()
