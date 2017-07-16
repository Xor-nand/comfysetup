#usr/bin/python3
# this is the master program for the comfysetup package


import urllib.request
import filecmp

UPDATE_LIST = "/tmp/comfysetup_new_list.txt"
URL_LIST = "https://raw.githubusercontent.com/tommasoascari/comfysetup/master/list.txt"

def compare():
	compared = filecmp.cmp('list.txt', UPDATE_LIST)
	return compared

def netcheck():
    try:
        urllib.request.urlopen("https://github.com", timeout=1)
        return True
    except urllib.request.URLError:
        return False

def updateList():
	print ("ima working on this")

def update():
	print (" > Looking for updates ...")
	filename, headers = urllib.request.urlretrieve(URL_LIST, filename=UPDATE_LIST)
	check = compare()
	if check == True:
		print (' > program mirrorlist is up to date')
	elif check == False:
		print (" > Found updates for the program mirrorlist")
		YN = input(" > Do you want to upgrade the list ? (Y/N) - ")
		if YN == "y":
			updateList()
		else :
			print ("list not updated")
			return 0

network = netcheck()

if network == True :
	update()
else :
	print ("no internet bro")
