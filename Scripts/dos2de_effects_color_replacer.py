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

startpath = Path('G:/Divinity Original Sin 2/DefEd/Data/Editor/Mods/ZZZ_GreenNecroFire_0bc91e73-ce14-4d3f-934c-3024a8ba348d/Assets/Effects')
color_prop_id = {}
#color_prop_id['particles'] = '93b34a52-eef2-4f88-80f6-19e3126188ca'
color_prop_id['light'] = '16caf8e6-d471-43da-b704-c845b1437927'
color_prop_id['ribbon'] = '5e5355ff-1c5f-48dd-888e-0129e288f8b6'

def get_attribute_value(node, attribute_name):
    try:
        att = node[attribute_name]
        return str(att)
    except: pass
    return None

def get_color_nodes(xml):
    nodes = []
    for k,prop in color_prop_id.items():
        n = xml.find_all("rampchannel", {"id":prop})
        if n != None:
            nodes.extend(n)
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

def load_colors(file, colors):
    f = open(file, 'r', encoding='utf-8')
    contents = f.read()
    xml = BeautifulSoup(contents, 'xml')
    p = Path(file)
    file_backup = p.parent.joinpath("Backup/", p.name)
    export_file(file_backup, contents)
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
                    color.debug_print()
                    colors.append(color)
        
        for c in colors:
            if not c.int in color_remap:
                recolor = Color(c.int)
                if recolor.r > recolor.g:
                    g = recolor.g
                    r = recolor.r
                    recolor.r = g
                    recolor.g = r
                color_remap[c.to_hex()] = recolor
        
        for c in colors:
            if c.to_hex() in color_remap:
                recolor = color_remap[c.to_hex()]
                c.node["value"] = str(recolor.to_int())
        
        file_path = Path(file)
        export_dir = file_path.parent.joinpath("_Generated")
        Path.mkdir(export_dir, parents=True, exist_ok=True)

        target = export_dir.joinpath(file_path.name).with_name(file_path.stem.replace("RS3", "LLGREENFLAME")).with_suffix(".lsefx")
        export_file(target, str(xml.prettify()))

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

win = Root()
win.mainloop()