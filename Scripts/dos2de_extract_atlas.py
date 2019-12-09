from bs4 import BeautifulSoup
from PIL import Image
import os
from pathlib import Path

class Atlas():
	def __init__(self, name, texture_name, width=2048, height=2048, iconw=64, iconh=64):
		self.name = name
		self.icons = []
		self.texture_name = texture_name
		self.image_width = int(width)
		self.image_height = int(height)
		self.icon_width = int(iconw)
		self.icon_height = int(iconh)
		self.icon_offset = float(0.5/self.image_width)

class Icon():
	def __init__(self, atlas, name, u1, v1, u2, v2):
		self.name = name
		self.u1 = float(u1)
		self.v1 = float(v1)
		self.u2 = float(u2)
		self.v2 = float(v2)
		self.rect = (
			int(atlas.image_width * (self.u1 - atlas.icon_offset)), 
			int(atlas.image_height * (self.v1 - atlas.icon_offset)), 
			int(atlas.image_width * (self.u2 + atlas.icon_offset)),
			int(atlas.image_height * (self.v2 + atlas.icon_offset))
		)


script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
icons_output_dir = script_dir.joinpath("_Icons_Extracted").resolve()
os.chdir(script_dir.resolve())

atlases_dir = "G:/Divinity Original Sin 2/DefEd/Data/Public/HumanSebille_59f1d870-bdc6-45cb-a8fc-26a1b6afde33/GUI/"
#atlases_dir = "D:/Modding/DOS2DE_Extracted/_ExtractedPaks/Public/Shared/GUI"
#atlases_dir = "C:/Modding/Tools/_GUI"
#textures_dir = "D:/Modding/DOS2DE_Extracted/_ExtractedPaks/Public/Shared/Assets/Textures/Icons"
textures_dir = "G:/Divinity Original Sin 2/DefEd/Data/Public/HumanSebille_59f1d870-bdc6-45cb-a8fc-26a1b6afde33/Assets/Textures/Icons/"

atlas_files = []
texture_files = []

for file in os.listdir(atlases_dir):
    if file.endswith(".lsx"):
        atlas_files.append((file, os.path.join(atlases_dir, file)))

for file in os.listdir(textures_dir):
    if file.endswith(".dds"):
        texture_files.append((file, os.path.join(textures_dir, file)))

#atlas_path = os.path.join(script_dir, "Ability_Skill_Status_Icons.lsx")
#texture_path =  os.path.join(script_dir, "Ability_Skill_Status_Icons.dds")

for atlasname, atlas_path in atlas_files:
	atlas_xml = None
	f = open(atlas_path, 'r')
	atlas_xml = BeautifulSoup(f.read(), 'lxml')
	f.close()

	atlas_name = Path(atlas_path).stem

	atlas_texturesize = atlas_xml.find("node", attrs={"id":"TextureAtlasTextureSize"})
	atlas_sizew = atlas_texturesize.find("attribute", {"id":"Width"})["value"]
	atlas_sizeh = atlas_texturesize.find("attribute", {"id":"Height"})["value"]

	atlas_texturepathnode = atlas_xml.find("node", attrs={"id":"TextureAtlasPath"})
	atlas_texturepath = atlas_texturepathnode.find("attribute", {"id":"Path"})["value"]
	atlas_texture = os.path.basename(atlas_texturepath)

	atlas_iconsize =  atlas_xml.find("node", {"id":"TextureAtlasIconSize"})
	atlas_iconw = atlas_iconsize.find("attribute", {"id":"Width"})["value"]
	atlas_iconh = atlas_iconsize.find("attribute", {"id":"Height"})["value"]

	atlas = Atlas(atlas_name, atlas_texture, atlas_sizew, atlas_sizeh, atlas_iconw, atlas_iconh)

	texture_path = os.path.join(textures_dir, atlas.texture_name)
	if os.path.exists(texture_path):
		for icon_node in atlas_xml.find_all("node", {"id":"IconUV"}):
			mapkey = icon_node.find("attribute", {"id":"MapKey"})["value"]
			u1 = icon_node.find("attribute", {"id":"U1"})["value"]
			v1 = icon_node.find("attribute", {"id":"V1"})["value"]
			u2 = icon_node.find("attribute", {"id":"U2"})["value"]
			v2 = icon_node.find("attribute", {"id":"V2"})["value"]
			icon = Icon(atlas, mapkey, u1, v1, u2, v2)
			atlas.icons.append(icon)

		output_dir = os.path.join(icons_output_dir, atlas.name)
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)

		print("Opening texture: {}".format(texture_path))
		img = Image.open(texture_path)
		for icon in atlas.icons:
			img_crop = img.crop(icon.rect)
			result_image = Image.new('RGBA', (atlas.icon_width, atlas.icon_height), (0, 0, 0, 0))
			result_image.paste(img_crop, (0,0), mask=0)
			filename = os.path.join(output_dir, icon.name + ".png")
			print("Writing icon to: {}".format(filename))
			result_image.save(filename)
	else:
		print("Texture '{}' does not exist!".format(texture_path))