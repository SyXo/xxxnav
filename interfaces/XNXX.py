#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import Request, Session
from bs4 import BeautifulSoup
import re

from .XInterface import XInterface

class XNXX(XInterface):
	def getDownloadLink(self,vid):
			s = Session()
			url_base = 'https://www.xnxx.com/video-'+vid+'/'
			r = s.get(url_base)
			soup = BeautifulSoup(r.text, "html.parser")
			# print(soup.findAll('script')[6].string.encode('utf8')) #relacionados
			js_downloads = soup.findAll('script')[6].string
			# print(soup.findAll('script'))
			m = re.search('setVideoUrlHigh\(\'.+\'\)', js_downloads)
			download_link = m.group().replace("setVideoUrlHigh('","").replace("')","")
			return download_link

	def getVideosFromHtml(self,html):
		videos = {}
		soup1 = BeautifulSoup(html,"html.parser")
		video_list = soup1.findAll('div',attrs={'class' : 'thumb-block'})
		c = 0
		for video in video_list:
			videos[c] = {
				'preview' 	: '',
				'thumb'		: video.find('div', class_="thumb").find('img').get('data-src'),
				'name'		: video.find('div', class_="thumb-under").find('a').get("title"),
				'id'		: video.get('id').replace("video-",""),
				'duration'	: video.find('p',class_='metadata').string
			}
			c += 1
		return videos
		
	def getSearchResults(self,value):
		# MAKE FIRST ACCESS TO VIDEO TO GET SESSION
		print("Searching for videos with keyword '%s'..." % value)
		url1 = 'https://www.xnxx.com/search/'+value
		headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1' }
		s = Session()
		s.headers = headers
		resp = s.request('GET',url1)
		print("First call HTTP status: ["+str(resp.status_code)+"] "+resp.reason)

		# GET VIDEO LIST
		videos = {}
		# video_list = soup1.findAll('div',attrs={'class' : 'thumb-block'})
		c = 0
		# for video in video_list:
		# 	videos[c] = {
		# 		'preview' 	: video.find('div','thumb_container').get('data-previewvideo'),
		# 		'thumb'		: video.find('img','thumb').get('src'),
		# 		'name'		: video.find('u').string.replace(",",""),
		# 		'id'		: video.find('img','hSprite').get('id'),
		# 		'duration'	: video.find('b').string
		# 	}
		# 	c += 1
		return self.getVideosFromHtml(resp.text)

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