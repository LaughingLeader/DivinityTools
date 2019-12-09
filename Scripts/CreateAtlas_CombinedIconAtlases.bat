@echo off
setlocal enabledelayedexpansion

set icons=D:\Modding\DOS2DE\Projects_Source\CombinedAtlases\icons_export
set atlas=G:\Divinity Original Sin 2\DefEd\Data\Public\CombinedIconAtlases_ba1c5d97-0948-4758-ac94-beebe49c7a8a\GUI\AllIcons_Merged.lsx
set texture=D:\Modding\DOS2DE\Projects_Source\CombinedAtlases\AllIcons_Merged.png
set dds_export=G:\Divinity Original Sin 2\DefEd\Data\Public\CombinedIconAtlases_ba1c5d97-0948-4758-ac94-beebe49c7a8a\Assets\Textures\Icons\AllIcons_Merged.dds
set uuid=94406648-2f62-4533-988b-6c6767de44f9

set "LogFile=%~n0_Log.txt"

If Exist "%LogFile%" Del "%LogFile%"

py dos2de_create_atlas.py "%icons%" "%atlas%" "%texture%" "%uuid%" "%dds_export%" >>"%LogFile%" 2>&1

Exit /b

