@echo off
setlocal enabledelayedexpansion

set icons=G:\Modding\DOS2DE\Projects_Source\LeaderLib\Icons_Shared
set atlas=G:\Divinity Original Sin 2\DefEd\Data\Public\LeaderLib_543d653f-446c-43d8-8916-54670ce24dd9\GUI\LeaderLib_SharedIcons.lsx
set texture=G:\Modding\DOS2DE\Projects_Source\DivinityTools\Scripts\LeaderLib_SharedIcons.png
set dds=G:\Divinity Original Sin 2\DefEd\Data\Public\LeaderLib_543d653f-446c-43d8-8916-54670ce24dd9\Assets\Textures\Icons\LeaderLib_SharedIcons.dds
set uuid=7edbcc6f-1325-4566-8f47-e014dedec2fb

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_create_atlas.py %icons% "%atlas%" "%texture%" %uuid% "%dds%" >>"%LogFile%" 2>&1

Exit /b

