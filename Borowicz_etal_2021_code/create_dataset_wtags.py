# Tyler Estro - Stony Brook University 10/26/17
#
import argparse, os, piexif, sys
import pandas as pd
import numpy as np
from iptcinfo3 import IPTCInfo
from datetime import datetime

parser = argparse.ArgumentParser(description='extracts image metadata and writes a csv file')
parser.add_argument('base_dir', type=str, help='base directory to recursively search for images in')
args = parser.parse_args()
if not os.path.isdir(args.base_dir):
	parser.error(args.base_dir + ' is not a directory')

# setting up the main dataframe
cols = ['Source', 'File', 'Species', 'Latitude', 'Longitude', 'Month', 'Day', 'Year', 'Title', 'Comment', 'Caption', 'Keywords']
df = pd.DataFrame(columns=cols)

# dict between absolute dirs and the name of the dir
###
#base_dir="C:/Users/Alex/Google Drive/Repos/soc_med_seals/nn_images"
#base_dir="C:\\Users\\Alex\\Downloads\\temp"
image_dirs = {dI : os.path.join(args.base_dir,dI) for dI in os.listdir(args.base_dir) if os.path.isdir(os.path.join(args.base_dir,dI))}
#image_dirs = {dI : os.path.join(base_dir,dI) for dI in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir,dI))}

# iterating over all dirs in /images dir
for dir_name, dir in image_dirs.items():
	for subdir in os.listdir(dir):
		if 'NonSeal' in subdir:
			continue
		newdir = dir + '/' + subdir
		for infile in os.listdir(dir + '/' + subdir):
                  #make empty objects 
			latitudes = np.NaN
			longitude = np.NaN
			date = np.NaN
			title = np.NAN
			comments = np.NAN
			keywords = np.NAN

			try:	
				exif_dict = piexif.load(newdir + '/' + infile)
				print(newdir)
				# converting lat/long to +/- degree dec format
				#print(exif_dict['GPS'])
				#print(exif_dict['GPS'][piexif.GPSIFD.GPSLatitude])
				if all (k in exif_dict['GPS'] for k in (piexif.GPSIFD.GPSLatitude, piexif.GPSIFD.GPSLatitudeRef)):
					latitudes = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]
					#print('true')
					d = float(latitudes[0][0]) / float(latitudes[0][1])			
					m = float(latitudes[1][0]) / float(latitudes[1][1])
					s = float(latitudes[2][0]) / float(latitudes[2][1])
					latitudes = d + (m / 60.0) + (s / 3600.0)
					#print('in',latitudes)
					#print(exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef])
					if b'S' in exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] and latitudes > 0:
						latitudes = latitudes*-1
						#print('true')
					else: latitudes=latitudes
					#elif b'N' in exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] and latitudes < 0 or latitudes == 0:
						#latitudes = np.NaN
					#print('out',latitudes)
						#print(latitudes)
				#print('mid',latitudes)
				if all (k in exif_dict['GPS'] for k in (piexif.GPSIFD.GPSLongitude, piexif.GPSIFD.GPSLongitudeRef)):
					longitude = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]
					#print(exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef])
					d = float(longitude[0][0]) / float(longitude[0][1])			
					m = float(longitude[1][0]) / float(longitude[1][1])
					s = float(longitude[2][0]) / float(longitude[2][1])
					longitude = d + (m / 60.0) + (s / 3600.0)
					if b'W' in exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] and longitude > 0:
						longitude = longitude*-1
					else: longitude=longitude
					#elif b'E' in exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] and longitude < 0 or longitude == 0:
						#longitude = np.NaN
				# check for DateTimeOriginal first, o.w. GPSDateStamp
				date = ''
				if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
					date = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]#.split(':')
				elif piexif.GPSIFD.GPSDateStamp in exif_dict["GPS"]:
					date = exif_dict["GPS"][piexif.GPSIFD.GPSDateStamp]#.split(':')
				elif piexif.EXIFIFD.DateTimeDigitized in exif_dict["Exif"]:
					date = exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized]#.split(':')
				
				# Pull out any text tags or other text 
				if piexif.ImageIFD.ImageDescription in exif_dict["0th"]:
					title = exif_dict["0th"][piexif.ImageIFD.ImageDescription].decode('utf-8')
					#print('true description')
				
				## User keywords or tags are not exif, but are file properties stored as iptc
				info = IPTCInfo(newdir + '/' + infile)
				if not info:
					keywords = 'X'
					comments = 'X'
				#print(infile)
				#print(info)
				#print(type(info))
					
				if not info['keywords']:
					keywords = 'X'
				else:
					keywords = info['keywords']
					#type(keywords)
					#print(info['keywords'])
				#print(keywords)
				if info['caption/abstract'] != ['']:
					comments = info['caption/abstract']
				else:
					comments = " "
				
				# add a row to the dataframe if we have the necessary dataframe
				#if not np.isnan(latitude) and not np.isnan(longitude) and date[0]:
					#df = df.append({'Source':dir_name, 'File':infile, 'Species':subdir, 'Latitude':latitude, 
					#'Longitude':longitude,'Month':date[1], 'Day':date[2].split()[0], 'Year':date[0]}, ignore_index=True)
				#print('end',latitudes)
				#if not np.isnan(latitudes) : 
					#print(latitudes)
				date = date.decode('utf-8')[0:10].split(':') #Decode from bytes
				#print(date, 'end')
				df = df.append({'Source':dir_name, 'File':infile, 'Species':subdir, 'Latitude':latitudes, 
					'Longitude':longitude,'Month':date[1], 'Day':date[2], 'Year':date[0], 'Caption':title, 'Comment':comments, 'Keywords':keywords}, ignore_index=True)
			except:
				#continue
				df = df.append({'Source':dir_name, 'File':infile, 'Species':subdir, 'Latitude':latitudes,
                                        'Longitude':longitude,'Month':'NA', 'Day':'NA', 'Year':'NA', 'Caption':title, 'Comment':comments, 'Keywords':keywords}, ignore_index=True)
				
				
df.to_csv('seal_dataset.csv', index=False)
