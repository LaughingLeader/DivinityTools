@echo off
setlocal enabledelayedexpansion

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_copy_localization.py "G:\Divinity Original Sin 2\DefEd\Data\Mods\Mimicry_d9cac48f-1294-68f8-dd4d-b5ea38eaf2d6\Localization\English\english.xml" "G:\Divinity Original Sin 2\DefEd\Data\Mods\Mimicry_d9cac48f-1294-68f8-dd4d-b5ea38eaf2d6\Localization" >>"%LogFile%" 2>&1

Exit /b