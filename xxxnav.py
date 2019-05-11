#!/usr/bin/python3
# -*- coding: utf-8 -*-


# #Tornado imports
# import tornado.ioloop
# import tornado.web

# #Utils imports
# from xdownloader_download import xDownload
# from xdownloader_search import xSearch

# #Creates routes
# application = tornado.web.Application([
# 	(r"/download", xDownload),
# 	(r"/search/([0-9,]+)", xSearch),
# ])

# #Main server port
# port = 8899
 
# #When running direct from script, start webserver
# if __name__ == "__main__":
# 	print "Starting Python Tornado Webserver at port {}".format(port)
# 	application.listen(port)
# 	tornado.ioloop.IOLoop.instance().start()	

import argparse
import webbrowser
import os

from xxxnav_utils import *
from xxxnav_links import getLinks
from xxxnav_search import updateSearch
from xxxnav_download import downloadLinks
from xxxnav_recommended import updateRecommended

def openURL(URL):
	scriptpath = os.path.split(os.path.realpath(__file__))[0]
	webbrowser.open(scriptpath + '/web/' + URL,1)




#If running from script
if __name__ == "__main__":

	parser = argparse.ArgumentParser("xxxnav")
	parser.add_argument("action", help="links | download | search | recommended", type=str)
	parser.add_argument("value", help="check xxxnav_[action] -h to check the correct argument for each action", nargs='+', type=str)
	args = parser.parse_args()

	if args.action == 'download':
		result = downloadLinks(args.value)
		if result == True:
			openURL('index.html')
			print('Look for your library results in web/index.html')
		else:
			print('I wasn\'t able to download your links, sorry.');
	if args.action == 'links':
		result = getLinks(args.value)
		for link in result:
			print(link)

	elif args.action == 'search':
		result = updateSearch(args.value)
		if result == True:
			openURL('search.html')
			print('Look for search results in web/search.html')
		else:
			print(f'No results found for "{args.value}"! Try another keyword, you creepy.');

	elif args.action == 'recommended':
		result = updateRecommended(args.value)
		if result == True:
			openURL('recommended.html')
			print('Look for search results in web/recommended.html')
		else:
			print('I wasn\'t able to generate your recommendations, sorry. Perhaps you could try the search option?');
			print(f'No results found for "{args.value}"! Try another keyword, you creepy.');		

	else:
		print(f'Unkown action {args.action}')
	


"""
Fonts:

http://www.drdobbs.com/open-source/building-restful-apis-with-tornado/240160382
"""
