# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:55:10 2018

@author: SMITH
"""

from PIL import Image
import os
import json

CAPTCHA_DIM = (180, 45)
CHARACTER_DIM = (30, 32)
FPATH = os.path.dirname(os.path.realpath(__file__))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print("base: "+base_path)
    except Exception:
        base_path = os.path.abspath(".")
    print("bitmaps: "+base_path)
    return os.path.join(base_path, relative_path)


def parse_captcha(img,bitmapPath):

    captcha = ""

    img_width = CAPTCHA_DIM[0]
    img_height = CAPTCHA_DIM[1]

    char_width = CHARACTER_DIM[0]
    char_height = CHARACTER_DIM[1]

    char_crop_threshold = {'upper': 12, 'lower': 44}

    img_matrix = img.convert('L').load()

    #bitmaps_fpath = os.path.join(FPATH, "bitmaps.json")
    #bitmaps_fpath = resource_path("bitmaps.json")

    bitmaps = json.load(bitmapPath)
    

    # remove single pixel width noise + thresholding
    for y in range(1, img_height - 1):
        for x in range(1, img_width - 1):
            if img_matrix[x, y-1] == 255 and img_matrix[x, y] == 0 and img_matrix[x, y+1] == 255:
                img_matrix[x, y] = 255
            if img_matrix[x-1, y] == 255 and img_matrix[x, y] == 0 and img_matrix[x+1, y] == 255:
                img_matrix[x, y] = 255
            if img_matrix[x, y] != 255 and img_matrix[x, y] != 0:
                img_matrix[x, y] = 255

    # loop through individual characters
    for i in range(char_width, img_width + 1, char_width):

        # crop with left, top, right, bottom coordinates
        img_char_matrix = img.crop(
            (i-char_width, char_crop_threshold['upper'], i, char_crop_threshold['lower'])).convert('L').load()

        matches = {}

        for character in bitmaps:
            match_count = 0
            black_count = 0

            lib_char_matrix = bitmaps[character]

            for y in range(0, char_height):
                for x in range(0, char_width):
                    if img_char_matrix[x, y] == lib_char_matrix[y][x] and lib_char_matrix[y][x] == 0:
                        match_count += 1
                    if lib_char_matrix[y][x] == 0:
                        black_count += 1

            perc = float(match_count)/float(black_count)
            matches.update({perc: character[0].upper()})

        try:
            captcha += matches[max(matches.keys())]
        except ValueError:
            captcha += "0"

    return captcha


#if __name__ == '__main__':
 #   img = Image.open(os.path.join(FPATH, "test.png"))
 #  print(parse_captcha(img))
