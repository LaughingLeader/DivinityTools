

items = [
"WPN_LLWEAPONEX_CombatShield_Blackring_1H_A_ec353f1e-c1ca-46d1-83ef-e9f4fea14475",
"WPN_LLWEAPONEX_CombatShield_Common_1H_A_8c7da07b-ad11-4a0c-8406-0261977042b6",
"WPN_LLWEAPONEX_CombatShield_Dwarves_1H_A_bc034226-19bd-45e6-be7d-ec0d28c2e412",
"WPN_LLWEAPONEX_CombatShield_Elves_1H_B_1268f5f0-e484-42ea-8c13-0014e6aeaaad",
"WPN_LLWEAPONEX_CombatShield_Humans_1H_A_3a404dab-4862-4490-aa0f-bc27d06fdc6c",
"WPN_LLWEAPONEX_CombatShield_Lizards_1H_C_067f48be-857d-43a8-bd0a-add59f025843",
"WPN_LLWEAPONEX_Shield_DualShields_Blackring_A_9d98560d-916a-4ea0-8064-8a5ac8c13b45",
"WPN_LLWEAPONEX_Shield_DualShields_Common_A_8df9c20b-98f5-4f48-8438-573456fdfbf1",
"WPN_LLWEAPONEX_Shield_DualShields_Dwarves_A_91fd35cb-93dd-4489-9cf5-2dcc9b0ac168",
"WPN_LLWEAPONEX_Shield_DualShields_Elves_B_565e917f-ed53-40ed-8093-2133bc3e2a50",
"WPN_LLWEAPONEX_Shield_DualShields_Humans_A_c0bf83ff-5a55-4ac8-8a2b-9d9044c10d10",
"WPN_LLWEAPONEX_Shield_DualShields_Lizards_C_4f6f404a-06df-4041-bda6-87b7e24fd52e",
]

rule_template = """
IF
ItemTemplateAddedToCharacter({item}, _Item, _Char)
AND
IsTagged(_Item, "LLWEAPONEX_CombatShield", 1)
AND
NOT LeaderLib_Variables_QRY_ObjectVariableSet(_Item, "LLWEAPONEX_ParentDualShield")
THEN
"""

for item in items:
