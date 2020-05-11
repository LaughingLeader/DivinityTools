@echo off
setlocal enabledelayedexpansion

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_copy_localization.py "G:\Divinity Original Sin 2\DefEd\Data\Mods\BarteringTweaks_27db95b3-6850-48c5-baec-3a1f2df9a825\Localization\English\english.xml" "G:\Divinity Original Sin 2\DefEd\Data\Mods\BarteringTweaks_27db95b3-6850-48c5-baec-3a1f2df9a825\Localization" >>"%LogFile%" 2>&1

Exit /b