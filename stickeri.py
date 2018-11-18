import os
import re
import path
import argparse
import numpy as np
from tqdm import tqdm
from skimage.transform import resize
from skimage.io import imread, imsave

def pic2stick(img):
    s = img.shape
    img = np.concatenate([img, np.zeros((shp[0], shp[1], 1))+1], 2) if s[2] == 3 else img
    to512, other = (1,0) if s[0] >= s[1] else (0,1)
    howlarge = s[to512]/s[other]
    new = int(np.ceil(512*howlarge))
    new_s = (512, new, s[2]) if to512 == 0 else (new, 512, s[2])
    img = resize(img, new_s, mode="reflect")
    return(img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Stickeripy a bunch of pictures to suitable for Telegram sticker format"
    )
    parser.add_argument(
        "folder", 
        metavar="Folder",
        help="Folder with pictures"
    )
    parser.add_argument(
        "output",
        metavar="Output",
        help="Output folder"
    )
    args = parser.parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    for a in tqdm([b for b in os.walk(args.folder)][0][2]):
        new_fn = re.sub(
            ".[a-zA-Z]+$", ".png", 
            os.path.join(
                args.output, os.path.split(a)[-1]
            )
        )
        imsave(new_fn, pic2stick(imread(os.path.join(args.folder, a))))