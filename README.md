This repo contains a code example for CIRES Earth Lab

There are two parts here:

1. ```FurSeal_Analysis.RMD```, and the associated output ```FurSeal_Analysis.html```
2. The scripts used to scrape and classify image data from Flickr

# The Project

In this example, I use field-collected data (field surveys) alongside image data scraped from Flickr and observations from iNaturalist to try to understand spatial and temporal trends in Antarctic fur seal occurence on the Antarctic Peninsula.
The field-collected data are available in the ```./data directory```. iNaturalist data are in their also, within tne ```./GBIF All iNat Records from Antarctica``` directory

Field-collected data come from the Antarctic Site Inventory, a project of Oceanites, and consist of records of fur seal occurences at sites on the Antarctic Peninsula.
iNaturalist data consist or records of fur seal occurence hat have been verified by several independent identifiers.

For the flickr records, we took what I've been calling an "eco-social" approach, essentially pressing social media data into service as ecological data. We wrote a simple web crawler and sent it to pull images from Flickr, specifically images tagged with the word 'seal' and with a geo-tag within the Peninsula.
Once we'd pulled in the images, we deployed a convolutional neural network to first identify the images that actually contained a seal, and then to identify the species of the seal in the image.

That work was developed for a prior project that was recently published. That paper ("Social sensors for wildlife") is included in the ```./Borowicz_etal_2021_code``` directory. 

Our interest there was in Weddell seals, but we used the byproduct - images of fur seals - as an auxillary dataset here.

If you're viewing this repo within the web portal, you may not be able to view the ```.html``` file that walks through the code. To do this, download the file and open it in a web browser. All necessary packages to run the ```.RMD``` file are listed within the file.
