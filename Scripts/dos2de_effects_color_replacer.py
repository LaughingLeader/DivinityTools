import os
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from bs4 import BeautifulSoup
from numpy import int32

class Color():
    def __init__(self, argb:int, node=None):
        self.int = int32(argb)
        self.a = ((argb & 0xFF000000) >> 24)
        self.r = ((argb & 0x00FF0000) >> 16)
        self.g = ((argb & 0x0000FF00) >> 8)
        self.b = (argb & 0x000000FF)
        self.node = node
    
    def to_int(self) -> int:
        al = int32((self.a << 24) & 0xFF000000)
        rl = int32((self.r << 16) & 0x00FF0000)
        gl = int32((self.g << 8) & 0x0000FF00)
        bl = int32(self.b & 0x000000FF)
        return int32(al | rl | gl | bl)

    def to_hex(self) -> str:
        return '#%02x%02x%02x%02x' % (self.a, self.r, self.g, self.b)

    def debug_print(self):
        print("Color ({}) | a({}) r({}) g({}) b({}) = ({}) | ({})".format(
            self.int, self.a, self.r, self.g, self.b, self.to_hex().upper(), int32(self.to_int())))

# def int32(x):
#     if x>0xFFFFFFFF:
#         raise OverflowError
#     if x>0x7FFFFFFF:
#         x=int(0x100000000-x)
#     if x<2147483648:
#         return -x
#     else:
#         return -2147483648
#     return x

#startpath = Path('G:/Divinity Original Sin 2/DefEd/Data/Editor/Mods/ZZZ_GreenNecroFire_0bc91e73-ce14-4d3f-934c-3024a8ba348d/Assets/Effects')
#startpath = Path('G:\Divinity Original Sin 2\DefEd\Data\Editor\Mods\WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f\Assets\Effects')
#startpath = Path('G:\Divinity Original Sin 2\DefEd\Data\Editor\Mods\ZZZ_PurpleNecrofire_c46b8710-e5f5-45f5-9485-a3993e11c951\Assets\Effects')
#bacupfolder = Path('D:\Modding\DOS2DE\Projects_Source\PurpleNecrofire\Effects_Recolor_Backup')
startpath = Path('G:\Divinity Original Sin 2\DefEd\Data\Editor\Mods\WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f\Assets\Effects\_Rename')
bacupfolder = Path('G:\Divinity Original Sin 2\DefEd\Data\Editor\Mods\WeaponExpansion_c60718c3-ba22-4702-9c5d-5ad92b41ba5f\Assets\Effects\_Rename\Backup')
color_prop_id = {}
color_prop_id['particles'] = '93b34a52-eef2-4f88-80f6-19e3126188ca'
color_prop_id['light'] = '16caf8e6-d471-43da-b704-c845b1437927'
color_prop_id['ribbon'] = '5e5355ff-1c5f-48dd-888e-0129e288f8b6'
color_prop_id['decal'] = '329fc981-abb2-422d-a808-ffa6f62fb778'
color_prop_id['model'] = '1f15bd2c-f19a-437b-b98a-77c9631b9af0'
color_prop_id['overlay'] = '2acf47b9-3924-46f3-a7a1-b1a6cbace32a'

import datetime
today = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

def get_attribute_value(node, attribute_name):
    try:
        att = node[attribute_name]
        return str(att)
    except: pass
    return None

def get_color_nodes(xml):
    nodes = []
    for k,prop in color_prop_id.items():
        n = list(xml.find_all("rampchannel", {"id":prop}))
        if n != None and len(n) > 0:
            nodes.extend(n)
            print("Found color component for type '{}'".format(k))
    if len(nodes) > 0:
        return nodes
    return None

color_remap = {}

def export_file(path, contents):
	try:
		f = open(str(path.absolute()), 'w', encoding='utf-8')
		f.write(contents)
		f.close()
		return True
	except Exception as e:
		print("Error writing '{}': {}".format(path.name, e))
	return False

