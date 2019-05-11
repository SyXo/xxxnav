#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import Request, Session
from bs4 import BeautifulSoup
import re

from XInterface import XInterface

class RedTube(XInterface):
	def getDownloadLink(self,value):
		s = Session()

		url_base = 'https://www.redtube.com/'+value


		r = s.get(url_base)
		soup = BeautifulSoup(r.text, "html.parser")
		print soup.find('noscript').find('source').get('src')
		
	def getSearchResults(self,value):
		# webbrowser.open(url[, new=0[, autoraise=True]])
		return True