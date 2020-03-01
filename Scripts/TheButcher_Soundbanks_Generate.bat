@echo off
setlocal enabledelayedexpansion

set input=D:\Modding\DOS2DE\WWise_Projects\TheButcher\GeneratedSoundBanks\Windows
set output=G:\Divinity Original Sin 2\DefEd\Data\Public\TheButcher_cef84a3a-1f20-40d7-a047-b27851febbf8\Assets\Sound

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_soundbank_setup.py %input% "%output%" >>"%LogFile%" 2>&1

Exit /b
