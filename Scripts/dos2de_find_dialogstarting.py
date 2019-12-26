from pathlib import Path
import re
import dos2de_common as common

scripts_folder = Path("D:/Modding/DOS2DE_Extracted/Mods/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Story/RawFiles/Goals")

scripts = list(scripts_folder.glob('*.txt'))

origin_ids = [
	"S_Player_Sebille_c8d55eaf-e4eb-466a-8f0d-6a9447b5b24c",
	"S_Player_Lohse_bb932b13-8ebf-4ab4-aac0-83e6924e4295",
	"S_Player_Red_Prince_a26a1efb-cdc8-4cf3-a7b2-b2f9544add6f",
	"S_Player_Ifan_ad9a3327-4456-42a7-9bf4-7ad60cc9e54f",
	"S_Player_Fane_02a77f1f-872b-49ca-91ab-32098c443beb",
	"S_Player_Beast_f25ca124-a4d2-427b-af62-df66df41a978",
	#"S_Player_GenericOrigin_7b6c1f26-fe4e-40bd-a5d0-e6ff58cef4fe",
]

#call_pattern = '^Proc_StartDialog(0,".*?",.*{origin}.*);/s*?$'
call_pattern_str = '^(.*Proc_StartDialog\(0,\".*?\",.*S_Player.*)$'
pattern = re.compile(call_pattern_str, re.MULTILINE | re.IGNORECASE)

params_pattern_str = '^.*Proc_StartDialog\(0,(\".*?\",.*)$'
params_pattern = re.compile(params_pattern_str)

ignore_vars = [
	"_Initiator",
	"_Magister",
	",_Player",
	"_Player,",
	"_Avatar"
]

def ignore_text(txt):
	for s in ignore_vars:
		if s in txt:
			return True
	return False

all_calls = []
for p in scripts:
	#print("Reading: " + p.stem)
	with open(p.absolute()) as f:
		file_str = f.read()
		matches = list(pattern.finditer(file_str))
		#if len(matches) > 0: print("Matches: {}".format(len(matches)))
		for m in matches:
			text = m.group(1)
			if text != "" and not text in all_calls:
				if not ignore_text(text):
					all_calls.append(text)

all_calls = sorted(all_calls)

print("Matches:{}".format(len(all_calls)))
print(*all_calls, sep="\n")

dialog_pattern_str = '^.*Proc_StartDialog\(0,(\".*?\").*S_Player.*$'
dialog_pattern = re.compile(dialog_pattern_str)

dialog_names = []
#blacklist_template = "LeaderLib_DialogOverride_Register_BlacklistDialogForRedirection({dialog});\n"
blacklist_template = "LeaderLib_DialogOverride_Register_BlacklistRedirection({dialog}\n"

for line in all_calls:
	m = dialog_pattern.match(line)
	if m:
		dialog = m.group(1)
		if dialog != "" and dialog != None and not dialog in dialog_names:
			dialog_names.append(dialog)

print("All dialogs:{}".format(len(dialog_names)))
print(*dialog_names, sep="\n")

clipboard_text = ""
#for dialog in sorted(dialog_names):
#	clipboard_text += blacklist_template.format(dialog=dialog)

for line in all_calls:
	m = params_pattern.match(line)
	if m:
		clipboard_text += blacklist_template.format(dialog=m.group(1))

common.clipboard_copy(clipboard_text)