import os
from pathlib import Path
import dos2de_common as common
from bs4 import BeautifulSoup
from typing import List, Dict

statobdefinitions_path = Path("G:\Divinity Original Sin 2\DefEd\Data\Editor\Config\Stats\StatObjectDefinitions.sod")
modifiers_path = Path("D:\Modding\DOS2DE_Extracted\Public\Shared\Stats\Generated\Structure\Modifiers.txt")

class Modifier():
	def __init__(self, name:str, value:str):
		self.name = name
		self.value = value
		self.export_name = ""
		self.display_name = ""

class ModifierType():
	def __init__(self, name:str, export_type:str):
		if "Status_" in name:
			name = name.replace("Status_", "")
		self.name = name
		self.export_type = export_type
		self.modifiers:Dict[str, Modifier] = {}

class Modifiers():
	def __init__(self):
		self.modifiertypes:Dict[str, ModifierType] = {}

	def Add(self, key:str, value:ModifierType):
		self.modifiertypes[key] = value

	def GetModifierValue(self, stattype:str, propname:str, subtype="")->str:
		for modtype in self.modifiertypes.values():
			#print("{} | {}".format(modtype.export_type, stattype))
			#if propname == "AuraRadius": print("Looking for: ({})({}) {} in {}({})".format(stattype, propname, subtype, modtype.name, modtype.export_type))
			if modtype.export_type == stattype:
				if stattype == "SkillData" or stattype == "StatusData":
					if modtype.name == subtype:
						for mod in modtype.modifiers.values():
							if mod.name == propname:
								return mod.value
				else:
					for mod in modtype.modifiers.values():
						if mod.name == propname:
							return mod.value
			elif modtype.name == stattype:
				for mod in modtype.modifiers.values():
					if mod.name == propname:
						return mod.value
		return None

def get_attribute(node, id, fallback)->str:
	try:
		return node[id]
	except: pass
	return fallback

def Build_StatDefinitions(file_path:str=None, debug:bool=False)->Modifiers:
	if file_path is None:
		file_path = statobdefinitions_path.absolute()
	modifiers = Modifiers()

	print("Reading file '{}'".format(file_path))
	f = open(file_path, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	obj_definitions = list(lsx_xml.find_all("stat_object_definition"))
	for node in obj_definitions:
		mod_type_name = node["name"]
		mod_export_type = get_attribute(node, "export_type", mod_type_name)
		if debug: print("Parsing modifier type {}".format(mod_type_name))
		modifier_type = ModifierType(mod_type_name, mod_export_type)
		modifiers.Add(mod_type_name, modifier_type)
		field_definitions = list(node.find_all("field_definition"))
		for defnode in field_definitions:
			#<field_definition name="Strength" display_name="Strength" export_name="Strength" type="Enumeration" enumeration_type_name="PreciseQualifier" description="Enter a value in [0,10] range. Code will turn it into level-appropriate amount of attribute. 10 is roughly the amount that a dedicated player can gather at that level." />
			def_name = defnode["export_name"]
			def_type = defnode["type"]
			mod = Modifier(def_name, def_type)
			mod.display_name = defnode["display_name"]
			mod.export_name = defnode["export_name"]
			modifier_type.modifiers[def_name] = mod
			if debug: print("---- Found modifier {} with value {}".format(def_name, def_type))

	if debug: print("Modifier types: {}".format("\n".join(modifiers.modifiertypes.keys())))
	return modifiers