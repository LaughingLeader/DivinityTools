import os
import sys
import pathlib
from pathlib import Path

statuses_template = """
new entry \"LLWEAPONEX_HANDCROSSBOW_SHOOT_HIT_{damage_type_name}\"
type \"StatusData\"
data \"StatusType\" \"CONSUME\"
using \"LLWEAPONEX_HIDDEN_CONSUME_BASE\"

new entry \"LLWEAPONEX_HANDCROSSBOW_SHOOT_DAMAGE_SCALED_{damage_type_name}\"
type \"StatusData\"
data \"StatusType\" \"DAMAGE\"
using \"LLWEAPONEX_HIDDEN_DAMAGE_BASE\"
data \"LeaveAction\" \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}_ScaledDamage\"

new entry \"LLWEAPONEX_HANDCROSSBOW_SHOOT_DAMAGE_WEAPON_{damage_type_name}\"
type \"StatusData\"
data \"StatusType\" \"DAMAGE\"
using \"LLWEAPONEX_HIDDEN_DAMAGE_BASE\"
data \"LeaveAction\" \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}_WeaponDamage\"
"""

skill_template_explodingstatus = """
new entry \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}_WeaponDamage\"
type \"SkillData\"
data \"SkillType\" \"Projectile\"
using \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_Default_WeaponDamage\"
data \"Ability\" \"{school}\"
data \"DamageType\" \"{damage_type}\"

new entry \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}_ScaledDamage\"
type \"SkillData\"
data \"SkillType\" \"Projectile\"
using \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_Default_ScaledDamage\"
data \"Ability\" \"{school}\"
data \"DamageType\" \"{damage_type}\"
"""

skill_template_handcrossbow_shoot = """
new entry \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}\"
type \"SkillData\"
data \"SkillType\" \"Projectile\"
using \"Projectile_LLWEAPONEX_HandCrossbow_Shoot\"
data \"Ability\" \"{school}\"
data \"DamageType\" \"{damage_type}\"
data \"Template\" \"{template}\"
data \"DisplayName\" \"Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}_DisplayName\"
data \"SkillProperties\" \"LLWEAPONEX_HANDCROSSBOW_SHOOT_HIT_{damage_type_name},100,0;{skillproperties}\"
data \"StatsDescriptionParams\" \"Skill:Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}_WeaponDamage:Damage;Skill:Projectile_LLWEAPONEX_HandCrossbow_Shoot_{damage_type}_ScaledDamage:Damage\"
"""

osiris_rules_template = """
IF
CharacterStatusAttempt(_Target, \"LLWEAPONEX_HANDCROSSBOW_SHOOT_HIT_{damage_type_name}\", (CHARACTERGUID)_Cause)
AND
NOT LeaderLib_Helper_QRY_WeaponIsEquipped(_Cause)
THEN
ApplyStatus(_Target, \"LLWEAPONEX_HANDCROSSBOW_SHOOT_DAMAGE_SCALED_{damage_type_name}\", 0.0, 1, _Cause);

IF
CharacterStatusAttempt(_Target, \"LLWEAPONEX_HANDCROSSBOW_SHOOT_HIT_{damage_type_name}\", (CHARACTERGUID)_Cause)
AND
LeaderLib_Helper_QRY_WeaponIsEquipped(_Cause)
THEN
ApplyStatus(_Target, \"LLWEAPONEX_HANDCROSSBOW_SHOOT_DAMAGE_WEAPON_{damage_type_name}\", 0.0, 1, _Cause);
"""

elements = [
    ("Default", "263e73fd-7c5d-48e7-8ebf-541c71c28004", "None", ""),
    ("Air", "b8e28d9a-c987-4cf7-8526-a0ee22771d45", "Air", "Electrify"),
    ("Corrosive", "d022f585-942c-498d-8211-9b97a3eeaadd", "None", "Melt;ACID,100,1"),
    ("Earth", "6cd56bf4-69d9-428b-a91b-87cdd1318d4e", "Earth", "Oilify;SLOWED,100,1"),
    ("Fire", "9ec7b36e-7baa-474e-9cc0-cd7023bb50f7", "Fire", "Ignite;BURNING,100,1"),
    ("Poison", "53c8524c-8227-4f19-9d1e-eb982e8cc220", "Poison", "Contaminate;POISONED,100,1"),
    ("Shadow", "80aecd6e-7fa1-4afc-aa5f-c5f6d578b79c", "Death", "Curse;CURSED,100,1"),
    ("Water", "54427696-0863-4b1a-9041-34d5b4e6e86c", "Water", "Freeze;CHILLED,100,1")
]

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

def export_file(path, contents):
    try:
        f = open(str(path.absolute()), 'w')
        f.write(contents)
        f.close()
        return True
    except Exception as e:
        print("Erroring writing '{}': {}".format(path.name, e))
    return False

output_statuses = ""
output_skills_status = ""
output_skills_shoot = ""
output_script = ""

for x in elements:
    damage_type = x[0]
    template = x[1]
    school = x[2]
    skillproperties = x[3]
    damage_type_upper = damage_type.upper()

    output_statuses += statuses_template.format(
        damage_type = damage_type, damage_type_name=damage_type_upper)
    output_skills_status += skill_template_explodingstatus.format(
        damage_type = damage_type, school=school)
    output_skills_shoot += skill_template_handcrossbow_shoot.format(
        damage_type = damage_type, skillproperties=skillproperties,
        school=school, template = template, damage_type_name=damage_type_upper)
    output_script += osiris_rules_template.format(damage_type_name=damage_type_upper)
    
export_file(script_dir.joinpath("Generated/Statuses_Generated.txt"), output_statuses)
export_file(script_dir.joinpath("Generated/Skills_Statuses_Generated.txt"), output_skills_status)
export_file(script_dir.joinpath("Generated/Skills_Shoot_Generated.txt"), output_skills_shoot)
export_file(script_dir.joinpath("Generated/StoryScript_Generated.txt"), output_script)

# import pyperclip
# pyperclip.copy(output_str)
# print("Generated text copied to clipboard.")

