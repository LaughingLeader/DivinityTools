import json
from pathlib import Path
from typing import List,Dict
import operator

import dos2de_common as Common
import dos2de_generate_input_event_array as input_array

inputEvents = input_array.get_keys()
input_array.export_flash()

name_map_manual = {
    "|Enable alignment to surface when moving/placing objects as Game Master|": "GMNormalAlignMode",
    "|Game Master Charactersheet|": "ToggleManageTarget",
    "|Game Master Inventory|": "ToggleGMInventory",
    "|Game Master target Kill/Resurrect|": "GMKillResurrect",
    "|Game Master target set Health|": "GMSetHealth",
    "|Game Master toggle minimap|": "ToggleGMMiniMap",
    "|Place ping beacon|": "Ping",
    "|Switch between GM mode and Possess mode|": "SwitchGMMode",
    "|Toggle the Item Generator Panel|": "ToggleGMItemGeneratorPane",
    "|Toggle the Mood Panel|": "ToggleGMMoodPanel",
    "|Toggle the Reward Panel|": "ToggleGMRewardPanel",
    "Balance Offer": "UITradeBalance",
    "Cancel Action": "ActionCancel",
    "Character Creation Zoom in": "CCZoomIn",
    "Character Creation Zoom out": "CCZoomOut",
    "Choose PAPER in a RPS discussion": "UIDialogRPSPaper",
    "Choose ROCK in a RPS discussion": "UIDialogRPSRock",
    "Choose SCISSORS in a RPS discussion": "UIDialogRPSScissors",
    "Combine items": "Combine",
    "Decrease FreeCamera FoV": "FreeCameraFoVDec",
    "Decrease FreeCamera Rotation Speed": "FreeCameraRotSpeedDec",
    "Decrease FreeCamera Speed": "FreeCameraSpeedDec",
    "Delete": "UIDelete",
    "Deselect Character": "DebugDeselectCharacter",
    "Force Object Animation": "ForceAnimation",
    "Force Splitscreen": "ToggleSplitscreen",
    "FreeCamera Decrease Height": "FreeCameraHeightDec",
    "FreeCamera Increase Height": "FreeCameraHeightInc",
    "Increase FreeCamera FoV": "FreeCameraFoVInc",
    "Increase FreeCamera Rotation Speed": "FreeCameraRotSpeedInc",
    "Increase FreeCamera Speed": "FreeCameraSpeedInc",
    "Kill Combat": "DebugKillCombat",
    "Mark As Wares" : "UIMarkWares",
    "Switch trade window" : "UITradeSwitchWindow",
    "Toggle Game Master game pause": "ToggleGMPause",
    "Toggle Game Master Roll Panel": "ToggleRollPanel",
    "Toggle Game Master Shroud": "ToggleGMShroud",
    "TogglePartyManagement": "Party Management Toggle",
    "UI Map Reset" : "UIMapReset",
    "UI Remove marker" : "UIMapRemoveMarker",
    "Hide debug view" : "DebugViewHide",
    "Iggy explorer previous": "IggyExplorerPrev",
    "Iggy explorer next": "IggyExplorerNext",
    "Interract": "Interact",
    "Key Force End Turn": "ForceEndTurn",
    "Level Up": "DebugLevelUp",
    "Melt a surface": "MeltSurface",
    "MessageBox Accept": "UIMessageBoxA",
    "MessageBox Cancel": "UIMessageBoxB",
    "MessageBox Other 1": "UIMessageBoxX",
    "MessageBox Other 2": "UIMessageBoxY",
    "Move Character Backward": "CharacterMoveBackward",
    "Move Character Forward": "CharacterMoveForward",
    "Move Character Left": "CharacterMoveLeft",
    "Move Character Right": "CharacterMoveRight",
    "Move FreeCamera Backward": "FreeCameraMoveBackward",
    "Move FreeCamera Forward": "FreeCameraMoveForward",
    "Move FreeCamera Left": "FreeCameraMoveLeft",
    "Move FreeCamera Right": "FreeCameraMoveRight",
    "Panel Select Toggle": "PanelSelect",
    "Party Management Toggle": "PartyManagement",
    "Rotate Character Left": "CharacterCreationRotateLeft",
    "Rotate Character Right": "CharacterCreationRotateRight",
    "Scroll debug view down": "DebugViewScrollDown",
    "Scroll debug view up": "DebugViewScrollUp",
    "Select Character": "DebugSelectCharacter",
    "Send feedback": "UISend",
    "Slowdown FreeCamera speed": "FreeCameraSlowdown",
    "Switch between Debug parties": "SwitchDebugParty",
    "AiGrid take step": "DebugAIGridTakeStep",
    "Bless a surface": "BlessSurface",
    "Cancel Targetting": "CancelSelectorMode", # Not sure
    "Change skillbar item": "UIRemoveItemSelection", # Not sure
    "Creater Fire Surface": "CreateFireSurface",
    "Curse a surface": "CurseSurface",
    "Electrify a surface": "ElectrifySurface",
    "FreeCamera Mouse Rotation": "FreeCameraToggleMouseRotate",
    "Freeze a surface": "FreezeSurface",
    "Freeze Game Time": "FreeCameraFreezeGameTime",
    "Give some gold to the Character": "GiveSomeGold",
    "Remove item from hand": "UIRemoveItemSelection",
    "Remove item from offer": "UITradeRemoveOffer",
    "Reset FreeCamera Speed to default": "FreeCameraSpeedReset",
    "Toggle Actions Bar on Hot Bar": "UIToggleActions",
    "Toggle Blindness To Criminals": "ToggleBlindToCriminals",
    "Toggle Camera Rotate": "CameraToggleMouseRotate",
    "Toggle Character": "DebugToggleCharacter",
    "Toggle Character Panels": "ToggleCharacterPane",
    "Toggle Helmet": "UIToggleHelmet",
    "Toggle Multiselection": "UIToggleMultiselection",
    "Toggle Party Edit Window": "DebugTogglePartyEdit",
    "|Toggle Party Management Panel|": "TogglePartyManagement",
    "Toggle Presentation mode": "TogglePresentation",
    "Toggle Stats": "WidgetToggleStats",
    "Toggle Tutorials": "UIToggleTutorials",
    "Toggle Creatures & Items Panel": "ToggleMonsterSelect", # Not sure
    "UI Add Stat Points": "UIAddPoints",
    "UI Character Creation Add Skill": "UICreationAddSkill",
    "UI Character Creation Edit Class Next": "UICreationEditClassNext",
    "UI Character Creation Edit Class Previous": "UICreationEditClassPrev",
    "UI Character Creation Next": "UICreationNext",
    "UI Character Creation Previous": "UICreationPrev",
    "UI Character Creation Remove Skill": "UICreationRemoveSkill",
    "UI Character Creation Tab Next": "UICreationTabNext",
    "UI Character Creation Tab Previous": "UICreationTabPrev",
    "UI Compare selected item with currently equipped item": "UICompareItems",
    "UI Copy call": "UICopy",
    "UI Cut call": "UICut",
    "UI Paste call": "UIPaste",
    "UI Edit Selected Character": "UIEditCharacter",
    "UI Filter Elements": "UIFilter",
    "UI Invite player": "UIInvite",
    "UI Main Tab Next": "UITabNext",
    "UI Main Tab Previous": "UITabPrev",
    "UI Module Menu Move Add-on Down": "UIAddonDown",
    "UI Module Menu Move Add-on Up": "UIAddonUp",
    "UI Module Menu Next Mode": "UIModNext",
    "UI Module Menu Previous Mode": "UIModPrev",
    "UI Remove Stat Points": "UIRemovePoints",
    "UI Rename character": "UIRename",
    "UI Request trade dialog": "UIRequestTrade",
    "UI Scroll Tooltip Down": "WidgetScrollDown",
    "UI Scroll Tooltip Up": "WidgetScrollUp",
    "UI Scroll dialog text down": "UIDialogTextDown",
    "UI Scroll dialog text up": "UIDialogTextUp",
    "UI Show info panel": "UIShowInfo",
    "UI refresh page": "UIRefresh"
}

