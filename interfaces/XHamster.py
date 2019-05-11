#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re

import os
#import urllib2
#import urllib
#import cookielib
import requests
import time
import sys
import re
from bs4 import BeautifulSoup

from .XInterface import XInterface

class XHamster(XInterface):
	def getDownloadLink(self,value):
		# BASIC DEFINITIONS
		#videoID = 

		# MAKE FIRST ACCESS TO VIDEO TO GET SESSION
		# print("Preparing to download video ID %s..." % videoID)
		# url1 = 'https://xhamster.com/videos/'+videoID
		headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1' }
		s = requests.Session()
		s.headers = headers
		resp = s.request('GET',value)
		print("First call HTTP status: ["+str(resp.status_code)+"] "+resp.reason)
		soup1 = BeautifulSoup(resp.text,"html.parser")

		# GET VIDEO NAME
		video_name = soup1.h1.string
		print("Video title: '%s'" % video_name)
		filename = video_name+'.mp4'

		# GET AVALIABLE VIDEO QUALITY
		box_download = str(soup1.find("table", {"id": "loadPopup"}))
		video_title = str(soup1.find("table", {"id": "loadPopup"}))
		qltys = re.findall('\/download\/[0-9]+p',box_download)
		qltys = [w.replace('/download/', '') for w in qltys]
		print('Avaliable qualities for download: [%s]' % ', '.join(qltys))
		print('[%s] was chosen as the best one' % qltys[-1])
		quality = qltys[-1]
		
		# PREPARE HEADERS FOR AJAX
		headers['X-Requested-With'] = 'XMLHttpRequest'
		headers['Host'] = "xhamster.com"
		headers['Accept'] = "*/*"
		headers['Accept-Language'] = "en-US,en;q=0.5"
		headers['Accept-Encoding'] = "gzip, deflate, br"
		headers['Referer'] = "https://xhamster.com/videos/"+videoID
		headers['x-legacy'] = "true"
		headers['Connection'] = "keep-alive"

		# EXECUTE AJAX
		s.headers = headers
		url2 = "https://xhamster.com/ajax/download_signup.php?vid="+videoID
		resp2 = s.request('GET',url2, data = {'vid': videoID})
		print("Second call HTTP status: ["+str(resp2.status_code)+"] "+resp2.reason)
		
		# PARSE AJAX DATA
		soup = BeautifulSoup(resp2.text,"html.parser")
		video_download_time = ''
		video_download_hash = ''
		for hidden in soup.find_all('input'):
			hidden_id = hidden.get('id')
			hidden_val = hidden.get('value')

			if(hidden_id == 'video_download_time'):
				video_download_time = hidden_val
			elif(hidden_id == 'video_download_hash'):
				video_download_hash = hidden_val
		print("Time = %s, Hash = %s" % (video_download_time, video_download_hash))

		
		# WAIT TO DOWNLOAD
		wait_sec = 20
		download_url = 'https://xhamster.com/movies/8340706/download/'+quality+'?t='+video_download_time+'&h='+video_download_hash
		return download_url
		
	def getSearchResults(self,value):
		# MAKE FIRST ACCESS TO VIDEO TO GET SESSION
		print("Searching for videos with keyword '%s'..." % value)
		url1 = 'https://xhamster.com/search?q='+value
		headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1' }
		s = requests.Session()
		s.headers = headers
		resp = s.request('GET',url1)
		print("First call HTTP status: ["+str(resp.status_code)+"] "+resp.reason)
		soup1 = BeautifulSoup(resp.text,"html.parser")

		# GET VIDEO LIST
		videos = {}
		video_list = soup1.findAll('div',attrs={'class' : 'video'})
		c = 0
		for video in video_list:
			videos[c] = {
				'preview' 	: video.find('div','thumb_container').get('data-previewvideo'),
				'thumb'		: video.find('img','thumb').get('src'),
				'name'		: video.find('u').string.replace(",",""),
				'id'		: video.find('img','hSprite').get('id'),
				'duration'	: video.find('b').string
			}
			c += 1

		# GET PAGE COUNT
		pages = soup1.find('div','pager').findAll('a')
		max_page = 1
		limit_page = 1
		for page in pages:
			if(page.string is not None):
				if(page.string.isdigit()):
					max_page = int(page.string)
		print('Total pages found: %d' % max_page)

		if(max_page > limit_page):
			print('Number of pages truncated to %d' % limit_page)
			max_page = limit_page

		# GET MIDDLE PAGES RESULTS
		if(max_page>1):
			for x in xrange(2,max_page+1):
				print("Getting results for page %d..." % x)
				urlx = 'https://xhamster.com/search?q='+query+'&p='+str(x)
				respx = s.request('GET',urlx)
				soupx = BeautifulSoup(respx.text,"html.parser")
				video_list = soupx.findAll('div',attrs={'class' : 'video'})
				for video in video_list:
					videos[c] = {
						'preview' 	: video.find('div','thumb_container').get('data-previewvideo'),
						'thumb'		: video.find('img','thumb').get('src'),
						'name'		: video.find('u').string.replace(",",""),
						'id'		: video.find('img','hSprite').get('id'),
						'duration'	: video.find('b').string
					}
					c += 1
		print('Total videos found: %d' % len(videos))

		return videos