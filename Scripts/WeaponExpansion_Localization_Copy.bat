@echo off
setlocal enabledelayedexpansion

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_copy_localization.py "G:\Divinity Original Sin 2\DefEd\Data\Mods\WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f\Localization\English\english.xml" "G:\Divinity Original Sin 2\DefEd\Data\Mods\WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f\Localization" >>"%LogFile%" 2>&1

Exit /b