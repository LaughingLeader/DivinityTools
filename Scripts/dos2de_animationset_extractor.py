from bs4 import BeautifulSoup
import os
import sys
import pathlib
from pathlib import Path
import shutil

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

sys.path.insert(0, "G:/Modding/DOS2DE/Projects_Source/DivinityTools/Scripts/lsf_scripts/")

import clr

clr.AddReference("G:/Modding/DOS2DE/Projects_Source/DivinityTools/Scripts/lsf_scripts/LSLib.dll")

input_file = Path('G:/Modding/DOS2DE/Projects_Source/AnimatonsPlus/_Backup/LLANIM_Dwarves_Male_ABC_AnimationsPlus_Custom_ebf6edc1-ed7f-44bc-9577-e00e65de9d30sx.lsf')

from LSLib.LS import ResourceUtils

res = ResourceUtils.LoadResource(input_file)
ResourceUtils.SaveResource(res, script_dir.joinpath("test.lsx"))