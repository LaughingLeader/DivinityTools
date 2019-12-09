import os
from pathlib import Path

replacements = []

replacements.append(("1_SYS_CC_LV_Template_Full_001", "6"))
replacements.append(("1_SYS_CC_LV_Template_Full_A_004", "11"))
#replacements.append(("1_SYS_CC_LV_Template_Full_002", "6"))
#replacements.append(("1_SYS_Icon_Generation_000_SYS_CC_LV_Template_Full_002", "6"))
#replacements.append(("1_SYS_CC_LV_Template_Full_002", "6"))

def add_replace_definition(prefix, num, cc_num):
	global replacements
	replace = ("{}{}".format(prefix, num), str(cc_num))
	replacements.append(replace)

# for i in range(4):
# 	cc_num = i + 7
# 	add_replace_definition("1_SYS_CC_LV_Template_Full_A_00", i, cc_num)
# 	add_replace_definition("1_SYS_CC_LV_Template_Full_A_00", i, cc_num)
# 	add_replace_definition("1_SYS_Icon_Generation_000_SYS_CC_LV_Template_Full_A_00", i, cc_num)
# 	#add_replace_definition("1_SYS_CC_LV_Template_Full_A_00", i, cc_num)

files = []
files_dir = 'G:/Divinity Original Sin 2/DefEd/Data/Mods/PartySizeEvolved_01888044-40fa-4250-8934-add840ac23b7/Levels/SYS_Character_Creation_A/Triggers'

for file in os.listdir(files_dir):
    if file.endswith(".lsx"):
        files.append(os.path.join(files_dir, file))

for f in files:
	lines = []
	replaced = 0
	with open(f) as infile:
		for line in infile:
			#if "Cam_Zoom_1" in line:
			#	print(line)
			for src, target in replacements:
				new_line = line.replace(src, target)
				if new_line != line:
					replaced += 1
				line = new_line
			lines.append(line)
	if replaced > 0:
		print("Replaced {} lines in '{}'.".format(replaced, f))
		with open(f, 'w') as outfile:
			for line in lines:
				outfile.write(line)