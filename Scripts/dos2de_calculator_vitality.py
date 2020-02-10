import numpy
import math
from pathlib import Path
import dos2de_common as Common
import re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

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

def CalculateVitality(level, healValue, vitality):
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

    print("Vitality scale for {} base vit at level {} = {} | vitalityExp: {} | vitalityBoost: {}".format(vitality, level, vitality_result, vitalityExp, vitalityBoost))
    return vitality_result

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()

        self.level = IntVar(self, 1, name="level")
        self.vitality = IntVar(self, 100, name="vitality")
        self.healValue = IntVar(self, 100, name="healValue")
        self.result = IntVar(self, 0, name="result")

        vcmd = (self.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        self.title("DOS2DE Vitality Calculator")
        self.minsize(640, 400)
        self.wm_iconbitmap('')

        self.frame = Frame(self)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.frame.grid(row = 0, column = 0, sticky="w")

        self.levelLabel = ttk.Label(self.frame, text="Level", width=20)
        self.vitalityLabel = ttk.Label(self.frame, text="Base Vitality", width=20)
        self.resultLabel = ttk.Label(self.frame, text="Hitpoints", width=20)

        self.levelEntry = ttk.Entry(self.frame, validatecommand=vcmd, textvariable=self.level)
        self.vitalityEntry = ttk.Entry(self.frame, validatecommand=vcmd, textvariable=self.vitality)
        self.resultText = ttk.Label(self.frame, textvariable=self.result)
        self.button = ttk.Button(self.frame, text = "Calculate", command = self.calculate)

        self.frame.pack(expand=True)
        self.levelLabel.grid(column = 0, row = 0)
        self.vitalityLabel.grid(column = 0, row = 1)
        self.resultLabel.grid(column = 0, row = 2)
        self.levelEntry.grid(column=1, row=0)
        self.vitalityEntry.grid(column=1, row=1)
        self.resultText.grid(column=1, row=2)
        self.button.grid(column=1, row=3)

        self.levelEntry.bind("<KeyRelease>", self.calculate)
        self.vitalityEntry.bind("<KeyRelease>", self.calculate)

        # self.levelLabel.grid(column = 0, row = 0)
        # self.vitalityLabel.grid(column = 0, row = 1)
        # self.resultLabel.grid(column = 0, row = 2)
        # self.levelEntry.grid(column=1, row=0)
        # self.vitalityEntry.grid(column=1, row=1)
        # self.resultText.grid(column=1, row=2)
        # self.button.grid(column=1, row=3)

        self.calculate()

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def calculate(self, event=None):
        self.result.set(CalculateVitality(self.level.get(), self.healValue.get(), self.vitality.get()))
        

# c = Color(int("-8324348"))
# print("Color (-8324348) | a({}) r({}) g({}) b({}) = ({}) | ({})".format(
#   c.a, c.r, c.g, c.b, c.to_hex().upper(),
#       int32(c.to_int())))

# effect_files = list(startpath.glob('*.lsefx'))
# for f in effect_files:
#     load_colors(f.absolute(), [])

win = Root()
win.mainloop()