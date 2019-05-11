#!/usr/bin/python
# -*- coding: utf-8 -*-
from requests import Request, Session
from bs4 import BeautifulSoup
import re
from xxxnav_utils import *

def updateRecommended(terms = []):

	term = terms.join(' ')

	s = Session()

	url_base = 'https://www.xnxx.com/search/'+term

	r = s.get(url_base)
	soup = BeautifulSoup(r.text, "html.parser")


	video_list = soup.findAll('div','thumb-block ')

	for video in video_list:
		print(video.text)

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
	updateRecommended(args.term)