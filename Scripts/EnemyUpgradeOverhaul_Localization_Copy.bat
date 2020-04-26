@echo off
setlocal enabledelayedexpansion

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_copy_localization.py "G:\Divinity Original Sin 2\DefEd\Data\Mods\EnemyUpgradeOverhaul_046aafd8-ba66-4b37-adfb-519c1a5d04d7\Localization\English\english.xml" "G:\Divinity Original Sin 2\DefEd\Data\Mods\EnemyUpgradeOverhaul_046aafd8-ba66-4b37-adfb-519c1a5d04d7\Localization" >>"%LogFile%" 2>&1

Exit /b