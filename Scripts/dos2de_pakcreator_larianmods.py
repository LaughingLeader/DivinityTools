import os
from pathlib import Path
import shutil
import subprocess
import dos2de_common as common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

larianmod_names = [
    "AS_BlackCatPlus",
    "AS_GrowYourHerbs",
    "AS_ToggleSpeedAddon",
    "CMP_8AP_Kamil",
    "CMP_BarterTweaks",
    "CMP_CraftingOverhaul",
    "CMP_EnemyRandomizer_Kamil",
    "CMP_Free_PetPalTag_Kamil",
    "CMP_FTJRespec_Kamil",
    "CMP_LevelUpEquipment",
    "CMP_OrganizedContainers_Marek",
    "CMP_SummoningImproved_Kamil"
]

data_path_mods = Path("D:/Modding/DOS2DE_Extracted/Mods")
data_path_public = Path("D:/Modding/DOS2DE_Extracted/Public")
pak_output = Path("D:/Users/LaughingLeader/Documents/Larian Studios/Divinity Original Sin 2 Definitive Edition/Mods")
divine_path = Path("G:/Modding/DOS2DE/ConverterApp/divine.exe")

class PakData():
    def __init__(self, name, modfolder, publicfolder):
        self.name = name
        self.mods = modfolder
        self.public = publicfolder

paklist = []

for name in larianmod_names:
    modspath = data_path_mods.joinpath(name)
    publicpath = data_path_public.joinpath(name)
    #pakdata = PakData(name, modspath, publicpath)
    #paklist.append(pakdata)
    if modspath.exists() and publicpath.exists():
        tempfolder = script_dir.joinpath("_Temp-" + name)
        tempfolder.mkdir(parents=True, exist_ok=True)
        modsfolder = tempfolder.joinpath("Mods").joinpath(name)
        publicfolder = tempfolder.joinpath("Public").joinpath(name)
        #modsfolder.mkdir(parents=True, exist_ok=True)
        #publicfolder.mkdir(parents=True, exist_ok=True)
        print("Copying '{}' to '{}'".format(modspath.absolute(), modsfolder))
        print("Copying '{}' to '{}'".format(publicpath.absolute(), publicfolder))
        shutil.copytree(modspath.absolute(), modsfolder)
        shutil.copytree(publicpath.absolute(), publicfolder)

        divine_str = str(divine_path.absolute())
        temp_folder_str = str(tempfolder.absolute())

        p = subprocess.run([divine_str, 
            "-g", 
            "dos2de",
            "-a",
            "create-package",
            "-s",
            temp_folder_str,
            "-d",
            str(pak_output.joinpath(name).with_suffix(".pak").absolute()),
            "-c",
            "lz4",
            "-p",
            "v13"
            ], 
            universal_newlines=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        print(p.stdout)
        print(p.stderr)

        shutil.rmtree(temp_folder_str, ignore_errors=True)
