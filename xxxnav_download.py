#!/usr/bin/python
# -*- coding: utf-8 -*-
from requests import Request, Session
from bs4 import BeautifulSoup
import unicodedata
import re
import os

from interfaces import *
from xxxnav_links import getLinks
from xxxnav_utils import *

def downloadFile(URL,destPath):
	# DOWNLOAD FILE
	with open(destPath, "wb") as f:
		print("Downloading %s") % destPath
		response = requests.get(download_url, stream=True)
		total_length = response.headers.get('content-length')
		if total_length is None: # no content length header
			f.write(response.content)
		else:
			prog_size = 20
			dl = 0
			total_length = int(total_length)
			last_time = time.time()
			time_counter = 0
			chunk_size = 10240 #Bytes
			for data in response.iter_content(chunk_size=chunk_size):
				dl += len(data)
				actual_time = time.time()
				time_elapsed = actual_time - last_time
				time_counter += time_elapsed

				f.write(data)
				done = int(prog_size * dl / total_length)
				last_time = actual_time
				if time_counter == 0:
					velocity = "--- B/s"
				else:
					velocity = dl/time_counter
					if(velocity<1024):
						velocity = "{:0.2f}".format(velocity)+" B/s"
					elif(velocity<(1024*1024)):
						velocity = "{:0.2f}".format(velocity/1024)+" kB/s"
					else:
						velocity = "{:0.2f}".format(velocity/(1024*1024))+" MB/s"
				message = velocity + " [" + str(dl) + "/" + str(total_length) + "]"
				sys.stdout.write("\r[%s%s] %s" % ('=' * done, ' ' * (prog_size-done),message))    
				sys.stdout.flush()
	print(" ")
	print(f"Finshed downloading '{URL}' to '{destPath}'")
	return True


def downloadLinks(Links=[]):

	links = getLinks(Links)
	scriptpath = os.path.split(os.path.realpath(__file__))[0]
	videospath = scriptpath + '/videos/'
	result = True


	for link in links:
		videoname = sanitizeFileName(link)
		destPath = videospath + videoname
		print(f'Downloading link "{link}" to "{destPath}"...');
		res = downloadFile(link)
		result = result & res;
	
	return result


	# for link in value:
	# 	print(link)
	
	# return(value)
		
#If running from script
if __name__ == "__main__":
	parser = argparse.ArgumentParser("xxxnav_download")
	parser.add_argument("links", help="video urls to get direct file links", nargs='+', type=str)
	args = parser.parse_args()
	updateSearch(args.links)