@echo off
setlocal enabledelayedexpansion

set input=D:\Modding\DOS2DE\WWise_Projects\EnemyUpgradeOverhaul\GeneratedSoundBanks\Windows
set output=G:\Divinity Original Sin 2\DefEd\Data\Public\EnemyUpgradeOverhaul_046aafd8-ba66-4b37-adfb-519c1a5d04d7\Assets\Sound

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_soundbank_setup.py %input% "%output%" >>"%LogFile%" 2>&1

Exit /b
