#usr/bin/python3
# this is the master program for the comfysetup package

import urllib2


def netcheck():
    try:
        urllib.request.urlopen("https://github.com", timeout=1)
        return True
    except urllib.request.URLError:
        return False

def Update():
	response = urllib2.urlopen('http://www.example.com/')
	html = response.read()
	print(html)


network = netcheck()

if network == true :
	update()
else :
	print ("no internet bro")
