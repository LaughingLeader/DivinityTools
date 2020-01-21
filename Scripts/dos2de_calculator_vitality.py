import numpy
import math
from pathlib import Path
import dos2de_common as Common
import re

data_vals = {
	"VitalityStartingAmount": 21,
	"VitalityExponentialGrowth": 1.25,
	"VitalityLinearGrowth": 9.091,
	"VitalityToDamageRatio": 5,
	"VitalityToDamageRatioGrowth": 0.2,
	"ExpectedDamageBoostFromAttributePerLevel": 0.065,
	"ExpectedDamageBoostFromSkillAbilityPerLevel": 0.015,
	"ExpectedDamageBoostFromWeaponAbilityPerLevel": 0.025,
	"ExpectedConGrowthForArmorCalculation": 1,
	"FirstVitalityLeapLevel": 9,
	"FirstVitalityLeapGrowth": 1.25,
	"HealToDamageRatio": 1.3,
	"SecondVitalityLeapLevel": 13,
	"SecondVitalityLeapGrowth": 1.25,
	"ThirdVitalityLeapLevel": 16,
	"ThirdVitalityLeapGrowth": 1.25,
	"FourthVitalityLeapLevel": 18,
	"FourthVitalityLeapGrowth": 1.35
}

data_text_path = Path("G:/Divinity Original Sin 2/DefEd/Data/Public/SmallerNumbers_b49064ba-f316-465e-b6b5-7380a14c8910/Stats/Generated/Data/Data.txt")
key_pattern = re.compile('^key "(.*?)","(.*?)".*$', re.MULTILINE | re.IGNORECASE)

with open(data_text_path.absolute()) as f:
	file_str = f.read()
	matches = list(key_pattern.finditer(file_str))
	for m in matches:
		keyName = m.group(1)
		keyValueStr = m.group(2)
		if keyName is not None and keyName != "" and keyValueStr != None and keyValueStr != "":
			keyValue = float(keyValueStr)
			data_vals[keyName] = keyValue

level = 20
healValue = 100
vitality = 100

VitalityExponentialGrowth = data_vals["VitalityExponentialGrowth"]
FirstVitalityLeapLevel = data_vals["FirstVitalityLeapLevel"]
FirstVitalityLeapGrowth = data_vals["FirstVitalityLeapGrowth"]
SecondVitalityLeapLevel = data_vals["SecondVitalityLeapLevel"]
SecondVitalityLeapGrowth = data_vals["SecondVitalityLeapGrowth"]
ThirdVitalityLeapLevel = data_vals["ThirdVitalityLeapLevel"]
ThirdVitalityLeapGrowth = data_vals["ThirdVitalityLeapGrowth"]
FourthVitalityLeapLevel = data_vals["FourthVitalityLeapLevel"]
FourthVitalityLeapGrowth = data_vals["FourthVitalityLeapGrowth"]
VitalityLinearGrowth = data_vals["VitalityLinearGrowth"]
VitalityStartingAmount = data_vals["VitalityStartingAmount"]
VitalityToDamageRatioGrowth = data_vals["VitalityToDamageRatioGrowth"]
VitalityToDamageRatio = data_vals["VitalityToDamageRatio"]
ExpectedDamageBoostFromSkillAbilityPerLevel = data_vals["ExpectedDamageBoostFromSkillAbilityPerLevel"]
HealToDamageRatio = data_vals["HealToDamageRatio"]

vitalityExp = pow(VitalityExponentialGrowth, level - 1)
if level >= FirstVitalityLeapLevel:
	vitalityExp = vitalityExp * FirstVitalityLeapGrowth / VitalityExponentialGrowth

if level >= SecondVitalityLeapLevel:
	vitalityExp = vitalityExp * SecondVitalityLeapGrowth / VitalityExponentialGrowth

if level >= ThirdVitalityLeapLevel:
	vitalityExp = vitalityExp * ThirdVitalityLeapGrowth / VitalityExponentialGrowth

if level >= FourthVitalityLeapLevel:
	vitalityExp = vitalityExp * FourthVitalityLeapGrowth / VitalityExponentialGrowth

vitalityBoost = round((level * VitalityLinearGrowth) + (VitalityStartingAmount * vitalityExp), 9) / 5 * 5.0

levelScaledDamage = vitalityBoost / (((level - 1) * VitalityToDamageRatioGrowth) + VitalityToDamageRatio)

averageLevelDamage = ((((level * ExpectedDamageBoostFromSkillAbilityPerLevel) + 1.0) * levelScaledDamage)
       * ((level * ExpectedDamageBoostFromSkillAbilityPerLevel) + 1.0))

skill_healing_scale = round(healValue * averageLevelDamage * HealToDamageRatio / 100.0, 9)

print("Heal scale for {} at level {} = {}".format(healValue, level, skill_healing_scale))

vitalityBoost = round((level * VitalityLinearGrowth) + (VitalityStartingAmount * vitalityExp), 9) / 5 * 5.0
vitality_result = (vitalityBoost * vitality) / 100

# (20 * 13) + (50 * 14) / 5 * 5.0
# (260) + (700) / 5 * 5.0
# (960) / 5 * 5.0

# 9015 = (vitalityBoost * vitality) / 100
# 9015 = (960 * 100) / 100

print("Vitality scale for {} base vit at level {} = {} | vitalityExp: {} | vitalityBoost: {}".format(vitality, level, vitality_result, vitalityExp, vitalityBoost))