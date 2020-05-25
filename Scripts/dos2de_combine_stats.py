import os
import sys
from pathlib import Path
from typing import List, Dict
import dos2de_common as Common

skills = [
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Cone.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_Cone.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Dome.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Jump.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_MultiStrike.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Projectile.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_Projectile.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_ProjectileStrike.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_ProjectileStrike.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Quake.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Rain.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Rush.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Shout.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_Shout.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Storm.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Summon.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_Summon.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Target.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_Target.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Teleportation.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_Teleportation.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Tornado.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Wall.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Skill_Zone.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Skill_Zone.txt",
]

statuses = [
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_ACTIVE_DEFENSE.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_BLIND.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_CHALLENGE.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_CHARMED.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_CONSUME.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Status_CONSUME.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_DAMAGE.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_DAMAGE_ON_MOVE.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_DEACTIVATED.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_DECAYING_TOUCH.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_DEMONIC_BARGAIN.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_DISARMED.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_EFFECT.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_EXTRA_TURN.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_FEAR.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_FLOATING.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_GUARDIAN_ANGEL.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_HEAL.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_HEAL_SHARING.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_HEAL_SHARING_CASTER.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_HEALING.txt",
	"D:/Modding/DOS2DE_Extracted/Public/DivinityOrigins_1301db3d-1f54-4e98-9be5-5094030916e4/Stats/Generated/Data/Status_HEALING.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_INCAPACITATED.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_INVISIBLE.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_KNOCKED_DOWN.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_MUTED.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_PLAY_DEAD.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_POLYMORPHED.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_SPARK.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_STANCE.txt",
	"D:/Modding/DOS2DE_Extracted/Public/Shared/Stats/Generated/Data/Status_THROWN.txt",
]

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

stats_output = script_dir.joinpath("Generated_CombinedStats")

skill_output:Path = stats_output.joinpath("SkillData.txt")
skill_output.parent.mkdir(parents=True, exist_ok=True)
with open(skill_output.absolute(), "wb") as outFile:
	for f in skills:
		with open(f, "rb") as infile:
			regionName = f.replace("D:/Modding/DOS2DE_Extracted/Public/", "").replace("/Stats/Generated/Data/", " - ")
			outFile.write("//REGION {}\n\n".format(regionName).encode())
			outFile.write(infile.read().decode().strip().encode())
			outFile.write("\n\n//REGION_END {}\n\n".format(regionName).encode())

status_output = stats_output.joinpath("StatusData.txt")
status_output.parent.mkdir(parents=True, exist_ok=True)
with open(status_output.absolute(), "wb") as outFile:
	for f in statuses:
		with open(f, "rb") as infile:
			regionName = f.replace("D:/Modding/DOS2DE_Extracted/Public/", "").replace("/Stats/Generated/Data/", " - ")
			outFile.write("//REGION {}\n\n".format(regionName).encode())
			outFile.write(infile.read().decode().strip().encode())
			outFile.write("\n\n//REGION_END {}\n\n".format(regionName).encode())