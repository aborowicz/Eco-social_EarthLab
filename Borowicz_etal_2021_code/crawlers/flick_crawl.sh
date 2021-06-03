#PBS -l walltime=04:00:00

#PBS -N seal_crawler_flickr

#PBS -q short

module load shared
module load torque
module load anaconda/3

cd ../..
cd projects/LynchGroup/spacewhale

# Let's find some seals!
# This script has a few jobs. It calls sites with lat and long from a csv
# Then it uses these as params for a crawler script that downloads images
# that have been geotagged within 2.5km of that gps point of that site.
# Images are stored in crawlers/downloaded_images/flickr/<SITE NAME>
#  ------- ------- -------
# There are several parameters to set, which in future could be the source
# another loop (nested loop). The first param is the text tag. Here it's
# 'weddell' for weddell seals. 
# Second: the max_number of images to get per thread. I need to look at this
#         more because I don't know how many threads there are
# Third and 4th: min date and max date to search for images. These are expressed
#                in unix timestamps
# Then -f is the flickr API key
# -y is the lat pulled from the csv
# -x is long from csv
# -n is the site name
# !!! Right now the csv is hard coded in the first line. This should be fine.
# The full site csv is ../seal_site_listASI.csv but there's also one called
# ../seal_site_listmini.csv which is only 3 sites for testing.

source activate ./webseal_env

cd ./git_webseals/seals_geo_survey/crawlers


MY_INPUT='../seal_site_listmini.csv'
declare -a A_LAT
declare -a A_LON
declare -a A_NAME
while IFS=, read -r COL1 COL2 COL3; do
	A_LAT+=("$COL1")
	A_LON+=("$COL2")
	A_NAME+=("$COL3")
done <"$MY_INPUT"

for index in "${!A_LAT[@]}"; do
	python icrawl.py weddell 500 978307200 1551147191  -c 'flickr' -f 'a2ddb1d1e62c931299a4bdb291b86820' -y ${A_LAT[$index]} -x ${A_LON[$index]} -n ${A_NAME[$index]}
done
