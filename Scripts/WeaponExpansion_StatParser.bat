@echo off
setlocal enabledelayedexpansion

set parser=D:\Projects\_Visual_Studio\lslib\StatParser\bin\Debug\StatParser.exe
set data=G:\Divinity Original Sin 2\DefEd\Data
set sod=G:\Divinity Original Sin 2\DefEd\Data\Editor\Config\Stats
set mod=WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f
set packages=D:\Users\LaughingLeader\Documents\Larian Studios\Divinity Original Sin 2 Definitive Edition\Local Mods

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

rem "D:\Projects\_Visual_Studio\lslib\StatParser\bin\Debug\StatParser.exe" --game-data-path "G:\Divinity Original Sin 2\DefEd\Data" --sod-path "G:\Divinity Original Sin 2\DefEd\Data\Editor\Config\Stats" --no-packages --mod WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f

rem "%parser%" --game-data-path "%data%" --sod-path "%sod%" --package-paths "%packages%" --mod "%mod%" >>"%LogFile%" 2>&1
"%parser%" --game-data-path "%data%" --sod-path "%sod%" --no-packages --mod "%mod%" >>"%LogFile%" 2>&1

rem @pause
