# -*- coding: utf-8 -*-
"""
	This file is part of openastro.org.

	OpenAstro.org is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	OpenAstro.org is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with OpenAstro.org.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, gettext, os.path
import xml.etree.ElementTree as ET

DATADIR = os.path.dirname(os.path.abspath(__file__)) + '/data/'

#debug
LOCAL=False
DEBUG=False
VERSION='1.1.57'

#debug print function
def dprint(str):
	if "--debug" in sys.argv or DEBUG:
		print('%s' % str)

class openAstroStatic :

	def readCfg (self) :
		filename    = DATADIR + 'open-astro-data-cfg.xml'
		tree        = ET.parse (filename)
		root        = tree.getroot()
		cfg         = {}
		cfg_tags    = ['version', 'use_geonames.org', 'houses_system', 'language', 'postype', 'zodiactype']
		for child in root :
			if (child.tag in cfg_tags) : 
				if (child.tag == '_use_geonames.org') :
					cfg[child.tag] = int (child.text)
				else :
					cfg[child.tag] = child.text
		return cfg
	def readPlanets (self) :
		filename    = DATADIR + 'open-astro-data-planets.xml'
		tree        = ET.parse (filename)
		root        = tree.getroot()
		planets     = []
		planet_tags = ['id', 'name', 'visible', 'element_points', 'zodiac_relation', 'label', 'label_short', 'visible_aspect_line', 'visible_aspect_grid']
		if (root.tag == 'planets') :
			for child in root :
				planet = {}
				for tag in planet_tags :
					planet[tag] = child.get (tag)
					if (tag == 'visible' or tag == 'element_points' or tag == 'zodiac_relation' or 
					    tag == 'visible_aspect_line' or tag == 'visible_aspect_grid') :
						planet[tag] = int (planet[tag])
				planets.append (planet)
		return planets
	def readAspects (self) :
		filename    = DATADIR + 'open-astro-data-aspects.xml'
		tree        = ET.parse (filename)
		root        = tree.getroot()
		aspects     = []
		aspect_tags = ['degree', 'name', 'visible', 'visible_grid', 'is_major', 'is_minor', 'orb']

		if (root.tag == 'aspects') :
			for child in root :
				aspect = {}
				for tag in aspect_tags :
					aspect[tag] = child.get (tag)
					if (tag != 'name') : 
						aspect[tag] = int (child.get (tag))
				aspects.append (aspect)
		return aspects
	def __init__(self) :
		self.planets        = self.readPlanets ()
		self.aspects        = self.readAspects ()
		self.cfg            = self.readCfg ()
		self.zodiac         = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces']
		self.zodiac_short   = ['Ari','Tau','Gem','Cnc','Leo','Vir','Lib','Sco','Sgr','Cap','Aqr','Psc']
		self.zodiac_element = ['fire','earth','air','water','fire','earth','air','water','fire','earth','air','water']
		self.zodiac_planets = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'pluto', 'jupiter', 'saturn', 'uranus', 'neptune']
		self.planets_index  = {'sun' : 0, 'moon' : 1, 'mercury' : 2, 'venus' : 3, 'mars' : 4, 'pluto': 9, 'juno' : 19, 'Node' : 10, 'southNode' : 29, 'northNode' : 10, 'chiron' : 15, 'marriage' : 30}
		self.signs_index    = {'aries' : 0,'taurus' : 1,'gemini' : 2,'cancer' : 3,'leo' : 4,'virgo' : 5, 'libra' : 6, 'scorpio' : 7,
		                       'sagittarius' : 8,'capricorn' : 9, 'aquarius' : 10, 'pisces' : 11, 'Asc' : 23, 'Des' : 25}
		return

OAS = openAstroStatic ()

def lat2str (coord) :
	sign = "north"
	if coord < 0.0:
		sign = "south"
		coord = abs(coord)
	deg = int(coord)
	min = int( (float(coord) - deg) * 60 )
	sec = int( round( float( ( (float(coord) - deg) * 60 ) - min) * 60.0 ) )
	return "%s°%s'%s\" %s" % (deg,min,sec,sign)
		
def lon2str (coord):
	sign = "east"
	if coord < 0.0:
		sign = "west"
		coord = abs(coord)
	deg = int(coord)
	min = int( (float(coord) - deg) * 60 )
	sec = int( round( float( ( (float(coord) - deg) * 60 ) - min) * 60.0 ) )
	return "%s°%s'%s\" %s" % (deg,min,sec,sign)
