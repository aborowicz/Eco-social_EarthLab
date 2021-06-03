#PBS -l walltime=04:00:00

#PBS -N seal_crawler_flickr

#PBS -q short

module load shared
module load torque
module load anaconda/3

cd ../..
cd projects/LynchGroup/spacewhale

# Let's find some seals!
# This script asks for images of weddell seals that are NOT geo_tagged
# over a specific time range. It does this by calling unix timecodes
# stored in a csv and looping over them.
# Images are stored in crawlers/downloaded_images/flickr/<Timestamp>
#  ------- ------- -------
# There are several parameters to set, which in future could be the source
# another loop (nested loop). The first param is the text tag. Here it's
# 'weddell seal' 
# Second: the max_number of images to get per thread. I need to look at this
#         more because I don't know how many threads there are
# Third and 4th: min date and max date to search for images. These are expressed
#                in unix timestamps
# Then -f is the flickr API key
# -n is the directory name, here the end date in unix timecode
# !!! Right now the csv is hard coded in the first line. This should be fine.
# The time csv is ../seal_time_loop.csv. This only needs to be run once.
# Future iterations can do this straight on the command line as we collect new
# images from future time spans.

source activate ./webseal_env

cd ./git_webseals/seals_geo_survey/crawlers


MY_INPUT='../seal_time_loop.csv'
declare -a A_START
declare -a A_END
declare -a A_TIMES
declare -a A_TIMEE
while IFS=, read -r COL1 COL2 COL3 COL4; do
        A_START+=("$COL1")
		A_END+=("$COL2")
        A_TIMES+=("$COL3")
		A_TIMEE+=("$COL4")
done <"$MY_INPUT"

for index in "${!A_START[@]}"; do
        python icrawl.py 'weddell seal' 500 ${A_START[$index]} ${A_END[$index]}  -c 'flickr' -f 'a2ddb1d1e62c931299a4bdb291b86820' -n ${A_END[$index]}
done

