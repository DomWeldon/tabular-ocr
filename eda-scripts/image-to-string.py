# test OCR capabilities
from stylish import *
import cv2
from PIL import Image
import sys
import argparse
import pyocr
import pyocr.builders

# build arguments
parser                              =   argparse.ArgumentParser(description='Convert an image to a string')
parser.add_argument('filename', type=str, nargs=1,help='image filename')
args                                =   parser.parse_args()

# welcome user
print (title('Image to String v00'))
print (tab() + 'will open ' + highlight(args.filename))

# find tesseract
tools                               =   pyocr.get_available_tools()
if len(tools) == 0:
    print(tab() + error("No OCR tool found"))
    sys.exit(1)
tool                                =   tools[0]
print(tab() + highlight("Will use tool '%s'" % (tool.get_name())))

# lang is english
lang                                =   'eng'

# test out one of our images
ocrText                             =   tool.image_to_string(
    Image.open(args.filename[0]),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)

print ocrText
