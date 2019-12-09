from bs4 import BeautifulSoup

import os
import sys

import subprocess

import pathlib
from pathlib import Path

import re

animations = (
"""skill_attack_ll_handcrossbow_01_cast
skill_attack_ll_pistol_01_cast
skill_attack_ll_rushpower_2h_01_cast
skill_attack_ll_rushround_2h_01_cast
skill_attack_ll_sh_01_cast
skill_attack_ll_sh_02_cast
skill_attack_ll_wd_01_cast
skill_attack_ll_wd_02_cast
skill_attack_unarmed_01_cast
skill_attack_unarmed_offhand_01_cast
skill_cast_ll_stance_01_cast
skill_cast_ll_throw_01_cast
skill_cast_ll_throw_02_cast
skill_cast_projectile_01_cast
skill_cast_projectile_offhand_01_cast
skill_cast_self_teleport_in_01_cast
skill_cast_self_teleport_out_01_cast
skill_prepare_ll_1h_01_loop
skill_prepare_ll_1h_01_start
skill_prepare_ll_handcrossbow_01_loop
skill_prepare_ll_handcrossbow_01_start
skill_prepare_ll_wd_01_loop
skill_prepare_ll_wd_01_start
skill_prepare_sneak_01_start
skill_prepare_weapon_1h_loop
skill_prepare_weapon_1h_start
skill_prepare_weapon_2h_loop
skill_prepare_weapon_2h_start
skill_prepare_weapon_2hs_loop
skill_prepare_weapon_bow_loop
skill_prepare_weapon_bow_start
skill_prepare_weapon_dw_loop
skill_prepare_weapon_dw_start
skill_prepare_weapon_dwsml_loop
skill_prepare_weapon_dwsml_start
skill_prepare_weapon_dwwd_loop
skill_prepare_weapon_dwwd_start
skill_prepare_weapon_pole_loop
skill_prepare_weapon_pole_start
skill_prepare_weapon_sh_loop
skill_prepare_weapon_sh_start
skill_prepare_weapon_shwd_loop
skill_prepare_weapon_shwd_start
skill_prepare_weapon_sml_loop
skill_prepare_weapon_sml_start
skill_prepare_weapon_st_loop
skill_prepare_weapon_st_start
skill_prepare_weapon_ua_loop
skill_prepare_weapon_ua_start
skill_prepare_weapon_wd_loop
skill_prepare_weapon_wd_start
skill_prepare_weapon_xb_loop
skill_prepare_weapon_xb_start""").splitlines(keepends=False)

def get_attribute_value(xml, attribute_name):
	try:
		att = xml.find("attribute", {"id":attribute_name})["value"]
		return str(att)
	except: pass
	return None

def attribute_match(xml, attribute_name, value):
	x = get_attribute_value(xml, attribute_name)
	return x is not None and x == value

def animation_match(x):
	m = x.find("attribute", {"id":"MapKey"})
	if m is not None:
		return m["value"] in animations
	return False

def export_file(path, contents):
	try:
		f = open(str(path.absolute()), 'w')
		f.write(contents)
		f.close()
		return True
	except Exception as e:
		print("Error writing '{}': {}".format(path.name, e))
	return False

def get_set_node(xml, id):
	node = xml.find("attribute", {"value":id})
	if node != None:
		return node.parent
	return 

#input_dir = Path('G:/Divinity Original Sin 2/DefEd/Data/Public/AnimationsPlus_326b8784-edd7-4950-86d8-fcae9f5c457c/Content/LLANIM_Overrides/[PAK]_AnimationSets')
input_dir = Path('G:/Modding/DOS2DE/Projects_Source/AnimatonsPlus/_Backup/MainOverrideSets_BeforeRemovingNewCustoms/Content/LLANIM_Overrides/[PAK]_AnimationSets')
input_files = list(input_dir.glob('*.lsx'))

output_dir = Path('G:/Divinity Original Sin 2/DefEd/Data/Public/AnimationsPlus_326b8784-edd7-4950-86d8-fcae9f5c457c/Content/LLANIM_AnimationSets/[PAK]_Custom_AnimationsPlus')
output_source_dir = Path('G:/SourceControlGenerator/Data/Divinity Original Sin 2 - Definitive Edition/Projects/AnimationsPlus/Content_Source/LLANIM_CustomAnimations_Script')

class Animation():
	def __init__(self, name, resource_uuid, node):
		self.name = name
		self.id = resource_uuid
		self.node = node

class AnimationSet():
	def __init__(self, filepath):
		self.animations = []
		self.filepath = filepath

for fpath in input_files:
	f = open(str(fpath.absolute()), 'r')
	animset_xml = BeautifulSoup(f.read(), 'html.parser')
	f.close()

	resource_node = animset_xml.find("node", {"id": "Resource"})
	animset_name = get_attribute_value(resource_node, "Name")
	animset_id = get_attribute_value(resource_node, "ID")

	animset = AnimationSet(fpath)

	custom_tab = get_set_node(animset_xml, "-1")
	#print("Set: {}".format(custom_tab))
	anim_nodes = list(custom_tab.find_all("node", {"id":"Animation"}))
	matched_nodes = [x for x in anim_nodes if animation_match(x)]

	if len(matched_nodes) == 0:
		print("Failed to match animation nodes")
		#for n in anim_nodes:
			#print("Anim node: {}".format(n))

	for node in matched_nodes:
		anim_data = Animation(get_attribute_value(node, "Name"), get_attribute_value(node, "ID"), node)
		if anim_data.name is not None:
			animset.animations.append(anim_data)

	animset.animations.sort(key=lambda x: x.name, reverse=False)
	#output_txt_str = "{}\t{}\n".format(animset_name, animset_id)
	output_txt_str = ""
	for x in animset.animations:
		output_txt_str += "{}\t{}\n".format(x.name, x.id)
	
	#p = Path(fpath).parent.joinpath(animset_name).with_suffix(".txt")
	output_txt_path = Path(output_source_dir).joinpath("{}_{}".format(animset_name, fpath.name)).with_suffix(".txt")
	export_file(output_txt_path, output_txt_str)

	for anim in animset.animations:
		anim.node.decompose()

	# output_xml_str = animset_xml.prettify()
	# output_xml_path = Path(output_source_dir).joinpath(fpath.name).with_suffix(".lsx")
	# export_file(output_xml_path, output_xml_str)