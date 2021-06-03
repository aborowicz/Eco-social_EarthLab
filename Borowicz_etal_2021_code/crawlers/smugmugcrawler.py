# Tyler Estro - Stony Brook University 11/03/17
#
# modified from https://github.com/iammrhelo/InstagramCrawler

from __future__ import division
import argparse, codecs, json, os, re, requests, selenium, sys, time
from collections import defaultdict
from selenium import webdriver
try:
	from urlparse import urljoin
	from urllib import urlretrieve
except ImportError:
	from urllib.parse import urljoin
	from urllib.request import urlretrieve

# HOST
HOST = 'http://www.smugmug.com'

# JAVASCRIPT COMMANDS
SCROLL_UP = "window.scrollTo(0, 0);"
SCROLL_DOWN = "window.scrollTo(0, document.body.scrollHeight);"

class SmugMugCrawler(object):
	"""
		Crawler class
	"""
	def __init__(self):
		self._driver = webdriver.PhantomJS()
		self._driver.implicitly_wait(10)
		self.data = defaultdict(list)

	def quit(self):
		self._driver.quit()

	def crawl(self, dir_path, keyword, max_num):
		print("dir_path: {}, keyword: {}, max_num: {}"
			  .format(dir_path, keyword, max_num))

		# Browse target page
		self.browse_target_page(keyword)
		# Scroll down until target number photos is reached
		self.scroll_to_num_of_posts(max_num)
		# Scrape photo links
		self.scrape_photo_links(max_num)
		# Save to directory
		self.download_and_save(dir_path, keyword)

		# Quit driver
		print("Quitting driver...")
		self.quit()

	def browse_target_page(self, keyword):
		target_url = HOST + '/search/?n=&scope=node&scopeValue=0&c=photos&q=' + keyword + '#s=recent'
		self._driver.get(target_url)
		time.sleep(5.0)

	def scroll_to_num_of_posts(self, max_num):
		# Get total number of posts of page
		num_info = re.search(r'([,\d]+) images', self._driver.page_source).group()
		num_images = int(num_info.strip(' images').replace(',', ''))
		print("images: {}, max_num: {}".format(num_images, max_num))
		max_num = max_num if max_num < num_images else num_images
		
		# scroll page until reached
		num_to_scroll = int((max_num - 4) / 4) + 1
		for page in range(num_to_scroll):
			print('Scrolling to page {} of {}.'.format(page+1, num_to_scroll), end='\r')
			self._driver.execute_script(SCROLL_DOWN)
			time.sleep(0.2)
		print('\r')

	def scrape_photo_links(self, max_num):
		print("Scraping image links...")
		smug_photo_links = re.finditer(r'url\(https://photos.smugmug.com...[\/\w \.-]*..[\/\w \.-]*..[\/\w \.-]*..[\/\w \.-].(jpg|jpeg|png)', 
			self._driver.page_source)
		photo_links = [m.group(0).lstrip('url(') for m in smug_photo_links]
		print("Number of image links: {}".format(len(photo_links)))
		self.data['photo_links'] = photo_links[0:max_num]

	def download_and_save(self, dir_path, keyword):
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		print("Saving to directory: {}".format(dir_path))

		# Save Photos
		for idx, photo_link in enumerate(self.data['photo_links'], 0):
			# Filename
			_, ext = os.path.splitext(photo_link)
			filename = keyword + str(idx) + ext
			filepath = os.path.join(dir_path, filename)
			print("Downloading {}".format(filename), end='\r')
			# Send image request
			try:
				urlretrieve(photo_link, filepath)
			except:
				continue
		print('\r')

def main():
	#	Arguments  #
	parser = argparse.ArgumentParser(description='SmugMug Crawler')
	parser.add_argument('keyword', type=str, help="keyword to crawl for")
	parser.add_argument('max_num', type=int, help='maximum number of images to download')
	parser.add_argument('-d', '--dir_path', type=str,
						default='./downloaded_images/smugmug', help='directory to save results')
	args = parser.parse_args()
	#  End Argparse #
	
	crawler = SmugMugCrawler()
	crawler.crawl(dir_path=args.dir_path,
				  keyword=args.keyword,
				  max_num=args.max_num)

if __name__ == "__main__":
	main()
