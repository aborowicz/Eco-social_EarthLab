# Tyler Estro - Stony Brook University 11/03/17
#
# This is a custom crawler that grabs the 100 latest images from PhotoBucket RSS Feeds
#
from bs4 import BeautifulSoup
from icrawler import Crawler, Parser, Feeder, SimpleSEFeeder, ImageDownloader

class PhotoBucketFeeder(Feeder):

	def feed(self, keyword):
		url = 'http://feed.photobucket.com/images/{}/feed.rss'.format(keyword)
		self.out_queue.put(url)
		self.logger.debug('put url to url_queue: {}'.format(url))


class PhotoBucketParser(Parser):

	def parse(self, response):
		soup = BeautifulSoup(
			response.content.decode('utf-8', 'ignore'), 'lxml')
		enclosures = soup.select('enclosure[url]')
		for enc in enclosures:
			yield dict(file_url=enc['url'])

class PhotoBucketCrawler(Crawler):

	def __init__(self,
				 feeder_cls=PhotoBucketFeeder,
				 parser_cls=PhotoBucketParser,
				 downloader_cls=ImageDownloader,
				 *args,
				 **kwargs):
		super(PhotoBucketCrawler, self).__init__(feeder_cls, parser_cls,
											   downloader_cls, *args, **kwargs)

	def crawl(self,
			  keyword,
			  offset=0,
			  max_num=100,
			  min_size=None,
			  max_size=None,
			  file_idx_offset=0):
		feeder_kwargs = dict(
			keyword=keyword)
		downloader_kwargs = dict(
			max_num=max_num,
			min_size=min_size,
			max_size=max_size,
			file_idx_offset=file_idx_offset)
		super(PhotoBucketCrawler, self).crawl(
feeder_kwargs=feeder_kwargs, downloader_kwargs=downloader_kwargs)