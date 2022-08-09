import json
from pathlib import Path
from typing import List,Dict
import operator
from collections import OrderedDict

import dos2de_common as Common

base = [
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Default\\inputconfig.json",
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Default\\inputconfig_controller.json",
]

files = [
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\keyboard_1.json",
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\controller_1.json",
    "D:\\Users\\LaughingLeader\\Documents\\Larian Studios\\Divinity Original Sin 2 Definitive Edition\\PlayerProfiles\\LaughingLeader\\inputconfig_p1.json",
]

debug_files = [
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\keyboard_debug.json",
    "D:\\Modding\\DOS2DE_Extracted\\PlayerProfiles\\Eoc\\controller_debug.json",
]

ignored = [
    "FlashMouseMove",
    # Throws errors in the editor
    "Action2",
    "Action3",
    "LinkDevice",
    "TogglePause",
    "UIRPSAutoResolve",
    "UITradeConfirmOffer",
    "UITradeMarkOffer",
    "WidgetSliderDecrease",
    "WidgetSliderIncrease",
]

ignored_keyword = [
    "Perfmon",
    "Mouse"
]

def ignore_input(key):
    for k in ignored:
        if key == k:
            return True
    for k in ignored_keyword:
        if k in key:
            return True
    return False

def get_keys(enable_debug=True)->Dict[str,List[str]]:
    inputEvents:Dict[str,List[str]] = {}

    target_files = []
    target_files.extend(base)
    target_files.extend(files)
    if enable_debug:
        target_files.extend(debug_files)

    for fpath in target_files:
        f = Path(fpath)
        contents = Common.load_file(f)
        if contents is not None:
            jdata = json.loads(contents)
            for k,v in jdata.items():
                saved:List[str] = inputEvents.get(k)
                if saved is None:
                    inputEvents[k] = []
                    saved = inputEvents[k]
                for key in v:
                    if not key in saved:
                        saved.append(key)
    with open('Generated/input-all.json', 'w', encoding='utf-8') as fp:
        #json.dump(inputEvents, fp, indent='\t')
        fp.write(Common.to_json(OrderedDict(sorted(inputEvents.items()))))
    return inputEvents

def export_flash(inputEvents=None):
    inputEvents = inputEvents or get_keys(False)
    events_str = ",".join(['"IE {}"'.format(x) for x in sorted(inputEvents.keys()) if not ignore_input(x)])
    output_str = "this.events = new Array({});".format(events_str)
    Common.export_file(Path("Generated/FlashInputEvents.txt"), output_str)

export_flash()

