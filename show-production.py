envoy_ip = '192.168.1.254'    # change this line to reflect your envoy ip
user = 'envoy'
passwd = '999999'             # change this line to reflect your envoy's password

# define a list of inverters related to their array position
# this will be different for each site and the html tables written out
# will also be different.
# the serial numbers listed below are ficticious!  Numbers were simply
# plugged into show how this works.
array_to_serial = \
[ \
# east array
'121012345678',
'121012345679',
'121012345680',
'121012345681',
'121012345682',
'121012345683',
'121012345684',
'121012345685',
'121012345686',
'121112345687',
'121012345688',
'121312345678',
# center array
'121012345689',
'121012345690',
'121012345691',
'121012345692',
'121012345693',
'121012345694',
'121012345695',
'121012345696',
'121712345678',
'121012345697',
'121012345698',
'121712345679',
# west array
'121312345679',
'121312345680',
'121312345681',
'121312345682',
'121312345683', 
'121312345684', 
'121312345685',
'121312345686',
'121312345687',
'121312345688',
'121312345689',
'121312345690' \
]

# Defines an array of tuples that defines the name of each array and the number of panels in each one
# Panels in the array_to_serial data structure above should be listed in the same order they are grouped
# in the list of array location tuples below. Each tuple should be formatted as:
# ("Array Name", Number of panels in the array)
array_to_loc = \
[ \
  ("East Array",12),
  ("Center Array",12),
  ("West Array",12) \
]

#--------------------------------------------------------------------------------------------------------------------------------------# 
# Name:               show-production.py
#
# Purpose:            Read Envoy inverter solar production data directly from the #                     Envoy.  
#                           Data is displayed in a Web browser window.
#                           A temp file named: envoy-production.html is used 
#                           for the display
#                           and may be deleted.
#                           Digest authentication must be used to log into the envoy. 
#                           JSON data is parsed using the standard Python JSON #                           module, and
#                           Python list and dictionary objects.
#
#  Notes:               The Envoy IP address can be entered in the top line of the program
#                            The Envoy username 'envoy' should not need to be changed!
#                            The password to log in locally to the envoy is the last 6 digits of the
#                                 envoy serial number -- unless changed.
#
# Requires:             Python Version 3.0 or later  (tested on version 3.5)
# Author:                Ken Clifton
# Web site:              http://www.kenclifton.com
# Tested on:            Linux and Windows
#
# Created:               5/30/2017
#--------------------------------------------------------------------------------------------------------------------------------------#
# define other lists as same length as the list of inverters
current_power = [None] * len(array_to_serial)
max_power = [None]  * len(array_to_serial)
last_report = [None]  * len(array_to_serial)

table_index = 0  # this index is incremented inside the writePVArrayTable() function

import datetime
from math import ceil

def convertJsonDatetoPython( jsonDate ):
	# convert installed date from JSON seconds value to Python date format
	java_timestamp = jsonDate
	seconds = java_timestamp
	python_date = datetime.datetime.fromtimestamp(seconds)
	return python_date
	# end of  convertJsonDatetoPython() function
	# -----------------------------------------------------------------

def writePVArrayTable( outFile, size ):
	# writes out a table for 12 inverters in a 4 x 3 table using the table_index which is incremented inside this function
	global table_index  # make table_index writable 
	outFile.write("<table border='1' cellpadding='2'>" + "\n")
	outFile.write("<tbody>" + "\n")

        # table size
	num_cols = 4
	num_rows = ceil(size/num_cols)
	max_index = table_index + size

	for row in range(num_rows):
		outFile.write("<tr>" + "\n")

		for column in range(num_cols):

                        # if we have reached our max_index, continue
			if table_index >= max_index:
				continue

			# derive values to color the table cells
			try:
				blue_value = current_power[table_index]
			except IndexError:
				continue

			green_value = blue_value - 30
			if green_value < 0:
				green_value = 0
			rgb = 'rgb(0, ' + str(green_value) + ', ' + str(blue_value) + ');'
			outFile.write("<td style='vertical-align: top; width: 10vw; height: 150px; background-color: " + \
			rgb + " font-size: 1em; font-weight: bold; color: white;'>" + "\n" )
			
			power_color = "#00ff00"
			if current_power[table_index] >= max_power[table_index]:
				power_color = "#b30000"

			outFile.write( array_to_serial[table_index] + '<br>' +"\n")
			outFile.write( '<br>' +"\n")
			outFile.write('Current : <font color='+power_color+'>' + str(current_power[table_index]) + 'w</font><br>' +"\n")
			outFile.write('Max: ' +  str(max_power[table_index]) + 'w<br>' +"\n")
			outFile.write('Last Rpt: ' + last_report[table_index] + '<br>' +"\n")
			outFile.write("</td>" + "\n" )
			table_index = table_index + 1
			# end of the column
		
		# write out the end of the row
		outFile.write("</tr>" + "\n")
	
	# write out the end of the table and the end of the html page       
	outFile.write("</tbody>" + "\n")
	outFile.write("</table>" + "\n")
	outFile.write( '<br>' +"\n")
	# end of  writePVArrayTable() function
	# --------------------------------------------------------


