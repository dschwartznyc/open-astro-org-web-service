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
from openastrochart.openAstroChart import openAstroChart

class openAstroChartFactory :
    # calculate a chart based on chart data in a dictionary and return the chart in a dictionary
    def caclulate (self, chart_data) :
        chart = openAstroChart ()
        chart.setChartData (chart_data)
        chart.calc ()
        return chart.getChart ()
    # calculate a chart based on settings in a JSON string and return the results in a JSON string
    def calculateFromToJSON (self, json_str) :
        chart = openAstroChart ()
        chart.importOACFromJSON (json_str)
        chart.calc ()
        return chart.getChartToJSON ()

# create the factory
OACF = openAstroChartFactory ()
    