from bs4 import BeautifulSoup,Tag
import os
from pathlib import Path
import glob
import dos2de_common as Common
from typing import List, Dict
import sys
import traceback
import subprocess

root_dir = Path("G:\SourceControlGenerator\Data\Divinity Original Sin 2 - Definitive Edition\Projects\EnemyUpgradeOverhaul")
os.chdir(root_dir)

scripts_dir = root_dir.joinpath("Mods\EnemyUpgradeOverhaul_046aafd8-ba66-4b37-adfb-519c1a5d04d7\Story\RawFiles\Lua")
#G:\Divinity Original Sin 2\DefEd\Data\Mods\EnemyUpgradeOverhaul_046aafd8-ba66-4b37-adfb-519c1a5d04d7\Story\RawFiles\Lua

files:List[Path] = list(scripts_dir.rglob("*.lua"))

def gitRename(source:str, newPath:str):
	p = subprocess.run(["git", 
		"mv",
		source,
		newPath], 
		universal_newlines=True, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)

for f in files:
	if "LLENEMY_" in f.name:
		new_name = f.name.replace("LLENEMY_", "")
		nextPath = f.parent.joinpath(new_name).with_suffix(".lua")
		sourcePath = str(f.absolute()).replace(str(root_dir.absolute())+"\\", "")
		newPath = str(nextPath.absolute()).replace(str(root_dir.absolute())+"\\", "")
		print("Renaming {} to {}".format(sourcePath, newPath))
		gitRename(sourcePath, newPath)
