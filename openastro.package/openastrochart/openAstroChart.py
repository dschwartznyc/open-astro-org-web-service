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
import datetime, math
#template processing
from string import Template
import json

import openastromod.importfile as importfile
import openastromod.swiss as ephemeris

from openastrochart.openAstroVersion import OAS, dprint

def toInt (x) :
	if (type (x) != int) :
		return (int (x))
	return x
def toFloat (x) :
	if (type (x) != float) :
		return (float (x))
	return x

#calculation class
class openAstroChart:

	def __init__(self):
		
		#get label configuration
		self.label = {'radix':'Radix','north':'North','south':'South','east':'East','west':'West'}
		
		#configuration
		self.type  = ""
		
		return	
	# convert UTC date and time to local 
	def utcToLocal(self):
		#make local time variables from global UTC
		h, m, s         = self.decHour(self.hour)
		utc             = datetime.datetime(self.year, self.month, self.day, h, m, s)
		tz              = datetime.timedelta(seconds=float(self.timezone)*float(3600))
		loc             = utc + tz
		self.year_loc   = loc.year
		self.month_loc  = loc.month
		self.day_loc    = loc.day
		self.hour_loc   = loc.hour
		self.minute_loc = loc.minute
		self.second_loc = loc.second
		#print some info
		dprint('utcToLocal: '+str(utc)+' => '+str(loc)+self.decTzStr(self.timezone))
	#floating latitude to string
	def lat2str( self, coord ):
		sign=self.label["north"]
		if coord < 0.0:
			sign=self.label["south"]
			coord = abs(coord)
		deg = int(coord)
		min = int( (float(coord) - deg) * 60 )
		sec = int( round( float( ( (float(coord) - deg) * 60 ) - min) * 60.0 ) )
		return "%s°%s'%s\" %s" % (deg,min,sec,sign)	
	#floating longitude to string
	def lon2str( self, coord ):
		sign=self.label["east"]
		if coord < 0.0:
			sign=self.label["west"]
			coord = abs(coord)
		deg = int(coord)
		min = int( (float(coord) - deg) * 60 )
		sec = int( round( float( ( (float(coord) - deg) * 60 ) - min) * 60.0 ) )
		return "%s°%s'%s\" %s" % (deg,min,sec,sign)
	#decimal hour to minutes and seconds
	def decHour( self , input ):
		hours=int(input)
		mands=(input-hours)*60.0
		mands=round(mands,5)
		minutes=int(mands)
		seconds=int(round((mands-minutes)*60))
		return [hours,minutes,seconds]	
	#join hour, minutes, seconds, timezone integere to hour float
	def decHourJoin( self , inH , inM , inS ):
		dh = float(inH)
		dm = float(inM)/60
		ds = float(inS)/3600
		output = dh + dm + ds
		return output
	#Datetime offset to float in hours	
	def offsetToTz( self, dtoffset ):
		dh = float(dtoffset.days * 24)
		sh = float(dtoffset.seconds / 3600.0)
		output = dh + sh
		return output
	#decimal timezone string
	def decTzStr( self, tz ):
		if tz > 0:
			h = int(tz)
			m = int((float(tz)-float(h))*float(60))
			return " [+%(#1)02d:%(#2)02d]" % {'#1':h,'#2':m}
		else:
			h = int(tz)
			m = int((float(tz)-float(h))*float(60))/-1
			return " [-%(#1)02d:%(#2)02d]" % {'#1':h/-1,'#2':m}
	#degree difference
	def degreeDiff( self , a , b ):
		out=float()
		if a > b:
			out=a-b
		if a < b:
			out=b-a
		if out > 180.0:
			out=360.0-out
		return out
	#decimal to degrees (a°b'c")
	def dec2deg( self , dec , type="3"):
		dec=float(dec)
		a=int(dec)
		a_new=(dec-float(a)) * 60.0
		b_rounded = int(round(a_new))
		b=int(a_new)
		c=int(round((a_new-float(b))*60.0))
		if type=="3":
			out = '%(#1)02d&#176;%(#2)02d&#39;%(#3)02d&#34;' % {'#1':a,'#2':b, '#3':c}
		elif type=="2":
			out = '%(#1)02d&#176;%(#2)02d&#39;' % {'#1':a,'#2':b_rounded}
		elif type=="1":
			out = '%(#1)02d&#176;' % {'#1':a}
		return str(out)	
	# export chart data to OAC
	def exportOAC(self,filename):
		template="""<?xml version='1.0' encoding='UTF-8'?>
					<openastrochart>
						<name>$name</name>
						<datetime>$datetime</datetime>
						<location>$location</location>
						<altitude>$altitude</altitude>
						<latitude>$latitude</latitude>
						<longitude>$longitude</longitude>
						<countrycode>$countrycode</countrycode>
						<timezone>$timezone</timezone>
						<geonameid>$geonameid</geonameid>
						<timezonestr>$timezonestr</timezonestr>
						<extra>$extra</extra>
					</openastrochart>"""
		h,m,s = self.decHour(self.hour)
		dt=datetime.datetime(self.year,self.month,self.day,h,m,s)
		substitute={}
		substitute['name']=self.name
		substitute['datetime']=dt.strftime("%Y-%m-%d %H:%M:%S")
		substitute['location']=self.location
		substitute['altitude']=self.altitude
		substitute['latitude']=self.geolat
		substitute['longitude']=self.geolon
		substitute['countrycode']=self.countrycode
		substitute['timezone']=self.timezone
		substitute['timezonestr']=self.timezonestr
		substitute['geonameid']=self.geonameid
		substitute['extra']=''
		#write the results to the template
		output=Template(template).substitute(substitute)
		f=open(filename,"w")
		f.write(output)
		f.close()
		dprint("exporting OAC: %s" % filename)
		return
	# set chart data from a dictionary
	def setChartData (self, chart_data) :
		self.name        = chart_data['name']
		self.countrycode = chart_data['countrycode']
		self.altitude    = toInt (chart_data['altitude'])
		self.geolat      = toFloat (chart_data['latitude'])
		self.geolon      = toFloat (chart_data['longitude'])
		self.timezone    = toFloat (chart_data['timezone'])
		self.geonameid   = chart_data['geonameid']
		self.timezonestr = chart_data['timezonestr']
		self.location    = chart_data['location']
		self.datetime    = chart_data['datetime']
		# year, month, day and hour are derived data from datetime (MB datetime is always UTC)
		dt               = datetime.datetime.strptime (self.datetime,"%Y-%m-%d %H:%M:%S")
		self.year        = dt.year
		self.month       = dt.month
		self.day         = dt.day
		self.hour        = self.decHourJoin (dt.hour,dt.minute,dt.second)
		return
	# export chart data to a dictionary
	def getChartData (self) :
		chart_data                = {}
		chart_data['name']        = self.name
		chart_data['datetime']    = self.datetime
		chart_data['location']    = self.location
		chart_data['altitude']    = self.altitude
		chart_data['latitude']    = self.geolat
		chart_data['longitude']   = self.geolon
		chart_data['countrycode'] = self.countrycode
		chart_data['timezone']    = self.timezone
		chart_data['geonameid']   = self.geonameid
		chart_data['timezonestr'] = self.timezonestr
		return chart_data
	# export chart to a dictionary
	def getChart(self) :
		# extract chart into dictionary
		chart                   = {}
		chart['chartData']      = self.getChartData ()
		chart['planets_sign']   = self.planets_sign.copy ()
		chart['planets_degree'] = self.planets_degree.copy ()
		chart['planets_aspect'] = self.planets_aspects.copy ()
		return chart
	# export chart to a JSON string
	def getChartToJSON (self) :
		# extract chart into JSON
		return json.dumps (self.getChart ())
	# set chart from a dictionary
	def setChart (self, chart) :
		# import chart from dictionary
		self.setChartData (chart['chartData'])
		self.planets_sign    = chart['planets_sign'].copy ()
		self.planets_degree  = chart['planets_degree'].copy ()
		self.planets_aspects = chart['planets_aspect'].copy ()
	# set chart from a JSON string
	def setChartFromJSON (self, chart_json) :	
		# import chart from JSON string
		self.setChart (json.loads (chart_json))
	# impport chart data from a JSON string
	def importOACFromJSON (self, json_str) :
		# load chart data from a JSON string
		r              = json.loads(json_str)
		self.setChartData (r)
		return
	# import chart data from a file (XML)
	def importOAC(self, filename):
		# read chart data from a file
		r              = importfile.getOAC(filename)[0]
		self.setChartData (r)
		#debug print
		dprint('importOAC: %s' % filename)
		return		
		# calculate the main body of the chart
	# calculate the chart (uses calcAspectGrid and calcElements)
	def calc (self):
		
		#empty element points
		self.fire  = 0.0
		self.earth = 0.0
		self.air   = 0.0
		self.water = 0.0
		
		#Combine module data
		if self.type == "Combine":
			#make calculations
			module_data = ephemeris.ephData(self.c_year,self.c_month,self.c_day,self.c_hour,self.c_geolon,self.c_geolat,self.c_altitude,OAS.planets,OAS.zodiac,OAS.cfg)
		
		#Solar module data
		if self.type == "Solar":
			module_data = ephemeris.ephData(self.s_year,self.s_month,self.s_day,self.s_hour,self.s_geolon,self.s_geolat,self.s_altitude,OAS.planets,OAS.zodiac,OAS.cfg)
		
		elif self.type == "SecondaryProgression":
			module_data = ephemeris.ephData(self.sp_year,self.sp_month,self.sp_day,self.sp_hour,self.sp_geolon,self.sp_geolat,self.sp_altitude,OAS.planets,OAS.zodiac,OAS.cfg,houses_override=self.houses_override)				
			
		elif self.type == "Transit" or self.type == "Composite":
			module_data = ephemeris.ephData(self.year,self.month,self.day,self.hour,self.geolon,self.geolat,self.altitude,OAS.planets,OAS.zodiac,OAS.cfg)
			t_module_data = ephemeris.ephData(self.t_year,self.t_month,self.t_day,self.t_hour,self.t_geolon,self.t_geolat,self.t_altitude,OAS.planets,OAS.zodiac,OAS.cfg)
		
		else:
			#make calculations
			module_data = ephemeris.ephData(self.year,self.month,self.day,self.hour,self.geolon,self.geolat,self.altitude,OAS.planets,OAS.zodiac,OAS.cfg)

		#Transit module data
		if self.type == "Transit" or self.type == "Composite":
			#grab transiting module data
			self.t_planets_sign       = t_module_data.planets_sign
			self.t_planets_degree     = t_module_data.planets_degree
			self.t_planets_degree_ut  = t_module_data.planets_degree_ut
			self.t_planets_retrograde = t_module_data.planets_retrograde
			self.t_houses_degree      = t_module_data.houses_degree
			self.t_houses_sign        = t_module_data.houses_sign
			self.t_houses_degree_ut   = t_module_data.houses_degree_ut
			
		#grab normal module data
		self.planets_sign             = module_data.planets_sign
		self.planets_degree           = module_data.planets_degree
		self.planets_degree_ut        = module_data.planets_degree_ut
		self.planets_retrograde       = module_data.planets_retrograde
		self.houses_degree            = module_data.houses_degree
		self.houses_sign              = module_data.houses_sign
		self.houses_degree_ut         = module_data.houses_degree_ut		
		self.lunar_phase              = module_data.lunar_phase
		
		#make composite averages
		if self.type == "Composite":
			#new houses
			asc = self.houses_degree_ut[0]
			t_asc = self.t_houses_degree_ut[0]
			for i in range(12):
				#difference in distances measured from ASC
				diff = self.houses_degree_ut[i] - asc
				if diff < 0:
					diff = diff + 360.0
				t_diff = self.t_houses_degree_ut[i] - t_asc
				if t_diff < 0:
					t_diff = t_diff + 360.0 
				newdiff = (diff + t_diff) / 2.0
				
				#new ascendant
				if asc > t_asc:
					diff = asc - t_asc
					if diff > 180:
						diff = 360.0 - diff
						nasc = asc + (diff / 2.0)
					else:
						nasc = t_asc + (diff / 2.0)
				else:
					diff = t_asc - asc
					if diff > 180:
						diff = 360.0 - diff
						nasc = t_asc + (diff / 2.0)
					else:
						nasc = asc + (diff / 2.0)
				
				#new house degrees
				self.houses_degree_ut[i] = nasc + newdiff
				if self.houses_degree_ut[i] > 360:
					self.houses_degree_ut[i] = self.houses_degree_ut[i] - 360.0 
					
				#new house sign				
				for x in range(len(OAS.zodiac)):
					deg_low=float(x*30)
					deg_high=float((x+1)*30)
					if self.houses_degree_ut[i] >= deg_low:
						if self.houses_degree_ut[i] <= deg_high:
							self.houses_sign[i]=x
							self.houses_degree[i] = self.houses_degree_ut[i] - deg_low

			#new planets
			for i in range(23):
				#difference in degrees
				p1 = self.planets_degree_ut[i]
				p2 = self.t_planets_degree_ut[i]
				if p1 > p2:
					diff = p1 - p2
					if diff > 180:
						diff = 360.0 - diff
						self.planets_degree_ut[i] = (diff / 2.0) + p1
					else:
						self.planets_degree_ut[i] = (diff / 2.0) + p2
				else:
					diff = p2 - p1
					if diff > 180:
						diff = 360.0 - diff
						self.planets_degree_ut[i] = (diff / 2.0) + p2
					else:
						self.planets_degree_ut[i] = (diff / 2.0) + p1
				
				if self.planets_degree_ut[i] > 360:
					self.planets_degree_ut[i] = self.planets_degree_ut[i] - 360.0
			
			#list index 23 is asc, 24 is Mc, 25 is Dsc, 26 is Ic
			self.planets_degree_ut[23] = self.houses_degree_ut[0]
			self.planets_degree_ut[24] = self.houses_degree_ut[9]
			self.planets_degree_ut[25] = self.houses_degree_ut[6]
			self.planets_degree_ut[26] = self.houses_degree_ut[3]
								
			#new planet signs
			for i in range(27):
				for x in range(len(OAS.zodiac)):
					deg_low=float(x*30)
					deg_high=float((x+1)*30)
					if self.planets_degree_ut[i] >= deg_low:
						if self.planets_degree_ut[i] <= deg_high:
							self.planets_sign[i]=x
							self.planets_degree[i] = self.planets_degree_ut[i] - deg_low
							self.planets_retrograde[i] = False
			
		self.calcAspectGrid ()
		self.calcElements ()
		return
	# calculate the aspect grid
	def calcAspectGrid(self) : 
		revr=list(range(len(OAS.planets)))
		revr.reverse()
		self.planets_aspects = {}
		for a in revr:
			planet_name = OAS.planets[a]['name']
			if OAS.planets[a]['visible_aspect_grid'] == 1:
				start=self.planets_degree_ut[a]
				#first planet 
				revr2=list(range(a))
				revr2.reverse()
				self.planets_aspects[planet_name] = {}
				for b in revr2:
					aspect_planet_name = OAS.planets[b]['name']
					if OAS.planets[b]['visible_aspect_grid'] == 1:
						end=self.planets_degree_ut[b]
						diff=self.degreeDiff(start,end)
						aspects_list = []
						for z in range(len(OAS.aspects)):
							if	(float(OAS.aspects[z]['degree']) - float(OAS.aspects[z]['orb']) ) <= diff <= ( float(OAS.aspects[z]['degree']) + float(OAS.aspects[z]['orb']) ) and OAS.aspects[z]['visible_grid'] == 1:
								aspects_list.append (OAS.aspects[z]['name'])
						self.planets_aspects[planet_name][aspect_planet_name] = aspects_list
	# calculate the elements of the chart
	def calcElements (self) :
		
		for i in range(len(OAS.planets)):
			#calculate element points for all planets
			ele = OAS.zodiac_element[self.planets_sign[i]]			
			if ele == "fire":
				self.fire = self.fire + OAS.planets[i]['element_points']
			elif ele == "earth":
				self.earth = self.earth + OAS.planets[i]['element_points']
			elif ele == "air":
				self.air = self.air + OAS.planets[i]['element_points']
			elif ele == "water":
				self.water = self.water + OAS.planets[i]['element_points']
		
		total             = self.fire + self.earth + self.air + self.water
		self.firePercent  = self.fire / total
		self.earthPercent = self.earth / total
		self.airPercent   = self.air / total
		self.waterPercent = self.water / total
		return
