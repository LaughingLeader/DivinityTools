from bs4 import BeautifulSoup
from PIL import Image
import os
import sys

import uuid

import subprocess

import pathlib
from pathlib import Path

import numpy

import time
start_time = time.time()

atlas_template = """
<?xml version="1.0" encoding="UTF-8" ?>
<save>
    <header version="2" />
    <version major="3" minor="6" revision="6" build="0" />
    <region id="IconUVList">
        <node id="root">
            <children>{icons}
            </children>
        </node>
    </region>
    <region id="TextureAtlasInfo">
        <node id="root">
            <children>
                <node id="TextureAtlasIconSize">
                    <attribute id="Height" value="{icon_w}" type="4" />
                    <attribute id="Width" value="{icon_h}" type="4" />
                </node>
                <node id="TextureAtlasPath">
                    <attribute id="Path" value="{texture_path}" type="20" />
                    <attribute id="UUID" value="{texture_uuid}" type="22" />
                </node>
                <node id="TextureAtlasTextureSize">
                    <attribute id="Height" value="{texture_width}" type="4" />
                    <attribute id="Width" value="{texture_height}" type="4" />
                </node>
            </children>
        </node>
    </region>
</save>
"""

class Rect():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Icon():
    def __init__(self, image_path, x,y,u1,v1,u2,v2):
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGBA")
        self.name = Path(image_path).stem
        self.pos = (x,y)
        self.uv = Rect(u1,v1,u2,v2)
    
    def to_xml(self):
        return """
                <node id="IconUV">
                    <attribute id="MapKey" value="{name}" type="22" />
                    <attribute id="U1" value="{u1}" type="6" />
                    <attribute id="U2" value="{u2}" type="6" />
                    <attribute id="V1" value="{v1}" type="6" />
                    <attribute id="V2" value="{v2}" type="6" />
                </node>""".format(
                    name = self.name,
                    u1 = self.uv.x,
                    v1 = self.uv.y,
                    u2 = self.uv.w,
                    v2 = self.uv.h
                )

def get_images(directory):
    dir_path = pathlib.Path(directory)
    files = dir_path.glob("*.png")
    return list(files)

import math
def truncate(number, digits, round_num = True) -> float:
    stepper = 10.0 ** digits
    if round_num:
        return round(math.trunc(stepper * number) / stepper, digits - 1)
    else:
        return math.trunc(stepper * number) / stepper

def get_arg(arg, fallback):
    if len(sys.argv) > arg:
        val = sys.argv[arg]
        if val != None:
            return val
    return fallback

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

images_dir = get_arg(1, script_dir.joinpath("icons"))
atlas_output = get_arg(2, script_dir.joinpath("AllIcons_Merged.lsx"))
texture_output = get_arg(3, script_dir.joinpath("AllIcons_Merged.png"))
atlas_uuid = get_arg(4, str(uuid.uuid4()))
texture_dds_output = get_arg(5, "")
if texture_dds_output == "":
    texture_dds_output = Path(texture_output).with_suffix(".dds")
else:
    # Ensure ext
    texture_dds_output = Path(texture_dds_output).with_suffix(".dds")

texture_name = Path(texture_output).stem
texture_xml_output = "Assets/Textures/Icons/{}.dds".format(texture_name)

atlas_size = 4096
icon_size = 64

images = get_images(images_dir)
print("Merging {} images.".format(len(images)))

icons = []

padding = float(0.5/atlas_size)
col_max = atlas_size / icon_size
row_max = atlas_size / icon_size

x = 0
y = 0

# For some reason, the editor appends the first two icons to the end
icons_first = []

for img in images:
    # u1 = truncate(float(((icon_size * x) / atlas_size) + padding), 9)
    # v1 = truncate(float(((icon_size * y) / atlas_size) + padding), 9)
    # u2 = truncate(float(((icon_size * (x + 1)) / atlas_size) - padding), 9)
    # v2 = truncate(float(((icon_size * (y + 1)) / atlas_size) - padding), 9)
    round_num = True
    truncate_u1 = 7
    truncate_v1 = 8
    truncate_u2 = 7
    truncate_v2 = 7

    if x <= 1 and y == 0: 
        u1 = truncate(numpy.clip(float(((icon_size * x) / atlas_size) + padding), 0, 1.0), 9, round_num=True)
        v1 = truncate(numpy.clip(float(((icon_size * y) / atlas_size) + padding), 0, 1.0), 9, round_num=False)
        u2 = truncate(numpy.clip(float(((icon_size * (x + 1)) / atlas_size) - padding), 0, 1.0), 7, round_num=False)
        v2 = truncate(numpy.clip(float(((icon_size * (y + 1)) / atlas_size) - padding), 0, 1.0), 7, round_num=False)
    else:
        u1 = truncate(numpy.clip(float(((icon_size * x) / atlas_size) + padding), 0, 1.0), truncate_u1, round_num)
        v1 = truncate(numpy.clip(float(((icon_size * y) / atlas_size) + padding), 0, 1.0), truncate_v1, round_num)
        u2 = truncate(numpy.clip(float(((icon_size * (x + 1)) / atlas_size) - padding), 0, 1.0), truncate_u2, round_num)
        v2 = truncate(numpy.clip(float(((icon_size * (y + 1)) / atlas_size) - padding), 0, 1.0), truncate_v2, round_num)

    icon = Icon(
        img.resolve(),
        x * icon_size, #math.floor(atlas_size * u1),
        y * icon_size, #math.floor(atlas_size * v1),
        u1,v1,u2,v2)

    if x <= 1 and y == 0:
        icons_first.append(icon)
    else:
        icons.append(icon)
    print("** Added icon '{}'.".format(icon.name))
    x += 1
    if(x >= col_max):
        y += 1
        x = 0
    if (y > row_max):
        print("[ERROR] Hit the max atlas size!")
        break

icons.extend(icons_first)
total = len(icons)

def create_atlas_output(icons_str, icon_w, icon_h, 
        texture_path, uuid, texture_width, texture_height):
    return atlas_template.format(
        icons = icons_str,
        icon_w = icon_w,
        icon_h = icon_h,
        texture_path = texture_path,
        texture_uuid = uuid,
        texture_width = texture_width,
        texture_height = texture_height
    )

icons_str = ""
for icon in icons:
    icons_str += icon.to_xml()

xml_str = create_atlas_output(icons_str, icon_size, icon_size, 
    texture_xml_output, atlas_uuid, atlas_size, atlas_size)

print("Saving atlas to '{}'.".format(atlas_output))

f = open(atlas_output, "w")
f.write(xml_str)

texture_image = Image.new('RGBA', (atlas_size, atlas_size), (0, 0, 0, 0))

for icon in icons:
    print("** Pasting '{}'.".format(icon.name))
    #texture_image.paste(icon.image, icon.pos, mask=0)
    texture_image.alpha_composite(icon.image, icon.pos)

print("Saving texture to '{}'.".format(texture_output))

texture_image.save(texture_output)

print("Done. Took **{} seconds** to merge {} icons.".format(time.time() - start_time, total))

#convert_params = 'nvcompress -alpha -bc3 "{}" "{}"'.format(texture_output, texture_dds_output)

# p = subprocess.run([convert_params],
#   shell=True,
#   universal_newlines=True, 
#   stdout=subprocess.PIPE, 
#   stderr=subprocess.PIPE)

p = subprocess.run(["nvcompress", 
    "-alpha", 
    "-bc3", 
    str(texture_output), 
    str(texture_dds_output),
    "-srgb"
    ], 
    universal_newlines=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE)
print(p.stdout)
print(p.stderr)