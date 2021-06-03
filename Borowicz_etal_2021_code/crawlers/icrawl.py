# Tyler Estro - Stony Brook University 10/26/17
#
# Based on iCrawler https://pypi.python.org/pypi/icrawler/0.4.7
# Documentation: http://icrawler.readthedocs.io/en/latest/index.html
#
# This script crawls several Web sites and downloads images matching the 
# specified keyword(s). All of these sites have different limits and terms, 
# and some require an API key. Do not make excessive queries from the same
# host!
#
# Baidu, Bing, and Google only allow 1000 results per query.
# Flickr API limits you to 3600 queries per hour. Do not exceed this or your API will get banned.
# Photobucket uses their top 100 RSS feed, so only returns 100 max.

#=============== Parsing arguments ===============#

import argparse
parser = argparse.ArgumentParser(description='iCrawler-based bundle of Web Crawlers')
parser.add_argument('keyword', type=str, help='the keyword(s) to search for')
parser.add_argument('max_num', type=int, help='the maximum number of results to return per search')
parser.add_argument('mindate', type=str, help='the earliest date to search from in flickr search')
parser.add_argument('maxdate', type=str, help='the latest date to search from in flickr search')
parser.add_argument('-c', '--crawlers', nargs='+', type=str, help='list of crawlers to use',
	choices=['all','baidu','bing','google','flickr','photobucket'], default='all')
parser.add_argument('-f', '--flickr', type=str, help='your Flickr API key (required to crawl Flickr)')
parser.add_argument('-t', '--threads', type=int, help='number of downloader and parser threads / 2', default=1)

##parser.add_argument('-b', '--bbox', type=str, help='bounding boxof area. Comma-delimited list of 4 vals in decimal form. Min long, min lat, max long, max lat.')
parser.add_argument('-x', '--lon', type=str, help='longitude for radial center for flicker geo-search')
parser.add_argument('-y', '--lat', type=str, help='latitude for radial center for flickr geo-search')
parser.add_argument('-n', '--nam', type=str, help='site name to name directory for images')


args = parser.parse_args()
if 'all' in args.crawlers:
	crawlers = ['baidu','bing','google','flickr','photobucket']
else:
	crawlers = args.crawlers
if 'flickr' in crawlers and not args.flickr:
	parser.error('you must provide a Flickr API Key to crawl Flickr')
 
#=================== File Naming ================# 
import base64
from icrawler import ImageDownloader
from six.moves.urllib.parse import urlparse

class PrefixNameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameDownloader, self).get_filename(
            task, default_ext)
        return 'prefix_' + filename
        
class Base64NameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        url_path = urlparse(task['file_url'])[2]
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                    'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm'
            ]:
                extension = default_ext
        else:
            extension = default_ext
        # works for python 3
        filename = base64.b64encode(url_path.encode()).decode()
        return '{}.{}'.format(filename, extension)
        
class OriginalNameDownloader(ImageDownloader):
    
    def get_filename(self, task, default_ext):
        url_path = urlparse(task['file_url'])[2]
        filename = url_path.split("/")[-1] 
        filename = filename.replace('\\','_')
        #filename = url_path.replace("/","pppp")
        #filename = filename.replace("\\","_")
        return '{}'.format(filename)

#=================== Crawling ===================#

from icrawler.builtin import (GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler, FlickrImageCrawler)
import os, sys
from datetime import date
from photobucket import PhotoBucketCrawler

if 'baidu' in crawlers:
	baidu_crawler = BaiduImageCrawler(storage={'root_dir': 'downloaded_images/baidu'},
            #downloader_cls=Base64NameDownloader,
            downloader_cls=OriginalNameDownloader,
		downloader_threads=args.threads, parser_threads=args.threads)
	baidu_crawler.crawl(args.keyword, max_num=min(1000, args.max_num))

if 'bing' in crawlers:	
	bing_crawler = BingImageCrawler(storage={'root_dir': 'downloaded_images/bing'},
             #downloader_cls=Base64NameDownloader,
             downloader_cls=OriginalNameDownloader,
		downloader_threads=args.threads, parser_threads=args.threads)
	bing_crawler.crawl(args.keyword, max_num=min(1000, args.max_num))

if 'flickr' in crawlers:
	flickr_crawler = FlickrImageCrawler(args.flickr, storage={'root_dir': 'downloaded_images/flickr/%s' % args.nam},
            #downloader_cls=Base64NameDownloader,     
            #downloader_cls=OriginalNameDownloader,                    
		downloader_threads=args.threads, parser_threads=args.threads)
	##flickr_crawler.crawl(text=args.keyword, sort='relevance', max_num=args.max_num)

	## Draft - There are a few different iterations below that support using the script in different ways - 
	## either looping through with sites, or pulling non geo-tagged images, etc.

#	flickr_crawler.crawl(text='weddell seal', sort='relevance', max_num=args.max_num, has_geo=0, min_upload_date=args.mindate, max_upload_date=args.maxdate)

	flickr_crawler.crawl(text=args.keyword, sort='relevance', max_num=args.max_num, lat=args.lat, lon=args.lon, radius=5, min_upload_date=args.mindate, max_upload_date=args.maxdate)


if 'google' in crawlers:
	google_crawler = GoogleImageCrawler(storage={'root_dir': 'downloaded_images/google'},
            #downloader_cls=Base64NameDownloader,
            downloader_cls=OriginalNameDownloader,
		downloader_threads=args.threads, parser_threads=args.threads)
	google_crawler.crawl(args.keyword, max_num=min(1000, args.max_num))
	
if 'photobucket' in crawlers:
	photobucket_crawler = PhotoBucketCrawler(storage={'root_dir': 'downloaded_images/photobucket'},
            #downloader_cls=Base64NameDownloader,    
            downloader_cls=OriginalNameDownloader,                          
		downloader_threads=args.threads, parser_threads=args.threads)
	photobucket_crawler.crawl(args.keyword, max_num=min(100, args.max_num))
	