def swap_red_to_green(color):
    if color.r > color.g:
        g = color.g
        r = color.r
        color.r = g
        color.g = r
    return color

def swap_red_to_blue(color):
    if color.r > color.b:
        r = color.r
        b = color.b
        color.b = r
        color.r = b
    return color

def swap_red_to_purple(color):
    if color.r > color.b:
        r = color.r
        b = color.b
        color.b = r
        color.r = int(r/2)
    return color

def swap_green_to_blue(color):
    if color.g > color.b:
        g = color.g
        b = color.b
        color.b = g
        color.g = b
    return color

def swap_blue_to_red(color):
    if color.b > color.r:
        b = color.b
        r = color.r
        color.r = b
        color.b = r
    return color

def swap_blue_to_red(color):
    if color.b > color.r:
        b = color.b
        r = color.r
        color.r = b
        color.b = r
    return color

def to_black(color):
    color.r = 0
    color.g = 0
    color.b = 0
    return color

def load_colors(file, colors):
    f = open(file, 'r', encoding='utf-8')
    contents = f.read()
    xml = BeautifulSoup(contents, 'xml')
    p = Path(file)
    #file_backup = p.parent.joinpath("Backup/", p.name)
    #export_file(file_backup, contents)
    f.close()
    channels = get_color_nodes(xml)
    if channels != None:
        for rampchannel in channels:
            #print("Ramp channel: {}".format(rampchannel))
            keyframes = list(rampchannel.find_all("keyframe"))
            for k in keyframes:
                color_val = get_attribute_value(k, "value")
                if color_val != None:
                    color = Color(int32(color_val), k)
                    #print("New color: {}".format(k))
                    #color.debug_print()
                    colors.append(color)
        
        for c in colors:
            if not c.int in color_remap:
                recolor = Color(c.int)
                #recolor = swap_green_to_blue(recolor)
                #recolor = swap_red_to_purple(recolor)
                recolor = to_black(recolor)
                #recolor = swap_blue_to_red(recolor)
                color_remap[c.to_hex()] = recolor
        
        for c in colors:
            if c.to_hex() in color_remap:
                recolor = color_remap[c.to_hex()]
                c.node["value"] = str(recolor.to_int())
        
        file_path = Path(file)

        backup_dir = bacupfolder.joinpath(today)
        Path.mkdir(backup_dir, parents=True, exist_ok=True)
        export_file(backup_dir.joinpath(file_path.name), contents)

        #target = Path(file_path.with_name(file_path.stem.replace("RS3", "LLPURPLEFIRE")).with_suffix(".lsefx"))
        target = file_path
        if target.exists:
            export_dir = file_path.parent.joinpath("_Generated")
            Path.mkdir(export_dir, parents=True, exist_ok=True)
            #target = Path(export_dir.joinpath(file_path.name).with_name(file_path.stem.replace("RS3", "LLPURPLEFIRE")).with_suffix(".lsefx"))
            target = Path(export_dir.joinpath(file_path.name).with_suffix(".lsefx"))

        export_file(target.absolute(), str(xml.prettify()))

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.colors = []
        
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)
        self.wm_iconbitmap('')
 
        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
 
        self.button()

    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Build Color List",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir = startpath.absolute(), title = "Select A File", filetype =
        (("Allspark Editor Files","*.lsefx"),("all files","*.*")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)
        if self.filename != None:
            load_colors(self.filename, self.colors)
        

# c = Color(int("-8324348"))
# print("Color (-8324348) | a({}) r({}) g({}) b({}) = ({}) | ({})".format(
#   c.a, c.r, c.g, c.b, c.to_hex().upper(),
#       int32(c.to_int())))

effect_files = list(startpath.glob('*.lsefx'))
for f in effect_files:
    load_colors(f.absolute(), [])

#win = Root()
#win.mainloop()