def read_envoy_data( envoy_ip_addr, username, password ):
	# function read_envoy_data gets the json data from the envoy
	# production readings require digest authentication

	import urllib.request
	import json
	import socket
	
	socket.setdefaulttimeout(30)

	productionTableString = '/api/v1/production/inverters/' 

	# build the full url to get the production Table
	url = 'http://' + envoy_ip_addr + productionTableString
	
	# https://docs.python.org/3.4/howto/urllib2.html#id5
	#
	# If you would like to request Authorization header for basic Authentication,
	# replace HTTPDigestAuthHandler object to HTTPBasicAuthHandler
	passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
	passman.add_password(None, url, username, password)
	#authhandler = urllib.request.HTTPBasicAuthHandler(passman)
	authhandler = urllib.request.HTTPDigestAuthHandler(passman)
	
	opener = urllib.request.build_opener(authhandler)
	urllib.request.install_opener(opener)
	
	try:
		response = urllib.request.urlopen(url,  timeout=30)
	except urllib.error.URLError as error:
		print('Data was not retrieved because error: {}\nURL: {}'.format(error.reason, url) )
		quit()  # exit the script - some error happened
	except socket.timeout:
		print('Connection to {} timed out, '.format( url))
		quit()  # exit the script - cannot connect
	
	try:
		# Convert bytes to string type and string type to dict
		string = response.read().decode('utf-8')
	except urllib.error.URLError as error:
		print('Reading of data stopped because error:{}\nURL: {}'.format(error.reason, url) )
		response.close()  # close the connection on error
		quit()  # exit the script - some error happened
	except socket.timeout:
		print('Reading data at {} had a socket timeout getting inventory, '.format( url))
		response.close()  # close the connection on error
		quit()  # exit the script - read data timeout
		
	json_data = json.loads(string)
	
	#close the open response object
	#urllib.request.urlcleanup()
	response.close()
	return json_data
	# end of function read_envoy_data
	# ------------------------------------------------ 

def main():    
	# call function read event log data from the envoy
	data = read_envoy_data(envoy_ip, user, passwd )
	
	# the following loop loads the lists with values from the Envoy
	for item in data:
		if item['serialNumber'] in array_to_serial:
			position = array_to_serial.index(item['serialNumber'])
			current_power[position] = item['lastReportWatts']
			max_power[position]= item['maxReportWatts']
			lastReportDate = convertJsonDatetoPython(item['lastReportDate'])
			last_report[position] =  lastReportDate.strftime('%Y-%m-%d %I:%M %p')
		else:
			print("Need to Add module: " + item['serialNumber'] + " to array_to_serial in correct location or have Enphase delete it!")
	# end of retrieval of data and loading of lists

	# the following code writes out a web page with the information from the lists
	# open the new html file to eventually display
	outFileRef = open("envoy-production.html","w")

	outFileRef.write("<html>" + "\n")
	outFileRef.write("<head>" + "\n")
	outFileRef.write("</head>" + "\n")
	outFileRef.write("<body>" + "\n")

	global table_index   # make table_index variable writeable from all functions
	table_index = 0  # this index is incremented inside the writePVArrayTable() function

	for name,size in array_to_loc:
		outFileRef.write("<p style='font-size:1.5em'><b>"+name+"</b></p>" + "\n")
		writePVArrayTable( outFileRef, size )

	# write out end of the web page
	outFileRef.write("</body>"+ "\n")
	outFileRef.write("</html>")
	outFileRef.close()

	# code to open the html just created in the default Web browser.
	import urllib
	import webbrowser
	import os.path
	full_path = os.path.join( os.getcwd(), 'envoy-production.html' )
	fileURL = "file://" + urllib.request.pathname2url(full_path)
	webbrowser.open(fileURL)
	# end of main() function
	# ----------------------------------

# call main() function to run program    
main()
