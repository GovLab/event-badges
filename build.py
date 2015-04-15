import staticjinja
import os
import json
import yaml
import sys
from slugify import slugify
from dateutil.parser import parse

# We define constants for the deployment.
cwd = os.getcwd()
searchpath  = os.path.join(cwd, "templates")
outputpath  = os.path.join(cwd, "site")


# We load the data we want to use in the templates.
#BADGES    = yaml.load(open('data/badges.yaml'))

SECTOR_MAPPING = { 'Government': 'gov',
'Business': 'com',
'Nonprofit': 'org',
'Academia': 'edu' }

def getSector(str):
	if str in SECTOR_MAPPING:
		return SECTOR_MAPPING[str]
	else:
		return ''

import csv

BADGES = []
with open('data/__badges2.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		(fname,lname,org,title,workshop,subsector,email,tbd,speaker) = row
		BADGES.append( { 'fname': fname,
			'lname': lname,
			'org': org,
			'title': title,
			'sector': getSector(subsector),
			'job': title,
			'field': workshop,
			'speaker': speaker })

BADGES = sorted(BADGES, key=lambda x:x['lname'])

for sector in ['gov', 'edu', 'com', 'org']:
	for i in range(1,6):
		BADGES.append( { 'fname': '',
			'lname': '',
			'org': '',
			'title': '',
			'sector': sector,
			'job': '',
			'field': 'TBD',
			'speaker': '' })

def loadAcademyData():
	return { 'badges': BADGES,
					 'resources': None }

site = staticjinja.make_site(
	searchpath=searchpath,
	outpath=outputpath,
	staticpaths=['static', '../data'],
	contexts=[(r'.*.html', loadAcademyData),]
	)
site.render(use_reloader=True)