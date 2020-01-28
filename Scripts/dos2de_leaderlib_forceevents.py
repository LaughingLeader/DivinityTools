force_total = 20

single_template = """EVENT LeaderLib_Force_ShootProjectile_{type_name}_{num}
VARS
	{type1}:_Target
ON
	On{type_name}Event(_Target, "LeaderLib_Force_ShootProjectile_{num}")
ACTIONS
	ShootLocalProjectileAt(Projectile_LeaderLib_Force{num}, _Target, FLOAT3:{{0;3.0;0}}, _Target, 1, %LeaderLib_Force_TargetHelper)\n"""

multi_template = """EVENT LeaderLib_Force_ShootProjectile_{type_name}_{num}
VARS
	{type1}:_Source
	{type2}:_Target
ON
	On{type_name}Event(_Source, _Target, "LeaderLib_Force_ShootProjectile_{num}")
ACTIONS
	ShootLocalProjectileAt(Projectile_LeaderLib_Force{num}, _Source, FLOAT3:{{0;3.0;0}}, _Target, 1, %LeaderLib_Force_TargetHelper)\n"""

event_types = [
	("Character", "CHARACTER", ""),
	#("Item", "ITEM", ""),
	("CharacterItem", "CHARACTER", "ITEM"),
	("CharacterCharacter", "CHARACTER", "CHARACTER"),
]

output_str = ""

for data in event_types:
	type_name = data[0]
	type1 = data[1]
	type2 = data[2]
	block_str = "//REGION {}\n".format(type_name.upper())
	num = 1
	while num <= force_total:
		if type2 != "":
			block_str += multi_template.format(type_name=type_name, type1=type1, type2=type2, num=num)
		else:
			block_str += single_template.format(type_name=type_name, type1=type1, num=num)
		if num < force_total:
			block_str += "\n"
		num = num + 1
	block_str += "//END_REGION\n\n"
	output_str += block_str
import pyperclip
pyperclip.copy(output_str)