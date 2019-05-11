#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import Request, Session
from bs4 import BeautifulSoup
import re

from XInterface import XInterface

class Beeg(XInterface):
    def getDownloadLink(self,value):
    	return 'hey ho'
	def getSearchResults(self,value):
		s = Session()

		url_base = 'https://beeg.com/'+value


		r = s.get(url_base)
		print r.text

		#ToDo (needs javascript)

		# soup = BeautifulSoup(r.text, "html.parser")
		# sources = (soup.findAll('script')[13].string.encode('utf8')) #relacionados
		# m = re.search('sources.+},', sources).group().split(",")[-2]
		# m2 = re.search(':".+"', m).group().replace(':"',"").replace('"',"").replace("\\","")
		# print m2

		# js_downloads = soup.findAll('script')[6].string.encode('utf8')
		# download_link = m.group().replace("setVideoUrlHigh('","").replace("')","")
		# print download_link

		#for x in soup.findAll('script'):
			#print x.text