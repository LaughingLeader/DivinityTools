from dataclasses import dataclass, field
from io import BufferedReader
from PIL import Image
import numpy
import lxml.etree as ET
from pathlib import Path
import os

@dataclass
class Icon:
    name:str = ""
    u1:float = 0
    u2:float = 0
    v1:float = 0
    v2:float = 0
    rect:tuple[4] = field(default_factory=lambda:(0,0,0,0))
    
    def update_rect(self, atlas:"Atlas")->tuple[4]:
        self.rect = (
            numpy.floor(atlas.tex_width * (self.u1)), 
            numpy.floor(atlas.tex_height * (self.v1)), 
            numpy.ceil(atlas.tex_width * (self.u2 - atlas.icon_offset)),
            numpy.ceil(atlas.tex_height * (self.v2 - atlas.icon_offset))
        )

@dataclass
class Atlas:
    name:str = ""
    icons:list["Icon"] = field(default_factory=lambda:[])
    texture_path:str = ""
    uuid:str = ""
    tex_width:int = 2048
    tex_height:int = 2048
    icon_width:int = 64
    icon_height:int = 64
    
    @property
    def icon_offset(self)->float:
        return float(0.5/self.tex_width)
    
    def __str__(self) -> str:
        return f"Atlas{{name({self.name}) texture_path({self.texture_path}) texture_size({self.tex_width},{self.tex_height}) icon_size({self.icon_width},{self.icon_height})}}"
    
    def parse(self, f:BufferedReader):
        elem:ET._Element
        for _,elem in ET.iterparse(f):
            if elem.tag == "node":
                node_id = elem.get("id")
                match(node_id):
                    case "TextureAtlasTextureSize":       
                        for id,value in [(x.get("id"), x.get("value")) for x in elem.iterdescendants()]:
                            if id == "Height":
                                self.tex_height = int(value)
                            elif id == "Width":
                                self.tex_width = int(value)
                    case "TextureAtlasIconSize":       
                        for id,value in [(x.get("id"), x.get("value")) for x in elem.iterdescendants()]:
                            if id == "Height":
                                atlas.icon_width = int(value)
                            elif id == "Width":
                                atlas.icon_height = int(value)
                    case "TextureAtlasPath":       
                        for id,value in [(x.get("id"), x.get("value")) for x in elem.iterdescendants()]:
                            if id == "Path":
                                self.texture_path = value
                            elif id == "UUID":
                                self.uuid = value
                    case "IconUV":       
                        icon = Icon()
                        for id,value in [(x.get("id"), x.get("value")) for x in elem.iterdescendants()]:
                            match(id):
                                case "MapKey":
                                    icon.name = value
                                case "U1":
                                    icon.u1 = float(value)
                                case "U2":
                                    icon.u2 = float(value)
                                case "V1":
                                    icon.v1 = float(value)
                                case "V2":
                                    icon.v2 = float(value)
                        if icon.name != "":
                            icon.update_rect(self)
                            self.icons.append(icon)

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
icons_output_dir = script_dir.joinpath("_Icons_Extracted").resolve()
os.chdir(script_dir.resolve())

atlases_dir = Path("D:/Modding/DOS2DE_Extracted/Public/Shared/GUI")
textures_dir = Path("D:/Modding/DOS2DE_Extracted/Public/Shared")

atlas_files:list[Path] = []

for file in atlases_dir.iterdir():
    if file.suffix == ".lsx":
        atlas_files.append(file)

#atlas_path = os.path.join(script_dir, "Ability_Skill_Status_Icons.lsx")
#texture_path =  os.path.join(script_dir, "Ability_Skill_Status_Icons.dds")

for atlas_path in atlas_files:
    atlas_xml = None
    with atlas_path.open("rb") as f:
        atlas_name = atlas_path.stem
        atlas = Atlas(atlas_name)
        atlas.parse(f)
        output_dir = icons_output_dir.joinpath(atlas.name)
        #output_dir.mkdir(parents=True, exist_ok=True)

        texture_path = textures_dir.joinpath(atlas.texture_path)
        if texture_path.exists() and texture_path.stem == "talentsAndAbilities":
            print(atlas)
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"Opening texture: {texture_path}")
            with Image.open(texture_path).convert('RGBA') as img:
                for icon in atlas.icons:
                    #print(icon)
                    img_crop = img.crop(icon.rect)
                    result_image = Image.new('RGBA', (atlas.icon_width, atlas.icon_height), (0, 0, 0, 0))
                    #result_image.paste(img_crop, (0,0), mask=0)
                    result_image.alpha_composite(img_crop, (0,0))
                    filename = output_dir.joinpath(icon.name).with_suffix(".png")
                    #print("Writing icon to: {}".format(filename))
                    # if filename.exists() == True:
                    #     filename = output_dir.joinpath(icon.name + "(01)").with_suffix(".png")
                    result_image.save(filename)
        else:
            print(f"Texture '{texture_path}' does not exist!")

print("Done!")