@echo off
setlocal enabledelayedexpansion

set input=D:\Modding\DOS2DE\WWise_Projects\WeaponExpansion\GeneratedSoundBanks\Windows
set output=G:\Divinity Original Sin 2\DefEd\Data\Public\WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f\Assets\Sound

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_soundbank_setup.py %input% "%output%" >>"%LogFile%" 2>&1

Exit /b
