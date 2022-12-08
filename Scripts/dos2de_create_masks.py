from dataclasses import dataclass, field
from PIL import Image
import numpy as np
from pathlib import Path
import os
import argparse

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir.resolve())

# python dos2de_create_masks.py -i "./IconMasking_Test/create_masks_input" -o "./IconMasking_Test/create_masks_output"

parser = argparse.ArgumentParser(description='Turn icons into greyscale images, where the transparency is black.')
parser.add_argument("-i", "--input", type=Path, required=True, help='The directory of icons to process')
parser.add_argument("-o", "--output", type=Path, required=True, help='The directory to copy results to.')
args = parser.parse_args()

input_dir:Path = args.input
output_dir:Path = args.output

if input_dir.is_dir() and output_dir.is_dir():
    output_dir.mkdir(exist_ok=True, parents=True)
    
    icons = [(p, Image.open(p).convert("RGBA")) for p in input_dir.rglob("*.png")]
    
    black_bg = Image.new('RGBA', (64,64), "BLACK")
    
    for p,icon in icons:
        output_path = output_dir.joinpath(p.name)
        data = np.array(icon)   # "data" is a height x width x 4 numpy array
        red,green,blue,alpha = data.T # Temporarily unpack the bands for readability
        color_areas = (red > 0) | (green > 0) | (blue > 0)
        data[..., :-1][color_areas.T] = (255, 255, 255) # Transpose back needed
        #transparent_areas = alpha > 0
        #data[..., :-1][transparent_areas.T] = (0, 0, 0) # Transpose back needed
        converted_icon = Image.fromarray(data)
        mask = black_bg.copy()
        mask.paste(converted_icon, (0,0), converted_icon)
        mask.save(output_path)
        #result_icon = Image.composite(icon, transparent_image, mask)
        #result_icon = Image.alpha_composite(icon, mask)