from bs4 import BeautifulSoup
import os
from pathlib import Path
import dos2de_common as common
import timeit

target_file = "D:\Modding\DOS2DE_Extracted\Public\Shared\RootTemplates\_merged.lsx"
template_entry = "\t{Surface} = ts:Create(\"{Handle}\", \"{Reference}\"),\n"

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

def get_attribute(xml:BeautifulSoup, id, node="attribute", attid="id", valueid="value", recursive=True):
	v = xml.find(node, attrs={attid:id}, recursive=recursive)
	if v is not None:
		try:
			inner = v[valueid]
			return inner
		except: pass
	return ""

def get_attribute_node(xml:BeautifulSoup, id, node="attribute", attid="id", recursive=True):
	v = xml.find(node, attrs={attid:id}, recursive=recursive)
	if v is not None:
		return v
	return None

class Entry():
	def __init__(self, surface, displayName, handle):
		self.surface = surface
		self.name = displayName
		self.handle = handle

	def Export(self,):
		return template_entry.format(Surface=self.surface, Handle=self.handle, Reference=self.name)

print("Reading file '{}'".format(target_file))
lsx_xml = None
f = open(target_file, 'r')
lsx_xml = BeautifulSoup(f.read(), 'lxml')
f.close()
print("Parsing nodes...")

def valid_entry(node):
	value = node["value"]
	if value:
		return value == "surface"
	return False

entries = list(x.parent for x in lsx_xml.find_all("attribute", attrs={"id":"Type"}, recursive=True) if valid_entry(x))

def get_data()->str:
	export_entries:list[Entry] = []
	for node in entries:
		name_node = get_attribute_node(node, "DisplayName", recursive=False)
		if name_node:
			displayName = name_node["value"]
			handle = name_node["handle"]
			surface = get_attribute(node, "Name")
			export_surface = Entry(surface, displayName, handle)
			export_entries.append(export_surface)
		else:
			print(node)
			print("=================")

	export_entries = sorted(export_entries, lambda x: x.surface)
	output = "LocalizedText.Surfaces = {\n"
	for entry in export_entries:
		output = output + entry.Export()
	output = output + "}"
	return output

def Run():
	output = get_data()
	output_path = script_dir.joinpath("Generated").joinpath("LocalizedText_RootTemplates.lua")
	common.export_file(output_path, output)

print("Completed in {} seconds.".format(timeit.timeit(Run, number=1)))