# this.events = new Array("IE Action1","IE ActionCancel","IE ActionMenu","IE AreaPickup","IE Benchmark","IE CCZoomIn","IE CCZoomOut","IE CameraBackward","IE CameraCenter","IE CameraForward","IE CameraLeft","IE CameraRight","IE CameraRotateLeft","IE CameraRotateMouseLeft","IE CameraRotateMouseRight","IE CameraRotateRight","IE CameraToggleMouseRotate","IE CameraZoomIn","IE CameraZoomOut","IE CancelSelectorMode","IE CharacterCreationAccept","IE CharacterCreationRotateLeft","IE CharacterCreationRotateRight","IE CharacterMoveBackward","IE CharacterMoveForward","IE CharacterMoveLeft","IE CharacterMoveRight","IE CloseApplication","IE Combine","IE ConnectivityMenu","IE ContextMenu","IE ControllerContextMenu","IE CycleCharactersNext","IE CycleCharactersPrev","IE DefaultCameraBackward","IE DefaultCameraCaptureInput","IE DefaultCameraFast","IE DefaultCameraForward","IE DefaultCameraFrontView","IE DefaultCameraLeft","IE DefaultCameraLeftView","IE DefaultCameraMouseDown","IE DefaultCameraMouseLeft","IE DefaultCameraMouseRight","IE DefaultCameraMouseUp","IE DefaultCameraPanCamera","IE DefaultCameraRight","IE DefaultCameraRotateDown","IE DefaultCameraRotateLeft","IE DefaultCameraRotateRight","IE DefaultCameraRotateUp","IE DefaultCameraSlow","IE DefaultCameraSpecialPanCamera1","IE DefaultCameraSpecialPanCamera2","IE DefaultCameraToggleMouseRotation","IE DefaultCameraTopView","IE DefaultCameraZoomIn","IE DefaultCameraZoomOut","IE DestructionToggle","IE DragSingleToggle","IE FlashAlt","IE FlashArrowDown","IE FlashArrowLeft","IE FlashArrowRight","IE FlashArrowUp","IE FlashBackspace","IE FlashCancel","IE FlashCtrl","IE FlashDelete","IE FlashEnd","IE FlashEnter","IE FlashHome","IE FlashLeftMouse","IE FlashMiddleMouse","IE FlashMouseMoveDown","IE FlashMouseMoveLeft","IE FlashMouseMoveRight","IE FlashMouseMoveUp","IE FlashPgDn","IE FlashPgUp","IE FlashRightMouse","IE FlashScrollDown","IE FlashScrollUp","IE FlashTab","IE FreeCameraFoVDec","IE FreeCameraFoVInc","IE FreeCameraFreezeGameTime","IE FreeCameraHeightDec","IE FreeCameraHeightInc","IE FreeCameraMoveBackward","IE FreeCameraMoveForward","IE FreeCameraMoveLeft","IE FreeCameraMoveRight","IE FreeCameraRotSpeedDec","IE FreeCameraRotSpeedInc","IE FreeCameraRotateControllerDown","IE FreeCameraRotateControllerLeft","IE FreeCameraRotateControllerRight","IE FreeCameraRotateControllerUp","IE FreeCameraRotateMouseDown","IE FreeCameraRotateMouseLeft","IE FreeCameraRotateMouseRight","IE FreeCameraRotateMouseUp","IE FreeCameraSlowdown","IE FreeCameraSpeedDec","IE FreeCameraSpeedInc","IE FreeCameraSpeedReset","IE FreeCameraToggleMouseRotate","IE GMKillResurrect","IE GMNormalAlignMode","IE GMSetHealth","IE HighlightCharacters","IE Interact","IE MoveCharacterUpInGroup","IE NextObject","IE PanelSelect","IE PartyManagement","IE Pause","IE Ping","IE PrevObject","IE QueueCommand","IE QuickLoad","IE QuickSave","IE ReloadInputConfig","IE RotateItemLeft","IE RotateItemRight","IE Screenshot","IE SelectorMoveBackward","IE SelectorMoveForward","IE SelectorMoveLeft","IE SelectorMoveRight","IE ShowChat","IE ShowSneakCones","IE ShowWorldTooltips","IE SkipVideo","IE SplitItemToggle","IE SwitchGMMode","IE ToggleCharacterPane","IE ToggleCombatMode","IE ToggleCraft","IE ToggleEquipment","IE ToggleFullscreen","IE ToggleGMInventory","IE ToggleGMItemGeneratorPane","IE ToggleGMMiniMap","IE ToggleGMMoodPanel","IE ToggleGMPause","IE ToggleGMRewardPanel","IE ToggleGMShroud","IE ToggleHomestead","IE ToggleInGameMenu","IE ToggleInfo","IE ToggleInputMode","IE ToggleInventory","IE ToggleJournal","IE ToggleManageTarget","IE ToggleMap","IE ToggleMonsterSelect","IE ToggleOverviewMap","IE TogglePartyManagement","IE TogglePresentation","IE ToggleRecipes","IE ToggleReputationPanel","IE ToggleRollPanel","IE ToggleSetStartPoint","IE ToggleSkills","IE ToggleSneak","IE ToggleSplitscreen","IE ToggleStatusPanel","IE ToggleSurfacePainter","IE ToggleTacticalCamera","IE ToggleVignette","IE UIAccept","IE UIAddPoints","IE UIAddonDown","IE UIAddonUp","IE UIBack","IE UICancel","IE UICompareItems","IE UIContextMenuModifier","IE UICopy","IE UICreateProfile","IE UICreationAddSkill","IE UICreationEditClassNext","IE UICreationEditClassPrev","IE UICreationNext","IE UICreationPrev","IE UICreationRemoveSkill","IE UICreationTabNext","IE UICreationTabPrev","IE UICut","IE UIDelete","IE UIDeleteProfile","IE UIDialogRPSPaper","IE UIDialogRPSRock","IE UIDialogRPSScissors","IE UIDialogTextDown","IE UIDialogTextUp","IE UIDown","IE UIEditCharacter","IE UIEndTurn","IE UIFilter","IE UIHotBarNext","IE UIHotBarPrev","IE UIInvite","IE UILeft","IE UIMapDown","IE UIMapLeft","IE UIMapRemoveMarker","IE UIMapReset","IE UIMapRight","IE UIMapUp","IE UIMapZoomIn","IE UIMapZoomOut","IE UIMarkWares","IE UIMessageBoxA","IE UIMessageBoxB","IE UIMessageBoxX","IE UIMessageBoxY","IE UIModNext","IE UIModPrev","IE UIPaste","IE UIRadialDown","IE UIRadialLeft","IE UIRadialRight","IE UIRadialUp","IE UIRefresh","IE UIRemoveItemSelection","IE UIRemovePoints","IE UIRename","IE UIRequestTrade","IE UIRight","IE UISelectChar1","IE UISelectChar2","IE UISelectChar3","IE UISelectChar4","IE UISelectSlot0","IE UISelectSlot1","IE UISelectSlot11","IE UISelectSlot12","IE UISelectSlot2","IE UISelectSlot3","IE UISelectSlot4","IE UISelectSlot5","IE UISelectSlot6","IE UISelectSlot7","IE UISelectSlot8","IE UISelectSlot9","IE UISend","IE UISetSlot","IE UIShowInfo","IE UIShowTooltip","IE UIStartGame","IE UISwitchDown","IE UISwitchLeft","IE UISwitchRight","IE UISwitchUp","IE UITabNext","IE UITabPrev","IE UITakeAll","IE UIToggleActions","IE UIToggleEquipment","IE UIToggleHelmet","IE UIToggleMultiselection","IE UIToggleTutorials","IE UITooltipDown","IE UITooltipUp","IE UITradeBalance","IE UITradeRemoveOffer","IE UITradeSwitchWindow","IE UIUp","IE WidgetButtonA","IE WidgetButtonBackSpace","IE WidgetButtonC","IE WidgetButtonDelete","IE WidgetButtonDown","IE WidgetButtonEnd","IE WidgetButtonEnter","IE WidgetButtonEscape","IE WidgetButtonHome","IE WidgetButtonLeft","IE WidgetButtonPageDown","IE WidgetButtonPageUp","IE WidgetButtonRight","IE WidgetButtonSpace","IE WidgetButtonTab","IE WidgetButtonUp","IE WidgetButtonV","IE WidgetButtonX","IE WidgetButtonY","IE WidgetButtonZ","IE WidgetMouseLeft","IE WidgetMouseMotion","IE WidgetMouseRight","IE WidgetScreenshot","IE WidgetScreenshotVideo","IE WidgetScrollDown","IE WidgetScrollUp","IE WidgetToggleDebugConsole","IE WidgetToggleDevComments","IE WidgetToggleEffectStats","IE WidgetToggleGraphicsDebug","IE WidgetToggleHierarchicalProfiler","IE WidgetToggleOptions","IE WidgetToggleOutput","IE WidgetToggleStats");