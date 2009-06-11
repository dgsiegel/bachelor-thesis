#!/usr/bin/python

import sys
import os
#sys.path.append(os.getcwd()+ '/')

from base64 import b64encode
from urllib import urlencode
import urllib2
import json

from exceptions import Exception

try:
  from api import TwitterAPI, dump
  from plugin import Plugin, init_plugin_system, find_plugins
except ImportError:
  print "The prototype modules can not be found."
  sys.exit(1)

twitter = TwitterAPI("petersample", "petersample")

init_plugin_system()

data = {"id": "twitter"}
#data = None

for plugin in find_plugins():
  plugin.download (twitter, None)


#id = twitter.users.show(id="twitter")['id']
#u = twitter.statuses.show(id=1472669360)
#
#dump(u)
