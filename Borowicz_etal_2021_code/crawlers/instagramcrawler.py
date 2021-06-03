# Tyler Estro - Stony Brook University 11/03/17
#
# modified from https://github.com/iammrhelo/InstagramCrawler

from __future__ import division
import argparse, codecs, json, os, re, sys, time
from collections import defaultdict
import requests, selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
try:
	from urlparse import urljoin
	from urllib import urlretrieve
except ImportError:
	from urllib.parse import urljoin
	from urllib.request import urlretrieve

# HOST
HOST = 'http://www.instagram.com'

# SELENIUM CSS SELECTOR
CSS_LOAD_MORE = "a._1cr2e._epyes"
CSS_RIGHT_ARROW = "a[class='_de018 coreSpriteRightPaginationArrow']"

# JAVASCRIPT COMMANDS
SCROLL_UP = "window.scrollTo(0, 0);"
SCROLL_DOWN = "window.scrollTo(0, document.body.scrollHeight);"

class InstagramCrawler(object):
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
		print("dir_path: {}, keyword: {}, max_num: {}".format(dir_path, keyword, max_num))
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
		relative_url = urljoin('explore/tags/', keyword)
		target_url = urljoin(HOST, relative_url)
		self._driver.get(target_url)

	def scroll_to_num_of_posts(self, max_num):
		# Get total number of posts of page
		num_info = re.search(r'\], "count": \d+',
							 self._driver.page_source).group()
		num_of_posts = int(re.findall(r'\d+', num_info)[0])
		print("posts: {}, max_num: {}".format(num_of_posts, max_num))
		max_num = max_num if max_num < num_of_posts else num_of_posts

		# scroll page until reached
		loadmore = WebDriverWait(self._driver, 10).until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, CSS_LOAD_MORE))
		)
		loadmore.click()

		num_to_scroll = int((max_num - 12) / 12) + 1
		for page in range(num_to_scroll):
			print('Scrolling to page {} of {}.'.format(page+1, num_to_scroll), end='\r')
			self._driver.execute_script(SCROLL_DOWN)
			time.sleep(0.2)
			self._driver.execute_script(SCROLL_UP)
			time.sleep(0.2)
		print('\r')
		
	def scrape_photo_links(self, max_num):
		print("Scraping image links...")
		# modified (jpg|jpeg|png) from .jpg just in case instagram has other formats
		encased_photo_links = re.finditer(r'src="([https]+:...[\/\w \.-]*..[\/\w \.-]*'
										  r'..[\/\w \.-]*..[\/\w \.-].(jpg|jpeg|png))', self._driver.page_source)
		photo_links = [m.group(1) for m in encased_photo_links]
		print("Number image links: {}".format(len(photo_links)))
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
			print('Downloading {}'.format(filename), end='\r')
			# Send image request
			try:
				urlretrieve(photo_link, filepath)
			except:
				continue
		print('\r')

def main():
	#	Arguments  #
	parser = argparse.ArgumentParser(description='Instagram Crawler')
	parser.add_argument('keyword', type=str, help="target keyword to crawl for (dont include #)")
	parser.add_argument('max_num', type=int, help='maximum number of images to download')
	parser.add_argument('-d', '--dir_path', type=str,
						default='./downloaded_images/instagram', help='directory to save results')
	args = parser.parse_args()
	#  End Argparse #
	crawler = InstagramCrawler()
	crawler.crawl(dir_path=args.dir_path,
				  keyword=args.keyword,
				  max_num=args.max_num)

if __name__ == "__main__":
	main()
