# import the necessary packages
import os
import argparse
import re

# construct the argument parser and
# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--directory', required=True,
    help='path to the directory which contains the data to rename')
args = vars(ap.parse_args())


for _, _, files in os.walk(args['directory']):
    for counter, filename in enumerate(files, 1):
        new_name = '{}.jpg'.format(counter)
        old_file_path = os.path.join(args['directory'], filename)
        new_file_path = os.path.join(args['directory'], new_name)
        os.rename(old_file_path, new_file_path)