osiris_db_bullet_template = """
DB_LLWEAPONEX_Pistols_BulletTemplates("{name}", "{template}", "{status_weapon}", "{status_scaled}");
"""

osiris_db_leaveaction_template = """
LeaderLib_Statuses_Register_LeaveActionStatus("WeaponExpansion_LeaveActionStatuses", "{status_weapon}", "{skill_weapon}", 0);
LeaderLib_Statuses_Register_LeaveActionStatus("WeaponExpansion_LeaveActionStatuses", "{status_scaled}", "{skill_scaled}", 0);
"""

status_template = """
new entry "LLWEAPONEX_PISTOL_DAMAGE_{name_upper}_WEAPON"
type "StatusData"
data "StatusType" "CONSUME"
using "_LLWEAPONEX_HIDDEN_CONSUME_BASE"
data "LeaveAction" "Projectile_LLWEAPONEX_Pistol_Damage_{name}_Weapon"

new entry "LLWEAPONEX_PISTOL_DAMAGE_{name_upper}_SCALED"
type "StatusData"
data "StatusType" "CONSUME"
using "_LLWEAPONEX_HIDDEN_CONSUME_BASE"
data "LeaveAction" "Projectile_LLWEAPONEX_Pistol_Damage_{name}_Scaled"
"""

skill_template = """
new entry "Projectile_LLWEAPONEX_Pistol_Damage_{name}_Weapon"
type "SkillData"
data "SkillType" "Projectile"
using "_Projectile_LLWEAPONEX_Pistol_Damage_Weapon_Base"
data "DamageType" "{damage_type}"
data "DeathType" "{death_type}"
data "Template" "{projectile_template}"

new entry "Projectile_LLWEAPONEX_Pistol_Damage_{name}_Scaled"
type "SkillData"
data "SkillType" "Projectile"
using "_Projectile_LLWEAPONEX_Pistol_Damage_Scaled_Base"
data "DamageType" "{damage_type}"
data "DeathType" "{death_type}"
data "Template" "{projectile_template}"
"""

class PistolBullet():
	def __init__(self, name, root_template, projectile_template, damage_type, death_type):
		self.name = name
		if projectile_template == "": projectile_template = "db2307a5-2bdf-4d1a-9500-aebf36d91995"
		self.root_template = root_template
		self.projectile_template = projectile_template
		self.damage_type = damage_type
		self.death_type = death_type
		self.status_weapon = "LLWEAPONEX_PISTOL_DAMAGE_{name}_WEAPON".format(name=self.name.upper())
		self.status_scaled = "LLWEAPONEX_PISTOL_DAMAGE_{name}_SCALED".format(name=self.name.upper())
		self.skill_weapon = "Projectile_LLWEAPONEX_Pistol_Damage_{name}_Weapon".format(name=self.name)
		self.skill_scaled = "Projectile_LLWEAPONEX_Pistol_Damage_{name}_Scaled".format(name=self.name)
		self.db_bullet = osiris_db_bullet_template.format(
			name=self.name,template=self.root_template,status_weapon=self.status_weapon,status_scaled=self.status_scaled
		)
		self.db_leaveaction = osiris_db_leaveaction_template.format(
			skill_weapon=self.skill_weapon,skill_scaled=self.skill_scaled,status_weapon=self.status_weapon,status_scaled=self.status_scaled)
		self.status_entry = status_template.format(name=self.name, name_upper=self.name.upper())
		self.skill_template = skill_template.format(name=self.name, damage_type=self.damage_type, 
			death_type=self.death_type, projectile_template=self.projectile_template)
bullets = [
	PistolBullet("Default", "", "", "Physical", "Physical"),
	PistolBullet("ArmorPiercing", "", "", "Piercing", "Piercing"),
	PistolBullet("Air", "", "", "Air", "Electrocution"),
	PistolBullet("Earth", "", "", "Earth", "DoT"),
	PistolBullet("Fire", "", "", "Fire", "Incinerate"),
	PistolBullet("Poison", "", "", "Poison", "Acid"),
	PistolBullet("Water", "", "", "Water", "FrozenShatter"),
]

import os
from pathlib import Path
import dos2de_common as Common

output_osiris_bullet_str = ""
output_osiris_leaveaction_str = ""
output_status_str = ""
output_skills_str = ""

for bullet in bullets:
	output_osiris_bullet_str += bullet.db_bullet
	output_osiris_leaveaction_str += bullet.db_leaveaction
	output_status_str += bullet.status_entry
	output_skills_str += bullet.skill_template

Common.export_file(Path("Generated").joinpath("LLWEAPONEX_PistolBullets_Osiris_BulletsDB.txt"), output_osiris_bullet_str)
Common.export_file(Path("Generated").joinpath("LLWEAPONEX_PistolBullets_Osiris_LeaveActionDB.txt"), output_osiris_leaveaction_str)
Common.export_file(Path("Generated").joinpath("LLWEAPONEX_PistolBullets_Statuses.txt"), output_status_str)
Common.export_file(Path("Generated").joinpath("LLWEAPONEX_PistolBullets_Skills.txt"), output_skills_str)