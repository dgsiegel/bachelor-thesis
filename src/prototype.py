#!/usr/bin/python

import sys
import os

from base64 import b64encode
from urllib import urlencode, quote_plus
import urllib2
import json
import time
import codecs
import webbrowser
from optparse import OptionParser

from exceptions import Exception

import markup
from markup import oneliner as e

try:
  from twitterapi import TwitterAPI, dump, TwitterAPIError
  from plugin import Plugin, init_plugin_system, find_plugins
  import conf

except ImportError:
  print "The prototype modules can not be found."
  sys.exit(1)


parser = OptionParser()
parser.add_option("-u", "--user", help="analyze a Twitter username")
parser.add_option("-k", "--keyword", help="search for a specific keyword")
parser.add_option("-l", "--location", help="search for a location")
parser.add_option("-r", "--range", help="a range in kilometers (has to be used together with the location option), e.g. 15")

(options, args) = parser.parse_args()

twitter = TwitterAPI(conf.username, conf.password)

if options.user:
  try:
    id = twitter.users.show(id=options.user, no_cache=True)
  except (TwitterAPIError, ValueError):
    print "No user named '%s' found. Running a search now." % options.user
    print "Please re-run this program, once you have found a user"
    webbrowser.open("http://search.twitter.com/search?q=\"%s\"" % quote_plus(options.user))
    sys.exit()
elif options.keyword:
  print "Running a keyword search for '%s'" % options.keyword
  print "Please re-run this program, once you have found a user"
  webbrowser.open("http://search.twitter.com/search?q=\"%s\"" % quote_plus(options.keyword))
  sys.exit()
elif options.location:
  if not options.range:
    options.range = "5"
  print "Running a location search for '%s' within %s km" % (options.location, options.range)
  print "Please re-run this program, once you have found a user"
  webbrowser.open("http://search.twitter.com/search?near=\"%s\"&within=%s&units=km"
      % (quote_plus(options.location), options.range))
  sys.exit()
elif options.range:
  print "Option range has to be used together with the location option"
  parser.print_help()
  exit(-1)
else:
  parser.print_help()
  exit(-1)


id = str(options.user)
data = {"id": id}

init_plugin_system()

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

htmlfile = "output.html"

fd = codecs.open(htmlfile, "w", encoding="utf-8")
fd.write(page())
fd.close()

webbrowser.open(htmlfile)

obj = twitter.account.rate_limit_status(no_cache=True)
dump(obj)
