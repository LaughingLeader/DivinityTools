import os, sys
from pathlib import Path
import glob
import dos2de_common as common
import timeit
import numpy as np
import plotly.graph_objs as go
import plotly.offline
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, fig, exec=True):
        # Create a QApplication instance or use the existing one if it exists
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

        super().__init__()

        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp.html"))
        plotly.offline.plot(fig, filename=self.file_path, auto_open=False)
        self.load(QUrl.fromLocalFile(self.file_path))
        self.setWindowTitle("Vitality Scaling")
        self.show()

        if exec:
            self.app.exec_()

    def closeEvent(self, event):
        os.remove(self.file_path)

import dos2de_extradata as ext

Ext = ext.ExtTable()

def SetLoweredScale():
    global Ext
    Ext.ExtraData.VitalityLinearGrowth = 25
    Ext.ExtraData.VitalityStartingAmount = 175
    Ext.ExtraData.VitalityExponentialGrowth = 1
    Ext.ExtraData.VitalityToDamageRatio = 5.7
    Ext.ExtraData.VitalityToDamageRatioGrowth = 0.11
    Ext.ExtraData.HealToDamageRatio = 1.6
    Ext.ExtraData.ExpectedDamageBoostFromAttributePerLevel = 0.04
    Ext.ExtraData.ExpectedDamageBoostFromSkillAbilityPerLevel = 0
    Ext.ExtraData.ExpectedDamageBoostFromWeaponAbilityPerLevel = 0
    Ext.ExtraData.FirstVitalityLeapGrowth = 1
    Ext.ExtraData.FirstVitalityLeapLevel = 9
    Ext.ExtraData.SecondVitalityLeapGrowth = 1
    Ext.ExtraData.SecondVitalityLeapLevel = 13
    Ext.ExtraData.ThirdVitalityLeapGrowth = 1
    Ext.ExtraData.ThirdVitalityLeapLevel = 16
    Ext.ExtraData.FourthVitalityLeapGrowth = 1
    Ext.ExtraData.FourthVitalityLeapLevel = 18

def GetVitalityExponential(level):
    expGrowth = Ext.ExtraData.VitalityExponentialGrowth
    growth = expGrowth ** (level - 1)

    if level >= Ext.ExtraData.FirstVitalityLeapLevel:
        growth = growth * Ext.ExtraData.FirstVitalityLeapGrowth / expGrowth

    if level >= Ext.ExtraData.SecondVitalityLeapLevel:
        growth = growth * Ext.ExtraData.SecondVitalityLeapGrowth / expGrowth

    if level >= Ext.ExtraData.ThirdVitalityLeapLevel:
        growth = growth * Ext.ExtraData.ThirdVitalityLeapGrowth / expGrowth

    if level >= Ext.ExtraData.FourthVitalityLeapLevel:
        growth = growth * Ext.ExtraData.FourthVitalityLeapGrowth / expGrowth

    return growth

def GetVitalityBoostByLevel(level):
    growth = GetVitalityExponential(level)
    vit = level * Ext.ExtraData.VitalityLinearGrowth + Ext.ExtraData.VitalityStartingAmount * growth
    return np.round(vit / 5.0) * 5.0

def GetLevelScaledDamage(level):
    vitalityBoost = GetVitalityBoostByLevel(level)
    return vitalityBoost / (((level - 1) * Ext.ExtraData.VitalityToDamageRatioGrowth) + Ext.ExtraData.VitalityToDamageRatio)

def GetAverageLevelDamage(level):
    scaled = GetLevelScaledDamage(level)
    return ((level * Ext.ExtraData.ExpectedDamageBoostFromAttributePerLevel) + 1.0) * scaled * ((level * Ext.ExtraData.ExpectedDamageBoostFromSkillAbilityPerLevel) + 1.0)

def GetLevelScaledWeaponDamage(level):
    scaledDmg = GetLevelScaledDamage(level)
    return scaledDmg / ((level * Ext.ExtraData.ExpectedDamageBoostFromWeaponAbilityPerLevel) + 1.0)

def CalculateVitality(level, baseVitality):
    vitalityBoost = np.round((level * Ext.ExtraData.VitalityLinearGrowth) + (Ext.ExtraData.VitalityStartingAmount * GetVitalityExponential(level))) / 5 * 5.0
    return vitalityBoost * baseVitality / 100

def CalculateArmorScaling(level, baseArmor):
    armorScaling = (GetVitalityBoostByLevel(level) * ((Ext.ExtraData.AttributeBaseValue + level * Ext.ExtraData.ExpectedConGrowthForArmorCalculation - Ext.ExtraData.AttributeBaseValue) * Ext.ExtraData.VitalityBoostFromAttribute) + 1.0) * Ext.ExtraData.ArmorToVitalityRatio
    armor = np.ceil(armorScaling * baseArmor / 100)
    return armor

def ScaledDamageFromPrimaryAttribute(primaryAttr):
    return (primaryAttr - Ext.ExtraData.AttributeBaseValue) * Ext.ExtraData.DamageBoostFromAttribute

#SetLoweredScale()

levels = []
for i in range(Ext.ExtraData.SoftLevelCap+1):
    levels.append(i)

def GetLevelVitalityData():
    v = []
    for i in range(Ext.ExtraData.SoftLevelCap+1):
        v.append(CalculateVitality(i, 100))
    return v

def GetLevelArmorData():
    v = []
    for i in range(Ext.ExtraData.SoftLevelCap+1):
        v.append(CalculateArmorScaling(i, 60))
    return v

def GetAverageDamageData():
    attributeDamageScale = ScaledDamageFromPrimaryAttribute(40)
    damageMultiplier = 1.0
    v = []
    for i in range(Ext.ExtraData.SoftLevelCap+1):
        v.append(np.ceil(GetAverageLevelDamage(i) * attributeDamageScale * damageMultiplier))
    return v

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=GetLevelVitalityData(),
    y=levels,
    name = 'Vitality', # Style name/legend entry with html tags
    connectgaps=True # override default to connect the gaps
))
fig.add_trace(go.Scatter(
    x=GetAverageDamageData(),
    y=levels,
    name='Average Level Damage',
))
fig.add_trace(go.Scatter(
    x=GetLevelArmorData(),
    y=levels,
    name='Average Armor',
))
win = PlotlyViewer(fig)