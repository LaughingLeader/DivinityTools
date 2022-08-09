from pathlib import Path
import asyncio
import subprocess
import argparse
import os
import datetime

data_paks = [
    "Game.pak",
    "GamePlatform.pak",
    "Engine.pak",
    "EngineShaders.pak",
    # "Effects.pak",
    "Icons.pak",
    # "LowTex.pak",
    # "Materials.pak",
    # "Minimaps.pak",
    # "SharedSoundBanks.pak",
    # "SharedSounds.pak",
    # "Textures.pak",
    "Shared.pak",
    "SharedDOS.pak",
    "Arena.pak",
    "GameMaster.pak",
    "Origins.pak",
    "Squirrel.pak",
    "Localization/English.pak",
    # "Localization/Video.pak",
    # "Localization/Voice.pak",
    # "Localization/Amlatspanish/Amlatspanish.pak",
    # "Localization/Chinese/Chinese.pak",
    # "Localization/Chinese/ChineseData.pak",
    # "Localization/Chinesetraditional/Chinesetraditional.pak",
    # "Localization/Chinesetraditional/ChinesetraditionalData.pak",
    # "Localization/Czech/Czech.pak",
    # "Localization/French/French.pak",
    # "Localization/German/German.pak",
    # "Localization/Italian/Italian.pak",
    # "Localization/Japanese/Japanese.pak",
    # "Localization/Japanese/JapaneseData.pak",
    # "Localization/Korean/Korean.pak",
    # "Localization/Korean/KoreanData.pak",
    # "Localization/Polish/Polish.pak",
    # "Localization/Portuguesebrazil/Portuguesebrazil.pak",
    # "Localization/Russian/Russian.pak",
    # "Localization/Spanish/Spanish.pak",
    "Patch1.pak",
    "Patch1_Hotfix1.pak",
    "Patch1_Hotfix2.pak",
    "Patch1_Hotfix4.pak",
    "Patch1_TDE.pak",
    "Patch2.pak",
    "Patch3.pak",
    "Patch4.pak",
    "Patch4-1.pak",
    "Patch5.pak",
    "Patch1_Gold.pak",
    "Patch6.pak",
    "Patch7.pak",
    "Patch7_Hotfix.pak",
    "Patch8.pak",
    "Patch10.pak",
]

default_data_path = os.environ.get("DOS2_PATH", None)
default_divine_path = os.environ.get("LSLIB_PATH", None)

if default_data_path is not None:
    default_data_path = Path(default_data_path)
    if default_data_path.exists() and not "DefEd/Data" in default_data_path.absolute():
        default_data_path = default_data_path.joinpath("DefEd/Data")

if default_divine_path is not None:
    default_divine_path = Path(default_divine_path)
    if default_divine_path.exists() and default_divine_path.joinpath("divine.exe").exists():
        default_divine_path = default_divine_path.joinpath("divine.exe")

default_extract_path = Path( __file__ ).parent.joinpath("/GameData_Extracted_{}".format(datetime.datetime.now().timestamp()))

async def extract_pak_async(f:Path, divine:Path, output:Path):
    targs = [
        divine.absolute(),
        "-g dos2de",
        f'-s "{f.absolute()}"',
        "-a extract-package",
        f'-d "{output.absolute()}"',
        "-i pak"
    ]
    cmd = " ".join(targs)
    proc = await asyncio.create_subprocess_shell(
        cmd,
        universal_newlines=False,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[divine] exited with {proc.returncode}]')
    encoding = "ISO-8859-1"
    if stdout:
        print(f'[divine]\n{stdout.decode(encoding)}')
    if stderr:
        print(f'[divine]\n{stderr.decode(encoding)}')

async def extract_pak(f:Path, divine:Path, output:Path):
    targs = [
        divine.absolute(),
        "-g dos2de",
        f'-s "{f.absolute()}"',
        "-a extract-package",
        f'-d "{output.absolute()}"',
        "-i pak"
    ]
    cmd = " ".join(targs)
    proc = subprocess.run(
        cmd,
        universal_newlines=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)

    print(f'[divine] exited with {proc.returncode}]')
    if proc.returncode == 0:
        print(f'[divine]\n{proc.stdout}')
        return True
    else:
        print(f'[divine] Error:\n{proc.stderr}')
        return False

def main():
    parser = argparse.ArgumentParser(description='Extract all game data paks in order.')
    parser.add_argument("-d", "--data", type=Path, default=default_data_path, help='The game data directory, such as Divinity Original Sin 2\DefEd\Data')
    parser.add_argument("-o", "--output", type=Path, default=default_extract_path, help='The directory to extract files to.')
    parser.add_argument("-l", "--divine", type=Path, default=default_divine_path, help='The path to divine.exe.')
    args = parser.parse_args()

    if args.data is not None and args.output is not None and args.divine is not None:
        data_dir:Path = args.data
        output_dir:Path = args.output
        divine_path:Path = args.divine

        if divine_path.is_dir():
            divine_path = divine_path.parent.joinpath("divine.exe")
            if not divine_path.exists():
                parser.print_help()
                os.error("Path to divine.exe is not set.")
                return False

        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Extracting all game data paks to {output_dir}")
        successes = 0
        errors = 0
        for pak_name in data_paks:
            pak_path = data_dir.joinpath(f"/{pak_name}")
            if pak_path.exists():
                if extract_pak(pak_path, divine_path, output_dir):
                    successes = successes + 1
                else:
                    errors = errors + 1
        total = successes + errors
        print(f"Processed {total} paks. Successes({successes}) Errors({errors})")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()