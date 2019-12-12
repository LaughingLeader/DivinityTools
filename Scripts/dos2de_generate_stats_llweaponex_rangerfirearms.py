

skills = [
	("Projectile_Multishot", "Projectile_LLWEAPONEX_Firearm_Multishot", "deb24a84-006f-4a3a-b4bb-b40fa52a447d"),
	("Projectile_EnemyMultishot", "Projectile_LLWEAPONEX_Firearm_Multishot_Enemy", "deb24a84-006f-4a3a-b4bb-b40fa52a447d"),
	("Projectile_SkyShot", "Projectile_LLWEAPONEX_Firearm_SkyShot", "e44859b2-d55f-47e2-b509-fd32d7d3c745"),
	("Projectile_EnemySkyShot", "Projectile_LLWEAPONEX_Firearm_SkyShot_Enemy", "e44859b2-d55f-47e2-b509-fd32d7d3c745"),
	("Projectile_ArrowSpray", "Projectile_LLWEAPONEX_Firearm_ArrowSpray", "7ce736c8-1e02-462d-bee2-36bd86bd8979"),
	("Projectile_EnemyArrowSpray", "Projectile_LLWEAPONEX_Firearm_ArrowSpray_Enemy", "7ce736c8-1e02-462d-bee2-36bd86bd8979"),
	("Projectile_PiercingShot", "Projectile_LLWEAPONEX_Firearm_PiercingShot", "d4eebf4d-4f0c-4409-8fe8-32efeca06453"),
	("Projectile_EnemyPiercingShot", "Projectile_LLWEAPONEX_Firearm_PiercingShot_Enemy", "d4eebf4d-4f0c-4409-8fe8-32efeca06453"),
	("Projectile_Snipe", "Projectile_LLWEAPONEX_Firearm_Snipe", "fbf17754-e604-4772-813a-3593b4e7bec8"),
	("Projectile_EnemySnipe", "Projectile_LLWEAPONEX_Firearm_Snipe_Enemy", "fbf17754-e604-4772-813a-3593b4e7bec8"),
	("Projectile_Ricochet", "Projectile_LLWEAPONEX_Firearm_Ricochet", "22cae5a3-8427-4526-aa7f-4f277d0ff67e"),
	("Projectile_EnemyRicochet", "Projectile_LLWEAPONEX_Firearm_Ricochet_Enemy", "22cae5a3-8427-4526-aa7f-4f277d0ff67e"),
	("Projectile_BallisticShot", "Projectile_LLWEAPONEX_Firearm_BallisticShot", "7c31f878-1f04-47bb-b8b1-05e605dc0b60"),
	("Projectile_EnemyBallisticShot", "Projectile_LLWEAPONEX_Firearm_BallisticShot_Enemy", "7c31f878-1f04-47bb-b8b1-05e605dc0b60"),
	("Projectile_PinDown", "Projectile_LLWEAPONEX_Firearm_PinDown", "8814954c-b0d1-4cdf-b075-3313ac71cf20"),
	("Projectile_EnemyPinDown", "Projectile_LLWEAPONEX_Firearm_PinDown_Enemy", "8814954c-b0d1-4cdf-b075-3313ac71cf20")
]

skill_template = """
new entry "{skill}"
type "SkillData"
data "SkillType" "Projectile"
using "{target}"
data "Template" "{template}"
data "DisplayName" "{name}_DisplayName"
data "Description" "{name}_Description"
data "SkillProperties" "SELF:LLWEAPONEX_FIREARM_SHOOT_EXPLOSION_FX,100,-2"
"""
#data "Memory Cost" "0"

locale_template = """
{name}_DisplayName\t
{name}_Description\t
"""

import os
from pathlib import Path
import dos2de_common as Common

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

output_str = ""
locale_str = ""

skills.sort(key=lambda x: x[1])

for target,skill,template in skills:
	output_str += skill_template.format(skill=skill, target=target, template=template, name=skill.replace("_Enemy", "").replace("Enemy", ""))
	if not "Enemy" in skill:
		locale_str += locale_template.format(name=skill)

#output_str += locale_str

Common.export_file(Path("Generated").joinpath("Skills_Firearms_RangerAlternatives.txt"), output_str)