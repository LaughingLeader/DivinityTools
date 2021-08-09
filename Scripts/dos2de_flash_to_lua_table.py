import os
from pathlib import Path
from typing import List,Dict
import operator
from collections import OrderedDict
import re
import argparse

import dos2de_common as Common

function_pattern = re.compile('public function (?P<name>.*?)\(.*$', re.MULTILINE | re.IGNORECASE)
call_pattern = re.compile('ExternalInterface.call\("(?P<name>.*?)"', re.MULTILINE | re.IGNORECASE)

ignoreMethods = [
    "MainTimeline",
    "onEventResize",
    "onEventResolution",
    "onEventUp",
    "onEventInit",
    "onEventDown",
]

type_map = {
    "Boolean" : "boolean",
    "Number" : "number",
    "uint" : "integer",
    "String" : "string",
    "*" : "any",
    "Array" : "table",
    "MovieClip" : "FlashMovieClip",
    "int" : "integer",
}

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

parser = argparse.ArgumentParser(description='Grab MainTimeline functions and ExternalInterface.call names.')
parser.add_argument("-d", "--directory", type=str, help='The directory to process.')
args = parser.parse_args()

if args.directory is not None:
    #target = target.replace('"', '').replace("\\", "/")
    dir_path = Path(args.directory)
    script_files:List[Path] = [p for p in dir_path.rglob('*.as')]
    output_path = Path(script_dir.joinpath("Generated/UIHooks").joinpath(str(dir_path.stem)).with_suffix('.txt'))
    output_txt = "{{{calls}}},\n{{{methods}}}"
    invokes = []
    calls = []
    for p in script_files:
        with open(p, 'r', encoding='utf-8') as f:
            input_txt = f.read()
            if "MainTimeline" in p.stem:
                for m in function_pattern.finditer(input_txt):
                    name = m.group('name')
                    if not name in invokes and not name in ignoreMethods:
                        invokes.append(name)
            else:
                for m in call_pattern.finditer(input_txt):
                    name = m.group('name')
                    if not name in calls:
                        calls.append(name)
    invokes.sort()
    calls.sort()
    output_txt = output_txt.format(calls=',\n'.join(['"{}"'.format(x) for x in calls]), methods=',\n'.join(['"{}"'.format(x) for x in invokes]))
    Common.export_file(output_path, output_txt.strip())