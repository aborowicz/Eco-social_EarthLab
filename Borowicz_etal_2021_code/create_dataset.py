# Tyler Estro - Stony Brook University 10/26/17
#
import argparse, os, piexif, sys
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='extracts image metadata and writes a csv file')
parser.add_argument('base_dir', type=str, help='base directory to recursively search for images in')
args = parser.parse_args()
if not os.path.isdir(args.base_dir):
	parser.error(args.base_dir + ' is not a directory')

# setting up the main dataframe
cols = ['Source', 'File', 'Species', 'Latitude', 'Longitude', 'Month', 'Day', 'Year']
df = pd.DataFrame(columns=cols)

# dict between absolute dirs and the name of the dir
image_dirs = {dI : os.path.join(args.base_dir,dI) for dI in os.listdir(args.base_dir) if os.path.isdir(os.path.join(args.base_dir,dI))}

# iterating over all dirs in /images dir
for dir_name, dir in image_dirs.items():
	for subdir in os.listdir(dir):
		if 'nonseal' in subdir:
			continue
		newdir = dir + '/' + subdir
		for infile in os.listdir(dir + '/' + subdir):
			latitude = np.NaN
			longitude = np.NaN
			date = np.NaN
			try:	
				exif_dict = piexif.load(newdir + '/' + infile)
				# converting lat/long to +/- degree dec format
				if all (k in exif_dict['GPS'] for k in (piexif.GPSIFD.GPSLatitude, piexif.GPSIFD.GPSLatitudeRef)):
					latitude = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]
					d = float(latitude[0][0]) / float(latitude[0][1])			
					m = float(latitude[1][0]) / float(latitude[1][1])
					s = float(latitude[2][0]) / float(latitude[2][1])
					latitude = d + (m / 60.0) + (s / 3600.0)
					if 'S' in exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] and latitude > 0:
						latitude = latitude*-1
					elif 'N' in exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] and latitude < 0 or latitude == 0:
						latitude = np.NaN
				if all (k in exif_dict['GPS'] for k in (piexif.GPSIFD.GPSLongitude, piexif.GPSIFD.GPSLongitudeRef)):
					longitude = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]
					d = float(longitude[0][0]) / float(longitude[0][1])			
					m = float(longitude[1][0]) / float(longitude[1][1])
					s = float(longitude[2][0]) / float(longitude[2][1])
					longitude = d + (m / 60.0) + (s / 3600.0)
					if 'W' in exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] and longitude > 0:
						longitude = longitude*-1
					elif 'E' in exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] and longitude < 0 or longitude == 0:
						longitude = np.NaN
				# check for DateTimeOriginal first, o.w. GPSDateStamp
				if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
					date = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].split(':')
				elif piexif.GPSIFD.GPSDateStamp in exif_dict["GPS"]:
					date = exif_dict["GPS"][piexif.GPSIFD.GPSDateStamp].split(':')
				# add a row to the dataframe if we have the necessary dataframe
				if not np.isnan(latitude) and not np.isnan(longitude) and date[0]:
					df = df.append({'Source':dir_name, 'File':infile, 'Species':subdir, 'Latitude':latitude, 
					'Longitude':longitude,'Month':date[1], 'Day':date[2].split()[0], 'Year':date[0]}, ignore_index=True)
			except:
				continue
				
				
df.to_csv('seal_dataset.csv', index=False)