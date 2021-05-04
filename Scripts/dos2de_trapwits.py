import math

AttributeBaseValue = 10
AttributeLevelGrowth = 2
AttributeBoostGrowth = 0.75
WitsGrowthDamp = 0.5

DifficultyName = {
    "Normal": 2,
    "Easy": 0,
    "Hard": 4,
    "VeryHard": 6
}

def GetWits(difficulty, level=12):
    if difficulty > 1:
        diffMult = (difficulty - 1) / 100.0
        attributeVal = diffMult * (AttributeLevelGrowth + AttributeBoostGrowth) * level
        a = math.ceil(attributeVal) * WitsGrowthDamp
        final = a + AttributeBaseValue
        print("diffMult({}), attributeVal({}), a({}), final({})".format(diffMult, attributeVal, a, final))
        #return (math.ceil((((difficulty - 1) / 100.0) * (AttributeLevelGrowth + AttributeBoostGrowth)) * level) * WitsGrowthDamp) + AttributeBaseValue
        return final
    else:
        return AttributeBaseValue

def GetInput():
    diff = input("Input trap difficulty...")
    level = int(input("Input item level..."))
    diffName2Value = DifficultyName.get(diff)
    if diffName2Value is not None:
        diff = diffName2Value
    else:
        diff = int(diff)
    wits_val = GetWits(diff, level)
    print("Trap Difficulty ({})".format(diff))
    print("Level ({})".format(level))
    print("Wits required: {}".format(wits_val))

def TestRange():
    for i in range(30):
        wits_val = GetWits(6, i)
        print("Level ({})".format(i))
        print("Wits required: {}".format(wits_val))

TestRange()