from PIL import Image,ImageOps
import random
from pathlib import Path
import os
import argparse
import timeit

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir.resolve())

# Example usage:
# python dos2de_create_masked_icons.py -i "./IconMasking_Test/icons" -m "./IconMasking_Test/masks" -o "./IconMasking_Test/output"
# python dos2de_create_masked_icons.py -i "./IconMasking_Test/icons" -m "./IconMasking_Test/masks" -o "./IconMasking_Test/output" --no-random

parser = argparse.ArgumentParser(description='Mask all images in a folder with a given set of mask files.')
parser.add_argument("-i", "--icons", type=Path, required=True, help='The directory of icons to process')
parser.add_argument("-m", "--masks", type=Path, required=True, help='The directory of mask images to use.')
parser.add_argument("-o", "--output", type=Path, required=True, help='The directory to copy results to.')
parser.add_argument("-r", "--random", action=argparse.BooleanOptionalAction, default=True, help='Randomly rotate the mask in 90 degree increments, or flip it.')
args = parser.parse_args()

icons_dir:Path = args.icons
masks_dir:Path = args.masks
output_dir:Path = args.output
do_random:bool = args.random

image_types = [".png", ".jpg", ".jpeg", ".bmp"]
rotations = [90,180,270]

def run():
    if icons_dir.is_dir() and masks_dir.is_dir() and output_dir.is_dir():
        output_dir.mkdir(exist_ok=True, parents=True)
        
        masks = [Image.open(p).convert("L") for p in masks_dir.rglob("*.png")]
        icons = [(p, Image.open(p).convert("RGBA")) for p in icons_dir.rglob("**/*") if p.suffix in image_types]
        
        def get_random_mask()->Image.Image:
            return random.choice(masks)
        
        for p,icon in icons:
            if icon.size[0] > 64 or icon.size[1] > 64:
                icon = icon.resize((64,64), resample=Image.BILINEAR)
            output_path = output_dir.joinpath(p.name).with_suffix(".png")
            mask = get_random_mask()
            if do_random:
                mask = mask.copy()
                mask.rotate(random.choice(rotations) * random.choice([-1,1]))
                match random.choice([1,2,3]):
                    case 1:
                        pass
                    case 2:
                        mask = ImageOps.flip(mask)
                    case 3:
                        mask = ImageOps.mirror(mask)
            icon.putalpha(mask)
            icon.save(output_path)

print("Masked icons in {} seconds.".format(timeit.timeit(run, number=1)))