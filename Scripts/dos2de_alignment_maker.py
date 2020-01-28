from bs4 import BeautifulSoup
import os
from pathlib import Path
import glob
import dos2de_common as Common

def get_attribute(xml, id, node="attribute", attid="id", valueid="value"):
	v = xml.find(node, attrs={attid:id})
	if v is not None:
		try:
			inner = v[valueid]
			return inner
		except: pass
	return ""

class Relation():
	def __init__(self, source, target, value):
		self.source = source
		self.target = target
		self.value = value

class Alignment():
	def __init__(self, name):
		self.name = name
		self.entities = []
		self.relations = []

path_alignments_shared = Path("D:\Modding\DOS2DE_Extracted\Mods\Shared\Story\Alignments\Alignment.lsx")
path_alignments_origins = Path("D:\Modding\DOS2DE_Extracted\Mods\DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4\Story\Alignments\Alignment.lsx")

alignments = {}

def get_alignments(lsx_path, filterfor=""):
	print("Reading file '{}'".format(lsx_path))
	lsx_xml = None
	f = open(lsx_path, 'r')
	lsx_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	lsx_alignments = list(lsx_xml.find_all("node", attrs={"id":"Alignment"}))
	for node in lsx_alignments:
		# <attribute id="Object" value="ARX_Civilian" type="22" />
		name = get_attribute(node, "Object")
		if not name in alignments.keys() and (filterfor == "" or filterfor in name):
			alignment = Alignment(name)
			alignments[name] = alignment
			print("Added alignment '{}'".format(name))

	lsx_entities = list(lsx_xml.find_all("node", attrs={"id":"Entity"}))
	for node in lsx_entities:
		alignment_name = get_attribute(node, "Alignment")
		name = get_attribute(node, "Name")
		if alignment_name in alignments.keys() and (filterfor == "" or filterfor in name):
			alignment = alignments[alignment_name]
			if alignment is not None:
				if not name in alignment.entities:
					alignment.entities.append(name)
					print("Added entity '{}' to alignment '{}'".format(name, alignment_name))

	lsx_relations = list(lsx_xml.find_all("node", attrs={"id":"Relation"}))
	for node in lsx_relations:
		source = get_attribute(node, "Source")
		target = get_attribute(node, "Target")
		value = get_attribute(node, "Value")
		if source in alignments.keys():
			alignment = alignments[source]
			if alignment is not None:
				alignment.relations.append(Relation(source, target, value))
				print("Added relation to alignment '{}' => '{}' = {}".format(source, target, value))
		else:
			for name,alignment in alignments.items():
				if source in alignment.entities:
					alignment.relations.append(Relation(source, target, value))
					print("Added relation to alignment '{}' entity '{}' => '{}' = {}".format(alignment.name, source, target, value))
					break

get_alignments(path_alignments_shared.absolute())
get_alignments(path_alignments_origins.absolute(), "Hero ")

template_alignment_lsx = """<?xml version="1.0" encoding="UTF-8" ?>
<save>
    <header version="2" />
    <version major="3" minor="6" revision="6" build="0" />
    <region id="AlignmentManager">
        <node id="root">
            <children>
                <node id="Alignments">
                    <children>
                        <node id="Alignment">
                            <attribute id="Object" value="LeaderLib_Dummy_TargetHelper" type="22" />
                        </node>
                        <node id="Alignment">
                            <attribute id="Object" value="LeaderLib_Neutral_NoConflict" type="22" />
                        </node>
                    </children>
                </node>
                <node id="Entities" />
                <node id="Relations">
                    <children>
{relations}
                    </children>
                </node>
            </children>
        </node>
    </region>
</save>
"""
template_relation = """                        <node id="Relation">
                            <attribute id="Source" value="{source}" type="22" />
                            <attribute id="Target" value="{target}" type="22" />
                            <attribute id="Value" value="{value}" type="4" />
                        </node>\n"""

target_dummy_alignment = Alignment("LeaderLib_Dummy_TargetHelper")
for key,alignment in alignments.items():
	target_dummy_alignment.relations.append(Relation(target_dummy_alignment.name, alignment.name, "0"))
	target_dummy_alignment.relations.append(Relation(alignment.name, target_dummy_alignment.name, "0"))
	for entity in alignment.entities:
		target_dummy_alignment.relations.append(Relation(target_dummy_alignment.name, entity, "0"))
		target_dummy_alignment.relations.append(Relation(entity, target_dummy_alignment.name, "0"))

relations_str = ""
for relation in target_dummy_alignment.relations:
	relations_str += template_relation.format(source=relation.source,target=relation.target,value=relation.value)

output_str = template_alignment_lsx.format(relations=relations_str)

import pyperclip
pyperclip.copy(output_str)
