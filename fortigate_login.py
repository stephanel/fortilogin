#!/usr/bin/env python
import sys
import httplib
import urllib
from urlparse import urlparse

if len(sys.argv) < 3:
	print "Usage : " + __file__+ " username password"	
	exit()

username = sys.argv[1]
password = sys.argv[2]

# Initial request to know if I'm behind a Fortinet captive portal
# I'm using httplib to detect and avoid the automatic redirection performed by urllib
conn = httplib.HTTPConnection('icanhazip.com')
conn.request('GET', '/')
rep = conn.getresponse()

# The captive portal responds with HTTP rep code 303
if rep.status == 303:
	# So I can extract the magic token embedded in the value of the Location header.
	# This value is something like this : http://10.151.0.1:1000/fgtauth?0004610d63757532
	
	locationUrl = rep.getheader('Location')		
	portalUrl = urlparse(locationUrl)
	magic = portalUrl.query

	postUrl = portalUrl.scheme + "://" + portalUrl.netloc + "/"

	print "Not authenticated !"
	print "Redirected to " + locationUrl
	print "------"
	print "Captive portal url : " + postUrl 
	print "Magic token : " + magic
	print "------"
	
	print "Authenticating as " + username
	
	rep = urllib.urlopen(locationUrl)	
	print "Step 1 : " + str(rep.getcode())

	params = urllib.urlencode({'4Tredir': 'http://icanhazip.com', 'magic': magic, 'answer': 1})
	rep = urllib.urlopen(postUrl, params)
	print "Step 2 : " + str(rep.getcode())

	params = urllib.urlencode({'4Tredir': 'http://icanhazip.com', 'magic': magic, 'username': username, 'password': password})
	rep = urllib.urlopen(postUrl, params)
	print "Step 3 : " + str(rep.getcode())
	print "Final response (should be your public IP address) : " + rep.read()
else:
	print "Already authenticated"
