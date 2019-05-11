#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import Request, Session
from bs4 import BeautifulSoup
import re

from XInterface import XInterface

class PornHD(XInterface):
	def getDownloadLink(self,value):
		s = Session()

		url_base = 'https://www.pornhd.com/videos/'+value+'/'


		r = s.get(url_base)
		soup = BeautifulSoup(r.text, "html.parser")
		sources = (soup.findAll('script')[13].string.encode('utf8')) #relacionados
		m = re.search('sources.+},', sources).group().split(",")[-2]
		m2 = re.search(':".+"', m).group().replace(':"',"").replace('"',"").replace("\\","")
		return m2
		
	def getSearchResults(self,value):
		# webbrowser.open(url[, new=0[, autoraise=True]])
		return True