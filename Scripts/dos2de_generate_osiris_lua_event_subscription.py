import os
from pathlib import Path
from sre_constants import REPEAT
from typing import List,Dict
import operator
from collections import OrderedDict
import re

import dos2de_common as Common

event_pattern = re.compile('^event (.*?)\((.*)\) .*$', re.MULTILINE | re.IGNORECASE)
query_pattern = re.compile('^query (\w+)\((.*)\) .*$', re.MULTILINE | re.IGNORECASE)

output_template = """
IF
{name}({placeholders})
THEN
DB_NOOP(1);
"""

query_template = "AND {name}({placeholders})\n"

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)
output_path = Path(script_dir.joinpath("Generated").joinpath("OsirisLuaEventSubscription.txt"))

def process_header():
    with open("G:\Divinity Original Sin 2\DefEd\Data\Mods\LeaderLib_543d653f-446c-43d8-8916-54670ce24dd9\Story\RawFiles\story_header.div", 'r', encoding='utf-8') as f:
        output_txt = ""
        txt = f.read()
        for m in event_pattern.findall(txt):
            name = m[0]
            params = m[1]
            arity = 0
            if params.strip() != "":
                arity = len(str.split(params, ","))
            if arity > 1:
                paramText = ",".join(list(("_" * arity)))
                output_txt = output_txt + str.format(output_template, name=name, placeholders=paramText)
            elif arity == 1:
                output_txt = output_txt + str.format(output_template, name=name, placeholders="_")
            else:
                output_txt = output_txt + str.format(output_template, name=name, placeholders="")
        
        added_query_event = False
        ignore_qry = [
            #"NRD_",
            "NRD_ModQuery",
            "NRD_LuaQuery",
            "NRD_LoadFile",
            "CharacterGetHostCharacter",
            "LeaderLib_Ext_QRY",
            "CharacterGetHostCharacter",
            "CharacterGetEquippedWeapon",
        ]
        def ignoreQuery(name):
            for n in ignore_qry:
                if n in name:
                    return True
        for m2 in sorted(query_pattern.findall(txt)):
            if not added_query_event:
                #event NRD_StatusIteratorEvent((STRING)_Event, (GUIDSTRING)_Object, (STRING)_StatusId, (INTEGER64)_StatusHandle) (3,1600,2,1)
                output_txt = output_txt + "\nIF\nNRD_StatusIteratorEvent(_Event, _Object, _Status, _Handle)\nAND CharacterGetHostCharacter(_Char)\nAND CharacterGetEquippedWeapon(_Char, _Item)\n"
                added_query_event = True
            name = m2[0]
            if ignoreQuery(name):
                continue

            paramText = m2[1]
            arity = 0
            params:List[str] = []
            if paramText.strip() != "":
                paramText = re.sub("\[in\]\(STRING\)_\w+", "\"\"", paramText, 0, re.MULTILINE)
                paramText = re.sub("\[in\]\(GUIDSTRING\)_\w+", "(GUIDSTRING)_Object", paramText, 0, re.MULTILINE)
                paramText = re.sub("\[in\]\(ITEMGUID\)_\w+", "(ITEMGUID)_Item", paramText, 0, re.MULTILINE)
                paramText = re.sub("\[in\]\(CHARACTERGUID\)_\w+", "(CHARACTERGUID)_Char", paramText, 0, re.MULTILINE)
                paramText = re.sub("\[in\]\(TRIGGERGUID\)_\w+", "TRIGGERGUID_S_ARX_OutsideArx_70258644-e81b-43b0-872c-d695cc32cdeb", paramText, 0, re.MULTILINE)
                #paramText = re.sub("\[in\]\(LEVELTEMPLATEGUID\)_\w+", "(LEVELTEMPLATEGUID)_Object", paramText, 0, re.MULTILINE)
                #paramText = re.sub("\[in\]\(SPLINEGUID\)_\w+", "(SPLINEGUID)_Object", paramText, 0, re.MULTILINE)
                paramText = re.sub("\[in\]\(INTEGER\)_\w+", "0", paramText, 0, re.MULTILINE)
                paramText = re.sub("\[in\]\(INTEGER64\)_\w+", "_Handle", paramText, 0, re.MULTILINE)
                paramText = re.sub("\[in\]\(REAL\)_\w+", "0.0", paramText, 0, re.MULTILINE)
                # paramText = str.replace(paramText, "[in]", "")
                paramText = re.sub("\[out\]\(\w+\)_\w+", "_", paramText, 0, re.MULTILINE)
                params = [x.strip() for x in str.split(paramText, ",")]
                arity = len(params)
            paramText = ", ".join(params)
            output_txt = output_txt + query_template.format(name=name,placeholders=paramText)
        if added_query_event:
            output_txt = output_txt + "THEN\nDB_NOOP(1);"
        Common.export_file(output_path, output_txt.strip())

process_header()