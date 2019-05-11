#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import Request, Session
from bs4 import BeautifulSoup
import re

from XInterface import XInterface

class PornHub(XInterface):
    def getDownloadLink(self,value):
    	s = Session()

		url_base = 'https://pornhub.com/view_video.php?viewkey='+value


		r = s.get(url_base)
		soup = BeautifulSoup(r.text, "html.parser")
		m = re.search('\[{"defaultQuality".+"}]', r.text)
		video_links = m.group().split("},{")
		for video_link in video_links:
			link = re.search('videoUrl.+', video_link).group().replace('videoUrl":"',"").replace('"',"")
			if(link != ""):
				return link
				break;
		return False
	def getSearchResults(self,value):
		# webbrowser.open(url[, new=0[, autoraise=True]])
        return True