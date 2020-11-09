#!/usr/bin/env python3
import os
import sys
import requests

try:
	from bs4 import BeautifulSoup as Soup
except BaseException as exc:
	print("You need the bs4 library, please install it with pip3!")
	exit(1)

import re
s = requests.Session()
links = Soup(s.get("https://sites.google.com/site/lsw2uy2kjx/navcore_tomtom").text, "html.parser").find_all("a")

print("Downloading {} TomTom firmwares...".format(len(links)))
for link in links:
	if link.text.endswith(".cab"):
		file = link.text.rsplit('/',1)[-1]
		if os.path.exists(file):
			print("Skipping {}, already downloaded.".format(file))
			continue
		print("Downloading {}...".format(file))
		contents = s.get(link.text)

		if contents.status_code == 404 or "Not found" in contents.content:
			print("Not found, skipping...")
			continue
		contents = contents.content

		with open(file, "wb+") as f:
			f.write(contents)
		print("Done.")


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

links = urls
print("Downloading {} TomTom firmwares...".format(len(links)))
for link in links:
	if link.endswith(".cab"):
		file = link.rsplit('/',1)[-1]
		if os.path.exists(file):
			print("Skipping {}, already downloaded.".format(file))
			continue

		print("Downloading {}...".format(file))
		contents = s.get(link)
		if contents.status_code == 404 or "Not found" in contents:
			print("Not found, skipping...")
			continue
		contents = contents.content
		with open(file, "wb+") as f:
			f.write(contents)
		print("Done.")
