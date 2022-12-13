lsx_template = """<?xml version="1.0" encoding="utf-8"?>
<save>
	<version major="3" minor="6" revision="6" build="0" />
	<region id="Templates">
		<node id="Templates">
			<children>
{entries}
            </children>
        </node>
    </region>
</save>
"""

entry_template = """				<node id="GameObjects">
					<attribute id="BloodSurfaceType" type="22" value="SurfaceNone" />
					<attribute id="CanBeMoved" type="19" value="True" />
					<attribute id="CanBePickedUp" type="19" value="True" />
					<attribute id="CanShootThrough" type="19" value="True" />
					<attribute id="CoverAmount" type="1" value="0" />
					<attribute id="Description" type="28" handle="{descHandle}" value="{desc}" />
					<attribute id="Flag" type="4" value="0" />
					<attribute id="GroupID" type="5" value="0" />
					<attribute id="Icon" type="22" value="{icon}" />
					<attribute id="LevelName" type="22" value="" />
					<attribute id="MapKey" type="22" value="{uuid}" />
					<attribute id="MeshProxy" type="22" value="" />
					<attribute id="Name" type="23" value="BOOK_SKILL_{stat}" />
					<attribute id="PhysicsTemplate" type="22" value="ef0bce41-34d2-49d6-8e94-eb85cb1e8928" />
					<attribute id="Scale" type="6" value="1" />
					<attribute id="Stats" type="22" value="{stat}" />
					<attribute id="Tooltip" type="1" value="2" />
					<attribute id="Type" type="22" value="item" />
					<attribute id="VisualTemplate" type="22" value="06d7cda8-b6f8-4749-b25b-460447e5c69c" />
					<attribute id="WalkThrough" type="19" value="True" />
					<children>
						<node id="AIBounds">
							<attribute id="AIType" type="1" value="1" />
							<attribute id="Max" type="12" value="0.0731614 0.00534957 0.113343" />
							<attribute id="Min" type="12" value="-0.0731614 0.00534957 -0.113343" />
							<attribute id="Radius" type="6" value="0.0674524" />
						</node>
						<node id="Equipment"/>
						<node id="GameMaster">
							<attribute id="GameMasterSpawnSection" type="4" value="12" />
							<attribute id="GameMasterSpawnSubSection" type="28" handle="h0596ef3fga2f1g4d13ga776gf5cc7ca4f149" value="Letters" />
						</node>
						<node id="InventoryList"/>
						<node id="ItemList" />
						<node id="LayerList"/>
						<node id="OnDestroyActions" />
						<node id="OnUsePeaceActions">
							<children>
								<node id="Action">
									<attribute id="ActionType" value="13" type="4" />
									<children>
										<node id="Attributes">
											<attribute id="Consume" value="True" type="19" />
											<attribute id="SkillID" value="{skill}" type="22" />
										</node>
									</children>
								</node>
							</children>
						</node>
						<node id="Scripts" />
						<node id="Tags" />
					</children>
				</node>"""

stat_template = """new entry "{statid}"
type "Object"
using "_Skillbooks"
data "RootTemplate" "{uuid}"
data "Act part" "1"
data "Value" "120"
data "ComboCategory" "{comboCategory}"
data "Requirements" "{requirements}"
data "ObjectCategory" "{objectCategory}"
data "MinAmount" "1"
data "MaxAmount" "1"
data "Priority" "1"
data "MinLevel" "1"
"""

tsv_template = """
Key	Content	Handle
{entries}
"""

import uuid
from pathlib import Path
from dataclasses import dataclass,field
import argparse
import timeit
import re
import os
import subprocess

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

@dataclass
class TranslatedString:
	handle:str
	content:str

def new_handle()->str:
	return "h" + str.replace(str(uuid.uuid4()), "-", "g")

def ts(content:str, handle:str=""):
	if handle == "":
		handle = new_handle()
	return TranslatedString(handle, content)

EMPTY_DESC = ts("", new_handle())

