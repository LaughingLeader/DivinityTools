import json
from pathlib import Path
from typing import List,Dict
import operator
from collections import OrderedDict

import dos2de_common as Common

base = [
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Default\\inputconfig.json",
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Default\\inputconfig_controller.json",
]

files = [
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\keyboard_1.json",
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\controller_1.json",
    "D:\\Users\\LaughingLeader\\Documents\\Larian Studios\\Divinity Original Sin 2 Definitive Edition\\PlayerProfiles\\LaughingLeader\\inputconfig_p1.json",
]

debug_files = [
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\keyboard_debug.json",
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\controller_debug.json",
]

ignored = [
    "FlashMouseMove"
]

def ignore_input(key):
    for k in ignored:
        if k in key:
            return True
    return False

def get_keys(enable_debug=True)->Dict[str,List[str]]:
    inputEvents:Dict[str,List[str]] = {}

    target_files = []
    target_files.extend(base)
    target_files.extend(files)
    if enable_debug:
        target_files.extend(debug_files)

    for fpath in target_files:
        f = Path(fpath)
        contents = Common.load_file(f)
        if contents is not None:
            jdata = json.loads(contents)
            for k,v in jdata.items():
                saved:List[str] = inputEvents.get(k)
                if saved is None:
                    inputEvents[k] = []
                    saved = inputEvents[k]
                for key in v:
                    if not key in saved:
                        saved.append(key)
    with open('Generated/input-all.json', 'w', encoding='utf-8') as fp:
        #json.dump(inputEvents, fp, indent='\t')
        fp.write(Common.to_json(OrderedDict(sorted(inputEvents.items()))))
    return inputEvents

def export_flash(inputEvents=None):
    inputEvents = inputEvents or get_keys(False)
    events_str = ",".join(['"IE {}"'.format(x) for x in sorted(inputEvents.keys()) if not ignore_input(x)])
    output_str = "this.events = new Array({});".format(events_str)
    Common.export_file(Path("Generated/FlashInputEvents.txt"), output_str)