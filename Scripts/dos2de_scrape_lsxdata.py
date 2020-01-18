import os
from pathlib import Path
from bs4 import BeautifulSoup
import dos2de_common as common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

data_folder = Path("D:/Modding/DOS2DE_Extracted/Mods")

meta_files = data_folder.glob("meta.lsx")