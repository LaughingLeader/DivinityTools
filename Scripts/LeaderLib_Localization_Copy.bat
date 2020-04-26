@echo off
setlocal enabledelayedexpansion

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_copy_localization.py "G:\Divinity Original Sin 2\DefEd\Data\Mods\LeaderLib_543d653f-446c-43d8-8916-54670ce24dd9\Localization\English\english.xml" "G:\Divinity Original Sin 2\DefEd\Data\Mods\LeaderLib_543d653f-446c-43d8-8916-54670ce24dd9\Localization" >>"%LogFile%" 2>&1

Exit /b