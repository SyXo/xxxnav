#!/usr/bin/python
# -*- coding: utf-8 -*-
from requests import Request, Session
from bs4 import BeautifulSoup
import re

from interfaces.XNXX import XNXX
from xxxnav_utils import *


def getLinks(value=[]):

	result = map(getDownloadLink, value) 
	# print(list(result)) 
	return result


	# for link in value:
	# 	print(link)
	
	# return(value)


def getDownloadLink(link):
	source = DetectSource(link)
	print(f"Found source '{source}' for link '{link}'")

	#YouPorn
	if source == 'YP': 
		vid = re.search('watch\/\d+\/', link).group().replace("watch/","").replace("/","")
		# print vid
		return interfaces.YouPorn.getDownloadLink(link)

	#xHamster
	elif source == 'XH':
		pass
	elif source == 'PD': #PornHD
		pass
	elif source == 'PH': #PornHub
		pass
	elif source == 'RT': #RedTube
		pass
	elif source == 'XN': #Xnxx
		vid = re.search('xnxx.com\/video-[0-9a-z]+\/', link).group().replace("xnxx.com\/video-","").replace("/","")
		
		# print vid
		return XNXX().getDownloadLink(link)
	else:
		return("Unknown source for link '%s'!" % link)

def DetectSource(link = ''):

	if(link.find('youporn.com/')>-1):
		return 'YP'
	elif(link.find('xhamster.com/')>-1):
		return 'XH'
	elif(link.find('xnxx.com/')>-1):
		return 'XN'



if __name__ == "__main__":
	lnk = getLinksFromArgs()
	print(lnk)