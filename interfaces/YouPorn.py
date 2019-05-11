#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import Request, Session
from bs4 import BeautifulSoup
import re

from XInterface import XInterface

class YouPorn(XInterface):
	def getDownloadLink(self,value):
		ss = Session()

		url_base = 'https://www.youporn.com/watch/'+vid+'/'

		r = s.get(url_base)
		soup = BeautifulSoup(r.text, "html.parser")
		download_link = soup.find('noscript').find('video').get('src')

		#return download_link
		return download_link
		
	def getSearchResults(self,value):
		# webbrowser.open(url[, new=0[, autoraise=True]])
		return True