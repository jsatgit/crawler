from bs4 import BeautifulSoup
import requests
import urllib2
import random
import re
import sys
import urlparse

visited = set()
stack = []
pat = "https?://.*(?!\.(pdf|docx|doc|jpg|png|gif|mp3|wav|avi|mp4))$"
	
def visit(url):
	try:
		res = urllib2.urlopen(url).read()
		soup = BeautifulSoup(res)

		res = 0

		if url not in visited:
			print url
			visited.add(url)
			stack.append(url)
		return soup
	except:
		return 0

def getChildren(soup):
	anchors = soup.find_all('a', href=True)
	unvisited = []
	for anchor in anchors:
		link = anchor['href']
		if re.match(pat, link) and link not in visited:
			unvisited.append(link)
	if unvisited:
		return unvisited
	else:
		return 0		

def backtrack():
	stack.pop()
	if len(stack):
		print ""
		print "========== Backtracking =========="
		print ""
		return stack[-1]
	else:
		return 0

def main():
	if len(sys.argv) != 2:
		print "Please input url."
	initUrl = sys.argv[1]

	soup = visit(initUrl)
	if not soup:
		print "Cannot access first page."
		return
	
	children = getChildren(soup)
	if not children:
		print "First page does not have links."
		return
	
	url = random.choice(children)

	while len(stack) > 0:
		soup = visit(url)		
		if soup:
			children = getChildren(soup)
			if children:
				url = random.choice(children)
			else:
				url = backtrack()
				if not url:
					break
		else:
			url = backtrack()
			if not url:
				break
	print "All webpages have been traversed!"

if __name__ == '__main__':
	main()