manual_id_map = dict([
    (1, "FlashLeftMouse"),
    (2, "FlashRightMouse"),
    (3, "FlashMiddleMouse"),
    (4, "FlashLeftMouse"),
])

name_map = {}
name_map.update(name_map_manual)
#name_map.update(name_map_generated)

def has_key(key:str, d:dict):
    for k in d.keys():
        if k == key:
            return True
        elif k.lower() == key.lower():
            return True
    return False

def get_name(name:str, d:dict):
    for k in d.keys():
        if k == name:
            return k
        elif k.lower() == name.lower():
            return k
    return name

def entry_in_list(x, list1):
    for entry in list1:
        if x.Name == entry.Name:
            return True
    return False

def unique_inputs(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if not entry_in_list(x, unique_list):
            unique_list.append(x)
    return unique_list

class InputEntry():
    def __init__(self, inputId=-1, name=""):
        self.InputID = int(inputId)
        self.Name = name
        self.DisplayName = ""
        self.Handle = ""

    @staticmethod
    def from_line(line:str):
        self = InputEntry()
        data = line.split("\t")
        #print(line, len(data))
        self.InputID = int(data[0])
        self.Name = str.replace(data[1], " ", "").replace("|", "")
        self.DisplayName = data[1]
        self.Handle = data[2]
        actual_name = name_map.get(self.Name) or name_map.get(self.DisplayName)
        if actual_name is not None and actual_name != "":
            self.Name = actual_name
        self.Name = get_name(self.Name, inputEvents)
        return self
    
    def export(self):
        return '["{}"] = InputEntry:Create({}, "{}", "{}")'.format(self.Name, self.InputID, self.DisplayName, self.Handle)
    
    def exportid(self):
        return '["{}"] = {}'.format(self.Name, self.InputID)

file = "DOS2 UI event IDs - Sheet1.tsv"

inputEntries:List[InputEntry] = []

with open(file, mode='r', encoding='utf-8') as f:
    inputEntries = [InputEntry.from_line(x.strip()) for x in f.readlines()]

valid_entries = [x for x in inputEntries if has_key(x.Name, inputEvents)]
missing_entries = sorted([x for x in inputEntries if not x in valid_entries], key=operator.attrgetter('Name'))

for inputId,name in manual_id_map.items():
    valid_entries.append(InputEntry(inputId, name))

valid_entries = sorted(valid_entries, key=operator.attrgetter('InputID'))

#entries_str = ",\n\t".join([x.export() for x in unique_inputs(valid_entries)])
export_input_dict = {}
for entry in valid_entries:
    existing = export_input_dict.get(entry.Name)
    if existing is None:
        export_input_dict[entry.Name] = entry.InputID
    else:
        print(entry.Name, existing, entry.InputID, type(existing))
        if type(existing) == "list":
            existing.append(entry.InputID)
        else:
            export_input_dict[entry.Name] = [existing, entry.InputID]

#entries_id_str = ",\n\t".join([x.exportid() for x in unique_inputs(valid_entries)])
entries_id_str = ",\n\t".join(['["{}"] = {}'.format(k, "{}".format(v).replace('[', '{').replace(']', '}')) for k,v in export_input_dict.items()])
#output_str = "InputEvents = {{\n\t{}\n}}".format(entries_str.strip())

input_enum_export = ",\n\t".join(['[{}] = "{}"'.format(x.InputID, x.Name) for x in valid_entries])
output_str2 = "Data.Input = {{\n\t{}\n}}\nData.InputEnum = {{\n\t{}\n}}".format(entries_id_str.strip(), input_enum_export.strip())
#missing_str = "name_map = {{\n\t{}\n\t{}\n}}".format(",\n\t".join(['"{}": "{}"'.format(k,v) for k,v in name_map_generated.items()]), ",\n\t".join(['"{}": ""'.format(x.DisplayName) for x in missing_entries]))
missing_str = "name_map_generated = {{\n\t{}\n}}".format(",\n\t".join(['"{}": ""'.format(x.DisplayName) for x in missing_entries]))
#Common.export_file(Path("Generated/InputKeyEntries.lua"), output_str.strip())
Common.export_file(Path("Generated/InputEvents.lua"), output_str2.strip())
Common.export_file(Path("Generated/MissingInputKeyEntries.py"), missing_str.strip())