from bs4 import BeautifulSoup
import os
import sys
import pathlib
from pathlib import Path
import shutil

output_gameplay_soundbanks_template = """<?xml version="1.0" ?>
<save>
 <header version="1" time="1339579443" />
 <region id="Sound">
     <node id="root">
         <children>
             <node id="SoundBanks"> 
                 <children>
                     <node id="SoundBank">
                         <attribute id="Bank" value="{name}" type="23" />
                         <attribute id="Preload" value="0" type="27" />
                     </node>
                 </children>
             </node>
         </children>
     </node>
 </region>
</save>"""

output_soundsbankslsx_template = """<?xml version="1.0" ?>
<save>
 <header version="1" time="1339579443" />
 <region id="SoundBanks">
     <node id="root">
         <children>
             <node id="Bank">
                 <attribute id="MapKey" value="{name}" type="22" />
                 <attribute id="Localized" value="0" type="19" />
             </node>
         </children>
     </node>
 </region>
</save>"""

def get_arg(arg, fallback):
	if len(sys.argv) > arg:
		val = sys.argv[arg]
		if val != None:
			return val
	return fallback

def get_attribute(xml, attribute_name):
	try:
		att = xml.get(attribute_name.lower())
		return att
	except: pass
	return None

def to_float(val, fallback=0):
	try:
		if val != None:
			return float(val)
	except: pass
	return fallback

def export_file(path, contents):
	try:
		f = open(str(path.absolute()), 'w')
		f.write(contents)
		f.close()
		return True
	except Exception as e:
		print("Erroring writing '{}': {}".format(path.name, e))
	return False

class SoundbankEvent():
	def __init__(self, node):
		self.id = str(get_attribute(node, "Id"))
		self.guid = str(get_attribute(node, "GUID")).replace("}", "").replace("{", "")
		self.name = str(get_attribute(node, "Name"))
		atten = get_attribute(node, "MaxAttenuation")
		if atten == None:
			atten = 60.0
		self.attenuation = to_float(atten)
		self.duration_min = to_float(get_attribute(node, "DurationMin"))
		self.duration_max = to_float(get_attribute(node, "DurationMax"))
		if self.duration_max == 0:
			duration_type = get_attribute(node, "DurationType")
			if duration_type == "Infinite":
				self.duration_max = -1
	
	def debug_print(self):
		return "Name({}) Id({}) GUID({}) Attenuation({}) DurMin({}) DurMax({})".format(
			self.name, self.id, self.guid, self.attenuation, self.duration_min, self.duration_max)

	def to_string(self):
		return "{}\t{}\t{}\t{}\t{}\n".format(
			self.guid, self.name, self.id, self.duration_max, self.attenuation)
	

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

input_dir = get_arg(1, None)
output_dir = get_arg(2, None)

if input_dir != None and output_dir != None:
	input_dir = Path(input_dir)
	output_dir = Path(output_dir)

	soundbanks_files = list(input_dir.glob("*.bnk"))
	main_soundbank = next(iter([x for x in soundbanks_files if x.stem != "Init"]))

	soundbanks_xml_path = input_dir.joinpath("SoundbanksInfo.xml")
	soundbanks_xml = None
	try:
		f = open(str(soundbanks_xml_path.absolute()), 'r')
		soundbanks_xml = BeautifulSoup(f.read(), 'html.parser')
		f.close()
	except: pass
	if soundbanks_xml != None:
		soundbank_events = []
		event_nodes = soundbanks_xml.find_all("event")
		for node in event_nodes:
			event = SoundbankEvent(node)
			soundbank_events.append(event)
			#print(event.debug_print())
	
		output_txt_str = "UUID Name    Hash    Duration    Attenuation\n"
		for event in soundbank_events:
			output_txt_str += event.to_string()
		
		output_txt_path = output_dir.joinpath(main_soundbank.with_suffix(".txt").name)
		print("Output: {}".format(output_txt_path))
		if export_file(output_txt_path, output_txt_str):
			print("Wrote soundbank file '{}' with '{}' events.".format(output_txt_path, len(soundbank_events)))
		
		gameplay_soundbanks_lsxpath = output_dir.joinpath("GameplaySoundBanks.lsx")
		if not gameplay_soundbanks_lsxpath.exists():
			gameplay_soundsbanks_str = output_gameplay_soundbanks_template.format(name=main_soundbank.stem)
			if export_file(gameplay_soundbanks_lsxpath, gameplay_soundsbanks_str):
				print("Wrote '{}'.".format(gameplay_soundbanks_lsxpath))
		
		soundbanks_lsx_path = output_dir.joinpath("SoundBanks.lsx")
		if not soundbanks_lsx_path.exists():
			soundsbanks_str = output_soundsbankslsx_template.format(name=main_soundbank.stem)
			if export_file(soundbanks_lsx_path, soundsbanks_str):
				print("Wrote '{}'.".format(soundbanks_lsx_path))
		
		wem_files = list(input_dir.glob("*.wem"))
		for f in wem_files:
			shutil.copy(f.absolute(), output_dir.joinpath(f.name))
		print("Copied '{}' .wem files to output folder.".format(len(wem_files)))

		if shutil.copy(main_soundbank.absolute(), output_dir.joinpath(main_soundbank.name)):
			print("Copied main soundbank '{}' to output folder.".format(main_soundbank.name))
else:
	#raise Exception("Input and output directory arguments not included. Skipping.")
	print("[ERROR] - Input and output directory arguments not included. Skipping.")

input("Press ENTER to close.")