@dataclass
class Skillbook:
	id:str
	skill:str
	description:TranslatedString = field(default_factory=lambda: EMPTY_DESC)
	icon:str = "unknown"
	uuid:str = ""
	statid:str = ""
	comboCategory:str = "" #SkillbookAir
	objectCategory:str = "" #SkillbookAirStarter
	requirements:str = "" #AirSpecialist 1

	def __post_init__(self):
		if self.uuid == "":
			self.uuid = str(uuid.uuid4())
		if self.statid == "":
			self.statid = f"SKILLBOOK_{self.id}"
	
	def to_template(self) -> str:
		return entry_template.format(uuid=self.uuid, icon=self.icon, stat=self.id, skill=self.skill, desc=self.description.content, descHandle=self.description.handle)
	
	def to_stat(self) -> str:
		return stat_template.format(uuid=self.uuid, statid=self.statid, comboCategory=self.comboCategory, requirements=self.requirements, objectCategory=self.objectCategory)
	
	def to_tsv(self) -> str:
		return f"{self.statid}\tPlaceholder\t{new_handle()}"

AllBooks:list[Skillbook] = [
	#Skillbook("BEETUS_FireThing", "Projectile_BEETUS_FireThing", FIREBOOK_DESC),
	#Skillbook("BEETUS_Burninating", "Target_BEETUS_Burninating", FIREBOOK_DESC),
]

#python dos2de_create_skillbooks.py -p "G:\Divinity Original Sin 2\DefEd\Data\Public\WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f\Stats\Generated\Data\LLWEAPONEX_Skills.txt" -t "Generated_Skillbooks/AllSkillbooks.lsx" -s "Generated_Skillbooks/Skillbooks.txt" --tsv "Generated_Skillbooks/Skillbooks.tsv" --divine "G:\Modding\DOS2DE\ConverterApp\divine.exe" --deletelsx
#python dos2de_create_skillbooks.py -p "D:\Modding\DOS2DE_Extracted\SkillData.txt" -t "Generated_Skillbooks/AllSkillbooks.lsx" -s "Generated_Skillbooks/Skillbooks.txt" --tsv "Generated_Skillbooks/Skillbooks.tsv"
#python dos2de_create_skillbooks.py -p "D:\Modding\DOS2DE_Extracted\SkillData.txt" --pygen "Generated_Skillbooks/AllBooks.py"

