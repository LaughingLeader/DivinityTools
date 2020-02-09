resistance = 150.0
damage = 200


res_mod = 1 - (100 - resistance) / 100

print("Damage: {} | Resistance: {} | Res Mod: {}".format(damage, resistance, res_mod))

damage = damage - (damage * res_mod)

print("Final damage: {}".format(damage))