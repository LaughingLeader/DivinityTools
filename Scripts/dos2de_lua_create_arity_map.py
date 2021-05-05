import os
from pathlib import Path
from typing import List,Dict
import operator
from collections import OrderedDict
import re

import dos2de_common as Common

events = {}

event_pattern = re.compile('^event (.*?)\((.*)\) .*$', re.MULTILINE | re.IGNORECASE)

output_template = """
OsirisEvents = {{
{entries}
}}
"""

entry_template = "\t{name} = {arity},"

entry_text = ""

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)
output_path = Path(script_dir.joinpath("Generated").joinpath("OsirisEvents.lua"))

with open("G:\Divinity Original Sin 2\DefEd\Data\Mods\LeaderLib_543d653f-446c-43d8-8916-54670ce24dd9\Story\RawFiles\story_header.div", 'r', encoding='utf-8') as f:
	matches = event_pattern.findall(f.read())
	for m in matches:
		name = m[0]
		params = m[1]
		arity = len(str.split(params, ","))
		#print(name, arity)
		events[name] = arity
	entry_text = "\n".join(entry_template.format(name=k, arity=events[k]) for k in sorted(events.keys()))
	Common.export_file(output_path, output_template.format(entries=entry_text).strip())
