# TODO last image is not getting renamed properly

# import the necessary packages
import argparse
import os
from PIL import Image

# construct the argument parser and
# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--directory', required=True,
    help='path to the directory which contains the data to rename')
args = vars(ap.parse_args())

counter = 1
num_files = len([f for f in os.listdir(args['directory'])]) + 1
max_image_number = 0

# iterate over the data directory and find the filename with
# the largest number
for _, _, files in os.walk(args['directory']):
    for filename in files:
        split = filename.split('.')[0]
        int_split = int(split)
        if max_image_number < int_split:
            max_image_number = int_split
print('[INFO] The maximum image index found was {}'.format(max_image_number))

# ensure that the files are concourrently named
while counter < num_files:
    current_file = os.path.join(args['directory'], '{}.jpg'.format(counter))
    if not os.path.exists(current_file):
        next_number = counter + 1
        print('[INFO] File {}.jpg does not exist'.format(counter))
        print('[INFO] Searching for next file to rename...')
        next_file = os.path.join(args['directory'], '{}.jpg'.format(next_number))
        if os.path.exists(next_file):
            print('[INFO] Found file {}.jpg, rename it to {}.jpg'.format(next_number, counter))
            os.rename(next_file, current_file)
        else:
            next_number += 1
            while next_number < max_image_number:
                next_file = os.path.join(args['directory'], '{}.jpg'.format(next_number))
                if os.path.exists(next_file):
                    print('[INFO] Found file {}.jpg, rename it to {}.jpg'.format(next_number, counter))
                    os.rename(next_file, current_file)
                    break
                else:
                    next_number += 1
    counter += 1

""" # Try converting all images in the given directory to the rgb
# style, especially if there exists an alpha channel in the image
# TODO: automatically walk over all subdirectories
for _, _, files in os.walk(args['directory']):
    im = Image.open(files)
    rgb_im = im.convert('RGB')
    rgb_im.save(files) """