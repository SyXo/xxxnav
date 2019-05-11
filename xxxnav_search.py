#!/usr/bin/python
# -*- coding: utf-8 -*-
from requests import Request, Session
from bs4 import BeautifulSoup
import re
import os

from xxxnav_utils import *

from interfaces.XNXX import XNXX
from interfaces.XHamster import XHamster

def writeToResults(html):
	scriptpath = os.path.split(os.path.realpath(__file__))[0]
	webpath = scriptpath + '/web/'
	searchfile = webpath + 'search.html'

	# DOWNLOAD FILE
	with open(searchfile, "w") as f:
		f.write(html)

def sanitizeFileName(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '-', value))

    return value;

def downloadThumb(thumb_url = ''):
	scriptpath = os.path.split(os.path.realpath(__file__))[0]
	thumbs_path = scriptpath + '/web/thumbs/'
	vid = (re.findall('_\d+.jpg',thumb_url)[0]).replace('_','').replace('.jpg','')
	print('Downloading thumbs for vid %s...' % vid)
	if not os.path.exists(thumbs_path+vid):
		os.makedirs(thumbs_path+vid)
	regex = re.compile(r"\/\d+_", re.IGNORECASE)
	for x in xrange(1,11):
		thumbx_url = regex.sub("/%d_" % x, thumb_url)
		filename = thumbs_path+vid+'/'+str(x)+'.jpg'
		with open(filename, "wb") as f:
			response = requests.get(thumbx_url, stream=True)
			for data in response.iter_content(chunk_size=10240):
				f.write(data)

def updateSearch(terms = []):

	#Get XHamster videos

	term = " ".join(terms)

	videos = XNXX().getSearchResults(term)
	
	for i in videos:
		DownloadThumb(videos[i]['thumb'])

	return True
 
	#print r.text
	                                                       
	# print(soup.findAll('script')[6].string.encode('utf8')) #relacionados

	# js_downloads = soup.findAll('script')[6].string.encode('utf8')
	# m = re.search('setVideoUrlHigh\(\'.+\'\)', js_downloads)
	# download_link = m.group().replace("setVideoUrlHigh('","").replace("')","")
	# print download_link

	#for x in soup.findAll('script'):
		#print x.text
		
#If running from script
if __name__ == "__main__":
	parser = argparse.ArgumentParser("xxxnav_search")
	parser.add_argument("term", help="term(s) for search", nargs='+', type=str)
	args = parser.parse_args()
	updateSearch(args.term)