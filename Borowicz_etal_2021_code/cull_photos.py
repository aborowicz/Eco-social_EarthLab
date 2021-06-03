#### Alex Borowicz - Stony Brook University 2 Mar 2019
#### After collecting photos with a crawler like icrawl, and after creating a dataset with
#### create_dataset_wtags.py, we need to get rid of images that came in without any useful metadata
#### Currently, create_dataset_wtags.py writes 'NA' in the date field for images that have no meta
#### and no other process does that, so all images with NA in one of those fields is trash.
#### We want to read the data csv, and for each empty image, remove it from its directory.


#
import argparse, os, sys, csv
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='extracts image metadata and writes a csv file')
parser.add_argument('base_dir', type=str, help='base directory to recursively search for images in')
args = parser.parse_args()
if not os.path.isdir(args.base_dir):
	parser.error(args.base_dir + ' is not a directory')

