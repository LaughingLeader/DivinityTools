
class Talent():
	def __init__(self, id_name, name, description, icon, ran=100, cp=4, group="Normal"):
		self.id = id_name
		self.name = name
		if(name == ""): self.name = self.id
		self.description = description
		self.icon = icon
		self.group = group
		self.cp = cp
		self.ran = ran

talents_all = [
	"ItemMovement",
	"ItemCreation",
	"Flanking",
	"AttackOfOpportunity",
	"Backstab",
	"Trade",
	"Lockpick",
	"ChanceToHitRanged",
	"ChanceToHitMelee",
	"Damage",
	"ActionPoints",
	"ActionPoints2",
	"Criticals",
	"IncreasedArmor",
	"Sight",
	"ResistFear",
	"ResistKnockdown",
	"ResistStun",
	"ResistPoison",
	"ResistSilence",
	"ResistDead",
	"Carry",
	"Throwing",
	"Repair",
	"ExpGain",
	"ExtraStatPoints",
	"ExtraSkillPoints",
	"Durability",
	"Awareness",
	"Vitality",
	"FireSpells",
	"WaterSpells",
	"AirSpells",
	"EarthSpells",
	"Charm",
	"Intimidate",
	"Reason",
	"Luck",
	"Initiative",
	"InventoryAccess",
	"AvoidDetection",
	"AnimalEmpathy",
	"Escapist",
	"StandYourGround",
	"SurpriseAttack",
	"LightStep",
	"ResurrectToFullHealth",
	"Scientist",
	"Raistlin",
	"MrKnowItAll",
	"WhatARush",
	"FaroutDude",
	"Leech",
	"ElementalAffinity",
	"FiveStarRestaurant",
	"Bully",
	"ElementalRanger",
	"LightningRod",
	"Politician",
	"WeatherProof",
	"LoneWolf",
	"Zombie",
	"Demon",
	"IceKing",
	"Courageous",
	"GoldenMage",
	"WalkItOff",
	"FolkDancer",
	"SpillNoBlood",
	"Stench",
	"Kickstarter",
	"WarriorLoreNaturalArmor",
	"WarriorLoreNaturalHealth",
	"WarriorLoreNaturalResistance",
	"RangerLoreArrowRecover",
	"RangerLoreEvasionBonus",
	"RangerLoreRangedAPBonus",
	"RogueLoreDaggerAPBonus",
	"RogueLoreDaggerBackStab",
	"RogueLoreMovementBonus",
	"RogueLoreHoldResistance",
	"NoAttackOfOpportunity",
	"WarriorLoreGrenadeRange",
	"RogueLoreGrenadePrecision",
	"WandCharge",
	"DualWieldingDodging",
	"Human_Inventive",
	"Human_Civil",
	"Elf_Lore",
	"Elf_CorpseEating",
	"Dwarf_Sturdy",
	"Dwarf_Sneaking",
	"Lizard_Resistance",
	"Lizard_Persuasion",
	"Perfectionist",
	"Executioner",
	"ViolentMagic",
	"QuickStep",
	"Quest_SpidersKiss_Str",
	"Quest_SpidersKiss_Int",
	"Quest_SpidersKiss_Per",
	"Quest_SpidersKiss_Null",
	"Memory",
	"Quest_TradeSecrets",
	"Quest_GhostTree",
	"BeastMaster",
	"LivingArmor",
	"Torturer",
	"Ambidextrous",
	"Unstable",
	"ResurrectExtraHealth",
	"NaturalConductor",
	"Quest_Rooted",
]

