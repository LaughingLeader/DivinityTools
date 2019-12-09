from bs4 import BeautifulSoup

import os
import sys

import subprocess

import pathlib
from pathlib import Path

import re

animation_node_template = (
"""																<node id="Animation">
																	<attribute id="MapKey" value="{name}" type="22" />
																	<children>
																		<node id="MapValue">
																			<attribute id="ID" value="{uuid}" type="22" />
																			<attribute id="Name" value="{name}" type="22" />
																		</node>
																	</children>
																</node>""")

custom_animset_template = ("""<?xml version="1.0" encoding="utf-8"?>
<save>
	<header version="2" time="0" />
	<version major="54" minor="6" revision="0" build="0" />
	<region id="AnimationSetBank">
		<node id="AnimationSetBank">
			<children>
				<node id="Resource">
					<attribute id="ID" value="{uuid}" type="22" />
					<attribute id="Localized" value="False" type="19" />
					<attribute id="SourceFile" value="" type="30" />
					<attribute id="Name" value="{name}" type="23" />
					<children>
						<node id="AnimationSet">
							<children>
								<node id="AnimationBank">
									<attribute id="Type" value="character" type="22" />
									<children>
										<node id="AnimationSubSets">
											<children>
												<node id="Object">
													<attribute id="MapKey" value="-1" type="4" />
													<children>
														<node id="MapValue">
															<children>
{animations}
															</children>
														</node>
													</children>
												</node>
											</children>
										</node>
									</children>
								</node>
							</children>
						</node>
					</children>
				</node>
			</children>
		</node>
	</region>
</save>""")

def export_file(path, contents):
	try:
		f = open(str(path.absolute()), 'w', encoding='utf-8')
		f.write(contents)
		f.close()
		return True
	except Exception as e:
		print("Error writing '{}': {}".format(path.name, e))
	return False

input_dir = Path('G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/AnimationsPlus/Content_Source/LLANIM_CustomAnimations_Script')
input_files = list(input_dir.glob('*.txt'))

output_dir = Path('G:/Divinity Original Sin 2/DefEd/Data/Public/AnimationsPlus_326b8784-edd7-4950-86d8-fcae9f5c457c/Content/LLANIM_AnimationSets/[PAK]_Custom_AnimationsPlus')

mappings = [
("LLANIM_Dwarves_Female_ABC_AnimationsPlus_Custom_06db04da-62c3-493c-b2c0-f88011944c2b.txt", 
	"LLANIM_Dwarves_Female_ABC_AnimationsPlus_Custom", "06db04da-62c3-493c-b2c0-f88011944c2b"),
("LLANIM_Dwarves_Male_ABC_AnimationsPlus_Custom_ebf6edc1-ed7f-44bc-9577-e00e65de9d30.txt", 
	"LLANIM_Dwarves_Male_ABC_AnimationsPlus_Custom", "ebf6edc1-ed7f-44bc-9577-e00e65de9d30"),
("LLANIM_Elves_Female_ABC_AnimationsPlus_Custom_736863e7-cc28-4b3d-b68e-4393858fe807.txt", 
	"LLANIM_Elves_Female_ABC_AnimationsPlus_Custom", "736863e7-cc28-4b3d-b68e-4393858fe807"),
("LLANIM_Elves_Male_ABC_AnimationsPlus_Custom_bbd4e61d-b48f-417c-8f24-86fd25391462.txt", 
	"LLANIM_Elves_Male_ABC_AnimationsPlus_Custom", "bbd4e61d-b48f-417c-8f24-86fd25391462"),
("LLANIM_Humans_Female_ABC_AnimationsPlus_Custom_0e7e93a7-c12a-4cd9-aece-eeb22afe908f.txt", 
	"LLANIM_Humans_Female_ABC_AnimationsPlus_Custom", "0e7e93a7-c12a-4cd9-aece-eeb22afe908f"),
("LLANIM_Humans_Male_ABC_AnimationsPlus_Custom_26f9f770-5378-4225-b4bb-b04d705c6bdf.txt", 
	"LLANIM_Humans_Male_ABC_AnimationsPlus_Custom", "26f9f770-5378-4225-b4bb-b04d705c6bdf"),
("LLANIM_Lizards_Female_ABC_AnimationsPlus_Custom_9cd345a5-91da-40bc-bba0-411a11d04cb0.txt", 
	"LLANIM_Lizards_Female_ABC_AnimationsPlus_Custom", "9cd345a5-91da-40bc-bba0-411a11d04cb0"),
("LLANIM_Lizards_Male_ABC_AnimationsPlus_Custom_e2ae63c8-bb13-43d7-aab3-a59ec5b5621c.txt", 
	"LLANIM_Lizards_Male_ABC_AnimationsPlus_Custom", "e2ae63c8-bb13-43d7-aab3-a59ec5b5621c")
]

for m in mappings:
	input_path = input_dir.joinpath(m[0])
	uuid = m[2]
	output_path = output_dir.joinpath("{}_{}".format(m[1], uuid)).with_suffix(".lsx")

	if len(uuid) != 36: # 32 chars, 4 hyphens
		raise Exception("UUID '{}' length is not 36 characters!".format(uuid))
	#output_path = output_dir.joinpath("{}".format(m[2])).with_suffix(".lsx")

	input_str = ""
	f = open(str(input_path.absolute()), 'r')
	input_str = f.read()
	f.close()
	animations = [x for x in input_str.splitlines(keepends=False) if x]
	#animations.sort(key=lambda x: x.split("\t")[0], reverse=True)
	anim_nodes = ""
	count = len(animations)
	for i in range(count):
		a = animations[i]
		s = a.split("\t")
		name = s[0].strip().replace(" ", "").replace("\t", "")
		resource = s[1].strip().replace(" ", "").replace("\t", "")
		anim_nodes += (animation_node_template.format(name=name, uuid=resource))
		if len(resource) != 36: # 32 chars, 4 hyphens
			raise Exception("Resource UUID '{}' length is not 36 characters!".format(resource))
		if i < count-1:
			anim_nodes += "\n"
	set_xml_str = '\ufeff'
	set_xml_str = set_xml_str + custom_animset_template.format(name=m[1], uuid=m[2], animations=anim_nodes)
	export_file(output_path, set_xml_str)
	
