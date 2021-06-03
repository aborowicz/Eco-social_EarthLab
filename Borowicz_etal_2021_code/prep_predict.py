# Tyler Estro - Stony Brook University 02/06/18
#
# Recursively removes files incompatible with PIL.Image.open or don'taken
# contain metadata.
# Depends on images being located in ./downloaded_images directory
#
# Usage: python prep_predict.py

# note: i'd like to add duplicate image detection as well

import os
import piexif
from PIL import Image

for path, subdirs, files in os.walk('./downloaded_images'):
    for filename in files:
        f = os.path.join(path, filename)
        # PIL.Image.open test
        try:
            image = Image.open(f)
        except:
            print('prep_predict: PIL.Image.open failed - Removed: ' + f)
            os.system("rm \"" + f + "\"")
            continue
        # piexif metadata test
        try:
            exif_dict = piexif.load(f)
        except:
            print('prep_predict: PiExif can not find EXIF data - Removed: ' + f)
            os.system("rm \"" + f + "\"")
            continue
        if not all(k in exif_dict['GPS'] for k in (piexif.GPSIFD.GPSLatitude, piexif.GPSIFD.GPSLatitudeRef)) \
                or not all(k in exif_dict['GPS'] for k in (piexif.GPSIFD.GPSLongitude, piexif.GPSIFD.GPSLongitudeRef)) \
                or (not piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"] and not piexif.GPSIFD.GPSDateStamp in
                    exif_dict["GPS"]):
            print('prep_predict: Insufficient Metadata - Removed: ' + f)
            os.system("rm \"" + f + "\"")
            continue
print("prep_predict: Removal of incompatible files completed")