talents_giftbag = [
	#Talent("PainDrinker", "", "", ""),
	#Talent("DeathfogResistant", "", "", ""),
	#Talent("Sourcerer", "", "", ""),
	#Talent("Rager", "", "", ""),
	#Talent("Elementalist", "", "", ""),
	Talent("Sadist", "", "Melee attacks deal additional fire damage to burning targets, poison damage to poisoned targets and physical damage to bleeding targets.", "Talent_Sadist", ran=50, cp=10, group="Weapon"),
	Talent("Haymaker", "", "Character's attacks never miss but they cannot deal critical strikes.", "Talent_Haymaker", ran=100, cp=8, group="Elite"),
	Talent("Gladiator", "", "Every time character is hit with a melee attack while wielding a shield, they perform a counterattack.<br>Can happen only once per turn. ", "Talent_Gladiator", ran=100, cp=6, group="Weapon"),
	Talent("Indomitable", "", "Character has immunity to Stunned, Frozen, Knocked Down, Polymorphed, Petrified, Crippled for 1 turn after being affected by one of these statuses.<br>Can happen once every 3 turns.", "Talent_Indomitable", ran=50, cp=12, group="Elite"),
	#Talent("WildMag", "", "", ""),
	#Talent("Jitterbug", "", "", "Talent_Jitterbug"),
	Talent("Soulcatcher", "", "When an allied character dies, a Zombie Crawler is raised at their corpse, under their control. Zombie Crawler lasts 3 turns or until character is resurrected. Range 12m. Does not affect summoned creatures.", "Talent_Soulcatcher", ran=20, cp=12, group="Elite"),
	Talent("MasterThief", "Master Thief", "Character has a chance to steal a consumable item on attack.<br>Can only happen once per turn.", "Talent_Master_Thief", ran=90, cp=4, group="Normal"),
	Talent("GreedyVessel", "Greedy Vessel", "Every time someone casts a Source spell in combat, character has a 20% chance of gaining a Source Point.", "Talent_Greedy_Vessel", ran=90, cp=4, group="Normal"),
	Talent("MagicCycles","Magic Cycles", "At the start of an encounter, you gain one of two statuses: Cycle of Fire and Water or Cycle of Earth and Air. Cyle of Fire and Water increases Pyro and Hyro by 2. Cyle of Earth and Air increases Geo and Aero by 2. Statuses swap each turn.", "Talent_Magic_Cycles", 100, 6, "Elite"),
]

talent_belt_stat = """
new entry "_LLENEMY_TalentBelt_{talent}"
type "Armor"
using "_LLENEMY_TalentBeltBase"
data "Talents" "{talent}"
"""

talent_status_stat = """
new entry "LLENEMY_TALENT_{talentupper}"
type "StatusData"
data "StatusType" "CONSUME"
using "LLENEMY_TALENT_BASE"
data "DisplayName" "LLENEMY_TALENT_{talentupper}_DisplayName"
data "Description" "LLENEMY_TALENT_{talentupper}_Description"
data "DisplayNameRef" "Talent: {talent}"
data "DescriptionRef" "{description}"
data "Icon" "{icon}"
data "Items" "_LLENEMY_TalentBelt_{talent}"
"""

talent_osiris = """
LLENEMY_Upgrades_AddStatus("Talents", "{group}", "LLENEMY_TALENT_{talentupper}", {ran}, {cp});"""

talent_tsv = """
LLENEMY_TALENT_{talentupper}_DisplayName\tTalent: {name}
LLENEMY_TALENT_{talentupper}_Description\t{description}"""

tsv_template = """Key\tContent
{entries}
"""

armor_str = ""
status_str = ""
osiris_str = ""
output_tsv = ""

for talent in talents_giftbag:
	armor_str += talent_belt_stat.format(talent=talent.id)
	status_str += talent_status_stat.format(talent=talent.id,talentupper=talent.id.upper(), description=talent.description, icon=talent.icon)
	osiris_str += talent_osiris.format(talentupper=talent.id.upper(),group=talent.group, ran=talent.ran, cp=talent.cp)
	output_tsv += talent_tsv.format(talentupper=talent.id.upper(), name=talent.name,description=talent.description)

import os
from pathlib import Path
import dos2de_common as Common

Common.export_file(Path("Generated").joinpath("LLENEMY_Talents_Armor.txt"), armor_str)
Common.export_file(Path("Generated").joinpath("LLENEMY_Talents_Statuses.txt"), status_str)
Common.export_file(Path("Generated").joinpath("LLENEMY_Talents_Osiris.txt"), osiris_str)
Common.export_file(Path("Generated").joinpath("LLENEMY_Talents_Localization.txt"), tsv_template.format(entries=output_tsv))