#!/usr/bin/python

import sys
import os
#sys.path.append(os.getcwd()+ "/")

from base64 import b64encode
from urllib import urlencode
import urllib2
import json
import time
import codecs
import webbrowser

from exceptions import Exception

import markup
from markup import oneliner as e

try:
  from twitterapi import TwitterAPI, dump
  from plugin import Plugin, init_plugin_system, find_plugins
  import conf

except ImportError:
  print "The prototype modules can not be found."
  sys.exit(1)

twitter = TwitterAPI(conf.username, conf.password)

init_plugin_system()

id = "furukama"
data = {"id": id}
#data = None

date = "Created on %s" % time.asctime()
title = "Fact Sheet"

page = markup.page()
page.init(css="style.css", title=title + " (%s)" % date)
page.h1(title)
page.h5(date)

page.div(class_="fact_sheet")
for plugin in find_plugins():
  plugin.download(twitter, data)
  plugin.parse()

  page.div(class_="plugin " + str(plugin.__module__))
  plugin.output(page)
  page.div.close()

page.div.close()

#htmlfile=tempfile.mktemp("foo.html")
htmlfile = "output.html"

#fd=open(htmlfile, "w", "utf-8")
fd = codecs.open(htmlfile, "w", encoding="utf-8")
fd.write(page())
fd.close()

webbrowser.open(htmlfile)

obj = twitter.account.rate_limit_status(no_cache=True)
dump(obj)
#id = twitter.users.show(id="twitter")["id"]
#u = twitter.statuses.show(id=1472669360)
#
#dump(u)
