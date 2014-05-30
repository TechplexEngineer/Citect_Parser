#! /usr/bin/python

# https://www.python.org/download/releases/2.7.6
# http://sourceforge.net/projects/dbfpy/files/dbfpy/2.2.5/

import Tkinter, Tkconstants, tkFileDialog
import sys, os
import re, glob
from dbfpy import dbf

def GetProjectDirectory():
	Tkinter.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	folder = tkFileDialog.askdirectory() # show an "Open" dialog box and return the path to the selected file

	if len(folder) < 3:
		raise Exception("No directory specified in GUI")
	return folder

def getAlarms(folder):
	# Get Alarms
	# anaalm.dbf
	# digalm.dbf
	# hardalm.dbf
	# hresalm.dbf
	# advalm.dbf
	# *alm.dbf

	alarms = dict()

	# pat = re.compile(r'^(ana|dig|hard|hres|adv)alm\.dbf$',re.IGNORECASE)
	# for item in os.listdir(folder):
	# 	if pat.match(item):
	# 		alarmfiles.append(item)
	alarmfiles = glob.glob(os.path.join(folder,'*alm.dbf'))
	print "Found {0} alarm files.\n".format(len(alarmfiles))


	for almType in alarmfiles:

		db = dbf.Dbf(almType, new=False)

		alarms[almType] = []

		for rec in db:
			alarms[almType].append(rec.asDict())

		print "Found {0} alarm{2} in {1}".format(len(alarms[almType]), almType, 's' if (len(alarms[almType]) == 0 or len(alarms[almType]) > 1) else '')
	print
	return alarms

def getTags(folder):
	# Get Tags
	# variable.dbf
	tags = list()

	tagfiles = glob.glob(os.path.join(folder,'variable.dbf'))
	print "Found {0} tag files.\n".format(len(tagfiles))

	for tagfile in tagfiles:
		db = dbf.Dbf(tagfile, new=False)
		for rec in db:
			tags.append(rec.asDict())
		print "Found {0} tag{2} in {1}".format(len(tags), tagfile, 's' if (len(tags) == 0 or len(tags) > 1) else '')
	return tags

def listPages(folder, includePath=True):
	# *.rdb files whose name starts with an underscore don't seem to directly map to pages
	# PageMenu.RDB and !Startup.RDB don't seem to map to pages in Citect
	pages = list()

	files = glob.glob(os.path.join(folder,'*.rdb'))

	for page in files:
		# If the first character of the filename starts with an underscore don't add it to the list of pages
		if os.path.basename(page)[0] == '_':
			continue

		if includePath:
			pages.append(page)
		else:
			# print os.path.basename(page)
			pages.append(os.path.basename(page))
	return pages

# http://stackoverflow.com/a/17197027
def strings(filename, min=4):
	import string
	with open(filename, "rb") as f:
		result = ""
		for c in f.read():
			if c in string.printable:
				result += c
				continue
			if len(result) >= min:
				yield result
			result = ""


# http://stackoverflow.com/a/600612
def mkdir_p(path):
	import os, errno
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise

def getCachePage(pagePath):
	mkdir_p('cache') # make the directory if it doesn't exist
	cachefile = os.path.join('.','cache', os.path.basename(pagePath))
	cachefile = os.path.abspath(cachefile)
	# check if the page is already cached # if not cache it
	if not os.path.isfile(cachefile):
		with open(cachefile, 'w+') as f:
			for line in list(strings(pagePath)):
				f.write(line)


	# return the page
	with open(cachefile) as f:
		lines = f.readlines()
		return ''.join(lines)

def isTagInPage(tag, pagePath):
	text = getCachePage(pagePath)
	return tag in text




if __name__=='__main__':
	folder = GetProjectDirectory()
	# print getAlarms(folder)
	# getTags(folder)
	pages = listPages(folder)
	tags = getTags(folder)
	# page = "C:/Users/bjbourque/Desktop/citect_project_analyzer/SAPPI_FINAL_2008_BB\EQ_IFConv.RDB"

	# print isTagInPage('IF401ORecvRetract', page)

	for page in pages:
		print "Tags on page '{0}'".format(os.path.basename(page))
		for tag in tags:
			if isTagInPage(tag['NAME'], page):
				print tag['NAME']
		print
		# sys.exit(0)

	# for page in pages:
	# 	print page
		# sys.exit(0)
