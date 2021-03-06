#!/usr/bin/env python

import mechanize
import lxml.html

url = 'http://undi.info'

req = mechanize.Request(url)
resp = mechanize.urlopen(req)
html = lxml.html.parse(resp).getroot()

#State Listings
links = html.cssselect("div.negeri_nav ul li a")

state_names = []
state_slugs = []
state_plates = []

for link in links:
	state_names.append(link.text.lower())
	state_slugs.append(link.attrib.get('slug'))
	state_plates.append(link.attrib.get('plate'))

#Parliament Constituency Listings
parliament_places = []
parliament_codes = []

for state in state_slugs:
	path = "div#parl_listing div.content ul li.negeri_p_"+state+"_li a"
	links = html.cssselect(path)
	for link in links:
		parliament_places.append(link.cssselect("span.place")[0].text)
		parliament_codes.append(link.cssselect("span.code")[0].text)

url = 'http://undi.info/ajax.php?a=info&c='

for parliament_code in parliament_codes:
	url_ajax = url+parliament_code
	req = mechanize.Request(url_ajax)
	resp = mechanize.urlopen(req)
	html = lxml.html.parse(resp).getroot()
	#years = html.cssselect("div.info_body div.year")
	
	for year_code in ['2008','2004']:
		path = "div.year_"+year_code+" div.party_list"
		party_lists = html.cssselect(path)
		
		for party_list in party_lists:
			votes = party_list.cssselect("div.votes")[0].text
			party_name = party_list.cssselect("div.party_name")[0].text
			candidate_name = party_list.cssselect("div.cand_name")[0].text
			votes = votes.replace(',','')
			if candidate_name == 'Uncontested' or party_name is None:
				party_name = 'None';
			print parliament_code+','+year_code+','+candidate_name+','+party_name+','+votes
	print ''
