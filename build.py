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

SECTOR_MAPPING = { 'Industry Professional': 'com',
	'Graduate Student': 'grad',
	'High School Student': 'highschool',
	'Undergraduate Student': 'undergrad',}

def getSector(str):
	if str in SECTOR_MAPPING:
		return SECTOR_MAPPING[str]
	else:
		return ''

import csv


BADGES = []
with open('/Users/sahuguet/Downloads/WiTNY Build-a-Thon Participants.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print(len(row))
		(timestamp, fname,	lname,	category, email, grade_level,
		xp_python, xp_APIs, xp_JavaScript, xp_nodejs, xp_HTML, xp_CPP, xp_pitching, xp_project_m, xp_engineering,
		extra_info, skip, focus, employer, laptop,
		ugrad_vs_grad, which_cuny, major, ct_program, tshirt_size, dietary_restrictions, school, cs) = row
		#(ts, fname, lname, category,
		#email, school, grade_level, cs_class, undergrad_vs_grad,
		#which_cuny, cuny_major, ct_programm, professional_focus, company,
		#python_expertise, javascript_expertise, html_expertise, cpp_expertise, nodejs_expertise, api,
		#ability_pitch, ability_project_management, ability_eng,
		#will_bring_laptop, diet, t_shirt, extra_experience, one_more) = row
		BADGES.append( { 'fname': fname,
			'lname': lname,
			'org': employer,
			'cuny': which_cuny,
			'employer': employer + school + which_cuny,
			'job': '',
			'title': 'no title',
			'sector': getSector(category),})

BADGES = sorted(BADGES, key=lambda x:x['lname'])

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