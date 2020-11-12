#!/usr/bin/env python3
import os
import sys
import requests
import re
import time

from multiprocessing.pool import ThreadPool

try:
	from bs4 import BeautifulSoup as Soup
except BaseException as exc:
	print("You need the bs4 library, please install it with pip3!")
	exit(1)


def download_file(file):
	if "Google Sites" in file: # literally no idea where it is comming from, looking into it later
		return False 
	try:
		print("Downloading {}...".format(file))
	
		contents = s.get(file)

		download_path = os.path.join("firmware", file.rsplit('/',1)[-1])

		if contents.status_code == requests.codes.ok:
			# ensure we actually got a cab archive
			if contents.content[:4].hex() == "4d534346": # Checking signature, http://download.microsoft.com/download/4/d/a/4da14f27-b4ef-4170-a6e6-5b1ef85b1baa/[ms-cab].pdf
				with open(download_path, "wb+") as f:
					f.write(contents.content)
					return True
			else:
				print("{} did not return a cab file, not going to save it.")

	except Exception as exc:
		print("Error while trying to get {}: {}".format(file ,exc))
	return False

def resolve_blogspot(): 
	content = s.get("https://www.w3.org/services/html2txt?url=http%3A%2F%2Fsoslouz.blogspot.com%2F2018%2F08%2Fcurrent-official-navcores-for-all.html").text
	urls = []

	for i in range(0, len(content)):
		if content[i:i+len("_http")] == "_http":
			end = 0
			while content[i+end:i+end+len(".cab")] != ".cab":
				end+=1
			link = content[i+1:i+end+len(".cab")].replace(" ", "").replace("\n", "")
			if "_http" in link:
				links = link.split("_http")
				if links[0].endswith(".ca"):
					links[0]+="b"
				if links[0].startswith("//"):
					links[0] = "http:"+links[0]
				links[1] = links[1][1:]
				if links[1].startswith("//"):
					links[1] = "http:"+links[1]
				if links[1].endswith(".ca"):
					links[1]+="b"

				urls.append(links[0])
				urls.append(links[1])

			else:
				urls.append(link)
			i+=len("_http")

	return urls

if __name__ == "__main__":
	starting_time = time.time()
	s = requests.Session()
	links = Soup(s.get("https://sites.google.com/site/lsw2uy2kjx/navcore_tomtom").text, "html.parser").find_all("a")

	cleared_urls = []
	for link in links:
		if link.text.endswith(".cab"):
			file = link.text.rsplit('/',1)[-1]
			if os.path.exists(file):
				print("Skipping {}, already downloaded.".format(file))
				continue

			print("Added {} to downloads table.".format(file))
			cleared_urls.append(link.text)

	files_to_download = cleared_urls + resolve_blogspot()

	if len(files_to_download) >= 8: # downloading 8 files at a time, don't know what value is best but to much could cause errors because system opens to many file handlers
		thread_count = 8
	else:
		thread_count = len(files_to_download)
	print("Downloading {} TomTom firmwares...".format(len(files_to_download)))

	# Make sure firmware folder exists
	try:
		if not os.path.exists("firmware"):
			os.mkdir("firmware");
	except OSError:
		print ("Could not create firmware directory")

	results = ThreadPool(thread_count ).imap_unordered(download_file, files_to_download)

	bad_requests = 0

	for r in results:
		if r == False:
			bad_requests = bad_requests + 1
		pass
	
	print("Finished in {} seconds with {} bad requests.".format(str(time.time() - starting_time), bad_requests))
	pass