def run():
	parser = argparse.ArgumentParser(description='Generate root templates and object stats for a given set of skills.')
	parser.add_argument("-p", "--parse", type=str, help='Parse stats text files (separated by ;) to build a list of skills to use.')
	parser.add_argument("-t", "--templates", type=Path, required=False, help='The path of the merged root templates file to generate.')
	parser.add_argument("-s", "--stats", type=Path, required=False, help='The path of the object stats file to generate.')
	parser.add_argument("-d", "--deletelsx", action=argparse.BooleanOptionalAction, default=False, help='Delete the generated lsx file after converting it to lsf.')
	parser.add_argument("--tsv", type=Path, help='An optional path to a tsv file to generate for all object stats.')
	parser.add_argument("--pygen", type=Path, help='Generate python text with all the parsed stats.')
	parser.add_argument("--divine", type=Path, help='The path to divine.exe. Required for lsf generation.')
	args = parser.parse_args()

	if args.parse is not None and args.parse != "":
		parse_paths = [Path(x) for x in args.parse.split(";")]
		for p in parse_paths:
			if p.exists():
				lines:list[str]
				with p.open("r", encoding="utf-8") as f:
					lines = f.read().splitlines()

				entry_pattern = re.compile("^new entry \"([^\"]+)\"", re.IGNORECASE)
				skilltype_pattern = re.compile("([^_]+)_(.+)", re.IGNORECASE)
				memrequirements_pattern = re.compile('data "MemorizationRequirements" "([^"]+)"', re.IGNORECASE)
				forGameMasterText = 'data "ForGameMaster" "Yes"'
				ignoreSkillByAttribute = [
					'data "ForGameMaster" "No"',
					'data "IsEnemySkill" "Yes"'
				]
				
				mem_requirements:str = ""
				skill_id:str|None = None
				forGameMaster = False

				def clear_entry():
					nonlocal forGameMaster,skill_id,mem_requirements
					forGameMaster = False
					skill_id = None
					mem_requirements = ""

				total = len(lines)
				i = 0
				while i < total:
					line = lines[i]
					i += 1
					if line != "" and i < total:
						if line in ignoreSkillByAttribute:
							clear_entry()
						elif line == forGameMasterText:
							forGameMaster = True
						else:
							next_memreq = match.group(1) if (match := memrequirements_pattern.search(line)) else ""
							if next_memreq != "":
								mem_requirements = next_memreq
							next_skill = match.group(1) if (match := entry_pattern.search(line)) else ""
							if next_skill != "":
								skill_id = next_skill
								forGameMaster = False
					elif skill_id != None and forGameMaster:
						book_id = match.group(2) if (match := skilltype_pattern.search(skill_id)) else skill_id
						AllBooks.append(Skillbook(book_id, skill_id, EMPTY_DESC, requirements=mem_requirements))
						clear_entry()
						
				print(f"[Skillbooks] {';'.join([x.id for x in AllBooks])}")
			else:
				print(f"Warning - File '{p}' for arg parse(-p) does not exist.")

	skillbooks = sorted(AllBooks, key=lambda x: x.id)
	if args.pygen is not None:
		pygen_path:Path = args.pygen
		if pygen_path.drive == "":
			templates_path = script_dir.joinpath(pygen_path)
		pygen_path.parent.mkdir(parents=True, exist_ok=True)
		with pygen_path.open("w", encoding="utf-8") as f:
			output = """AllSkills:list[Skillbook] = [
{entries}
]""".format(entries = "\n".join([f'\tSkillbook("{x.id}", "{x.skill}", requirements="{x.requirements}")' for x in skillbooks]))
			f.write(output)

	if args.templates is not None:
		templates_path:Path = args.templates
		if templates_path.drive == "":
			templates_path = script_dir.joinpath(templates_path)
		templates_output = lsx_template.format(entries="\n".join([x.to_template() for x in skillbooks]))
		templates_path.parent.mkdir(parents=True, exist_ok=True)
		with templates_path.open("w", encoding="utf-8") as f:
			f.write(templates_output)

		if args.divine is not None:
			divine_path:Path = args.divine
			if divine_path.exists():
				lsf_output = templates_path.with_suffix(".lsf")
				p = subprocess.run([str(divine_path.absolute()), 
					"-g", 
					"dos2de",
					"-l", 
					"all",
					"-s",
					str(templates_path.absolute()),
					"-a",
					"convert-resource",
					"-d",
					str(lsf_output.absolute()),
					"-i",
					"lsx",
					"-o",
					"lsf"
					], 
					universal_newlines=True, 
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
				if p.returncode == 0 and lsf_output.exists():
					print(p.stdout)
					print(f"Converted {templates_path} to {lsf_output}.")
					if args.deletelsx == True:
						os.remove(templates_path)
						print(f"Deleted {templates_path}.")
				else:
					print(f"Error({p.returncode}):\n{p.stdout}")

	if args.stats is not None:
		stats_path:Path = args.stats
		if stats_path.drive == "":
			stats_path = script_dir.joinpath(stats_path)
		stats_output = "\n".join([x.to_stat() for x in skillbooks])
		stats_path.parent.mkdir(parents=True, exist_ok=True)
		with stats_path.open("w", encoding="utf-8") as f:
			f.write(stats_output)

	if args.tsv is not None:
		tsv_path:Path = args.tsv
		if tsv_path.drive == "":
			tsv_path = script_dir.joinpath(tsv_path)
		tsv_output = tsv_template.format(entries="\n".join([x.to_tsv() for x in skillbooks]))
		tsv_path.parent.mkdir(parents=True, exist_ok=True)
		with tsv_path.open("w", encoding="utf-8") as f:
			f.write(tsv_output)

print("Generated skillbook data in {} second(s).".format(timeit.timeit(run, number=1)))