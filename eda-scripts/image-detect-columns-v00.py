# image-detect-columns-v00.py
# detect columns in an image
import cv2
from PIL import Image
from stylish import *
import sys
import os
import argparse
import pyocr
import pyocr.builders
import pandas as pd

# build arguments
parser                              =   argparse.ArgumentParser(description='Perform an OCR on an image then detect columns')
parser.add_argument('input_file', type=str, nargs=1,help='input file', default=None)
parser.add_argument('output_file', type=str, nargs=1,help='output file')
parser.add_argument('--from_csv', type=str, default=None)
parser.add_argument('--save_csv', type=str, default=None)
args                                =   parser.parse_args()

inputFile                           =   args.input_file[0]
outputFile                          =   args.output_file[0]
lineColor                           =   (0,0,255)

# lang is english
lang                                =   'eng'

# welcome user
print (title('Image Detect Columns v00'))

# check an OCR engine is present
tools                               =   pyocr.get_available_tools()
if len(tools) == 0:
    print tab(), error("No OCR tool found")
    sys.exit(1)
tool                                =   tools[0]
print tab(), highlight("Will use tool '%s'" % (tool.get_name()))

# are we performing an OCR?
if (args.from_csv != None):
    # nope, load it from pandas
    if (os.path.exists(args.from_csv) == False):
        # file does not exist, exit
        print tab(), warning('Cannot find input file {0}'.format(args.from_csv))
        sys.exit()
    print tab(), subheader('loading word boxes from'), highlight(args.from_csv)
    df                              =   pd.read_csv(args.from_csv)
else:
    # yes, does the input file exist?
    if (os.path.exists(inputFile) == False):
        # no, exit
        print tab(), warning('Cannot find input file {0}'.format(inputDir))
        sys.exit()

    # perform the OCR
    print tab(), subheader('Performing OCR'), 'on file ', highlight(inputFile)
    wordBoxes                          =   tool.image_to_string(
        Image.open(os.path.join(inputFile)),
        lang=lang,
        builder=pyocr.builders.WordBoxBuilder()
    )
    print tab(), done()

    # load into pandas
    print tab(), subheader('Loading word boxes'), 'into pandas...'
    df                                  =   pd.DataFrame(columns=['text', 'x0', 'y0', 'x1', 'y1'])
    i                                   =   0
    for box in wordBoxes:
        df.loc[i]                       =   [
            box.content.encode('utf-8'),
            box.position[0][0],
            box.position[0][1],
            box.position[1][0],
            box.position[1][1]
        ]
        i                               +=  1
    print tab(), done()

    # save as a CSV file?
    if (args.save_csv != None):
        print tab(), subheader('Saving dataframe as CSV'), highlight(args.save_csv)
        df.to_csv(args.save_csv)
        print tab(), done()

print tab(), 'found ', highlight(len(df)), 'word boxes.'
