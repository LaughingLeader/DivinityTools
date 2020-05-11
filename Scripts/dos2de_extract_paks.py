import os
from pathlib import Path
import shutil
import subprocess
import dos2de_common as common

ignore_paks = [
#"Arena.pak",
#"Effects.pak",
#"Engine.pak",
#"EngineShaders.pak",
#"Game.pak",
#"GameMaster.pak",
#"GamePlatform.pak",
#"Icons.pak",
#"LowTex.pak",
#"Materials.pak",
#"Minimaps.pak",
#"Origins.pak",
#"Patch1.pak",
#"Patch1_Gold.pak",
#"Patch1_Hotfix1.pak",
#"Patch1_Hotfix2.pak",
#"Patch1_Hotfix4.pak",
#"Patch1_TDE.pak",
#"Patch2.pak",
#"Patch3.pak",
#"Patch4.pak",
"Patch4-1.pak",
#"Patch5.pak",
#"Patch6.pak",
#"Patch7.pak",
#"Patch7_Hotfix.pak",
#"Shared.pak",
#"SharedDOS.pak",
#"SharedSoundBanks.pak",
#"SharedSounds.pak",
"SharedSounds_1.pak",
#"Squirrel.pak",
"Textures.pak",
"Textures_1.pak",
"Textures_2.pak",
"Textures_3.pak",
"Textures_4.pak",
"Textures_5.pak",
"Textures_6.pak",
"Textures_7.pak",
"Textures_8.pak",
]

pak_output = Path("D:/_Temp/_Paks")
divine_path = Path("G:/Modding/DOS2DE/ConverterApp/divine.exe")
data_path = Path("G:/Divinity Original Sin 2/DefEd/Data")
divine_str = str(divine_path.absolute())

paks = list(data_path.rglob("*.pak"))

for f in paks:
	if not f.name in ignore_paks:
		output_folder = pak_output.joinpath(f.stem)
		if not output_folder.exists():
			output_folder.mkdir(parents=True, exist_ok=True)
			print("Extracting {}".format(f.name))
			p = subprocess.run([divine_str, 
				"-s",
				str(f),
				"-a",
				"extract-package",
				"-d",
				str(output_folder),
				"-i",
				"pak",
				], 
				universal_newlines=True, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)