# python twitter tools (http://mike.verdone.ca/twitter/) by
# Mike Verdone was used as a reference for this API, thanks!
# python twitter tools is licenced under the MIT licence

import sys
import os

from base64 import b64encode
from urllib import urlencode
import urllib2
import json

from exceptions import Exception

cache = {}

TWITTER_API_METHODS_POST = [
    "create",       # in blocks/
                    #    favorites/
                    #    friendships/

    "destroy",      # in blocks/
                    #    direct_messages/
                    #    favorites/
                    #    friendships/
                    #    statuses/

    "follow",       # in notifications
    "leave",

    "new",          # in direct_messages/

    "update",       # in statuses/

    "end_session",  # in account/
    "update_delivery_device",
    "update_profile",
    "update_profile_background_image",
    "update_profile_colors",
    "update_profile_image",
]

def dump (obj):
  print json.dumps(obj, sort_keys=True, indent=2)

class TwitterAPICall (object):
  def __init__ (self, user=None, password=None, domain="twitter.com", uri=""):
    self.user = user
    self.password = password
    self.domain = domain
    self.uri = uri
    self.format = "json"

  def __getattr__ (self, arg):
    try:
      return object.__getattr__ (self, arg)
    except AttributeError:
      return TwitterAPICall (self.user, self.password, self.domain,
                             self.uri + "/" + arg)
  def __call__ (self, **args):
    method = "GET"
    for action in TWITTER_API_METHODS_POST:
        if self.uri.endswith (action):
            method = "POST"
            break

    uri = self.uri
    if ("id" in args):
      uri += "/%s" % args.pop("id")

    headers = {}
    query = ""
    post = None

    if (method == "GET"):
      if (args):
        query = "?%s" %(urlencode(args.items()))
    else:
      post = urlencode(args.items())

    if (self.username):
      headers["Authorization"] = "Basic " + b64encode ("%s:%s" %(self.user, self.password))

    cache_uri = "%s.%s%s" %(uri, self.format, query)
    if cache_uri in cache:
      return cache[cache_uri]
    else:
      url = urllib2.Request ("http://%s%s.%s%s" %(self.domain, uri, self.format, query),
                             post, headers)
      try:
        handle = urllib2.urlopen(url)
        result = json.loads(handle.read())
        cache[cache_uri] = result
        return result

      except urllib2.HTTPError, e:
        raise TwitterAPIError ("HTTP response code %i on URL: %s.%s using parameters: (%s)\ndetails: %s"
                            %(e.code, uri, self.format, urlencode(args.items()), e.fp.read()))

class TwitterAPIError (Exception):
  pass

class TwitterAPI (TwitterAPICall):
  def __init__ (self, user=None, password=None, domain="twitter.com"):
    TwitterAPICall.__init__(self, user, password, domain, "")

