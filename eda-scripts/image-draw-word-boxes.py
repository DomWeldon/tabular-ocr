# image-draw-word-boxes.py
# draw rectangles around all recognised text from all images in a directory and write to an output directory
from stylish import *
import cv2
from PIL import Image
import sys
import os
import argparse
import pyocr
import pyocr.builders

# build arguments
parser                              =   argparse.ArgumentParser(description='Perform an OCR on all images in a directory, draw rectangles around all recognized word boxes, and output these images to the output directory')
parser.add_argument('input_dir', type=str, nargs=1,help='input directory')
parser.add_argument('output_dir', type=str, nargs=1,help='output directory')
args                                =   parser.parse_args()

inputDir                            =   args.input_dir[0]
outputDir                           =   args.output_dir[0]
lineColor                           =   (0,0,255)

# lang is english
lang                                =   'eng'

# welcome user
print (title('Image Draw Word Boxes v00'))
# check that supplied arguments are valid

# 1. does the input dir exist?
if (os.path.isdir(inputDir) == False):
    # no, exit
    print tab(), warning('Cannot find input directory {0}'.format(inputDir))
    sys.exit()
totalInputFiles                     =   len(os.listdir(inputDir))

# does the output directory exist?
if (os.path.isdir(outputDir) == False):
    # no, make it
    os.mkdir(outputDir)

# inform user
print tab(), 'will open ', highlight(totalInputFiles), 'files from ', highlight(inputDir)

# find tesseract
tools                               =   pyocr.get_available_tools()
if len(tools) == 0:
    print tab(), error("No OCR tool found")
    sys.exit(1)
tool                                =   tools[0]
print tab(), highlight("Will use tool '%s'" % (tool.get_name()))

# perform action for all images
for filename in os.listdir(inputDir):
    print tab(2), subheader('opening image'), highlight(filename)
    print tab(3), 'performing OCR...'
    # get all wordboxes
    wordBoxes                       =   tool.image_to_string(
        Image.open(os.path.join(inputDir, filename)),
        lang=lang,
        builder=pyocr.builders.WordBoxBuilder()
    )
    print tab(3), done()
    print tab(3), 'found ', highlight(len(wordBoxes)), 'word boxes'

    # open the image in CV2
    print tab(3), 'opening image to create drawing'
    img                             =   cv2.imread(os.path.join(inputDir, filename))
    print tab(3), done()

    # draw the rectangles
    print tab(3), 'drawing ', highlight(len(wordBoxes)), 'rectangles'
    for box in wordBoxes:
        # position is originally: ((width_pt_x, height_pt_x), (width_pt_y, height_pt_y))
        cv2.rectangle(img, box.position[0], box.position[1], lineColor, thickness=3, lineType=8, shift=0)
    print tab(3), done()

    # save the file
    print tab(3), 'saving as', highlight(os.path.join(outputDir, filename))
    cv2.imwrite(os.path.join(outputDir, '{0}.png'.format(filename)), img)
    print tab(3), done()

# end of script
print title('Fin.')
