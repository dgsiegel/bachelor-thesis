# -*- coding: utf-8 -*-

# python twitter tools (http://mike.verdone.ca/twitter/) by
# Mike Verdone was used as a reference for this API, thanks!
# python twitter tools is licenced under the MIT licence

import sys
import os

from base64 import b64encode
from urllib import urlencode
from hashlib import md5
import urllib2
import json
import tempfile
import time
import codecs
import pickle

from exceptions import Exception

DEFAULT_CACHE_TIMEOUT = 3600

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


def dump(obj):
  print json.dumps(obj, sort_keys=True, indent=2)


class TwitterAPICall(object):

  def __init__(self, cache, user=None, password=None,
               domain="twitter.com", uri=""):
    self.user = user
    self.password = password
    self.domain = domain
    self.uri = uri
    self.format = "json"
    self.cache = cache

  def __getattr__(self, arg):
    try:
      return object.__getattr__(self, arg)
    except AttributeError:
      return TwitterAPICall(self.cache, self.user, self.password, self.domain,
                            self.uri + "/" + arg)

  def __call__(self, **args):
    method = "GET"
    for action in TWITTER_API_METHODS_POST:
      if self.uri.endswith(action):
        method = "POST"
        break

    uri = self.uri
    if "id" in args:
      uri += "/%s" % args.pop("id")

    no_cache = False
    if "no_cache" in args:
      if args["no_cache"]:
        no_cache = True
      args.pop("no_cache")

    headers = {}
    query = ""
    post = None

    if method == "GET":
      if args:
        query = "?%s" % urlencode(args.items())
    else:
      post = urlencode(args.items())

    if self.username:
      headers["Authorization"] = "Basic " + b64encode("%s:%s" % (self.user, self.password))

    cache_uri = "%s.%s%s" % (uri, self.format, query)

    cached_item = False
    if not no_cache:
      cached_item = self.cache.is_cached(cache_uri)

    if cached_item:
      ttl = round(self.cache.timeout - (time.time() - self.cache._get_cache_time(cache_uri)))
      print "cache hit for: " + cache_uri + " (TTL: %i minutes, %i seconds)" % divmod(ttl, 60)
      return self.cache.get(cache_uri)
    else:
      print "cache miss for: " + cache_uri

      rate_status_uri = "twitter.com/account/rate_limit_status"
      rate_status_url = urllib2.Request("http://%s.%s" % (rate_status_uri,
                                        self.format), None, headers)
      try:
        handle = urllib2.urlopen(rate_status_url)
        rate_status_result = json.loads(handle.read())
      except urllib2.HTTPError, e:
        raise TwitterAPIError("HTTP response code %i on URL: %s.%s\ndetails: %s"
                              % (e.code, rate_status_uri, self.format, e.fp.read()))
      if rate_status_result["remaining_hits"] <= 0:
        print "No API requests left until " + rate_status_result["reset_time"]
        return

      url = urllib2.Request("http://%s%s.%s%s" % (self.domain, uri,
                            self.format, query), post, headers)
      try:
        handle = urllib2.urlopen(url)
        result = json.loads(handle.read())
        if not no_cache:
          self.cache.set(cache_uri, result)
        return result
      except urllib2.HTTPError, e:

        raise TwitterAPIError("HTTP response code %i on URL: %s.%s using parameters: (%s)\ndetails: %s"
                              % (e.code, uri, self.format,
                              urlencode(args.items()), e.fp.read()))


class TwitterAPIError(Exception):
  pass


class TwitterAPI(TwitterAPICall):

  def __init__(self, user=None, password=None, domain="twitter.com"):
    filecache = FileCache()
    TwitterAPICall.__init__(self, filecache, user, password, domain, "")


class FileCache(object):

  def __init__(self):
    self.timeout = DEFAULT_CACHE_TIMEOUT
    self.cache_dir = "cache"
    if not os.path.exists(self.cache_dir):
      os.mkdir(self.cache_dir)

  def is_cached(self, key):
    path = self._get_key_path(key)
    if os.path.exists(path):
      last_cached = self._get_cache_time(key)
      if not last_cached or time.time() >= last_cached + self.timeout:
        return False
      else:
        return True
    else:
      return False

  def get(self, key):
    path = self._get_key_path(key)
    if os.path.exists(path):
      last_cached = self._get_cache_time(key)

      if not last_cached or time.time() >= last_cached + self.timeout:
        return None
      else:
        file = open(path, "r")
        ret = pickle.load(file)
        file.close()
        return ret
    else:

      return None

  def set(self, key, data):
    path = self._get_key_path(key)

    (temp_fd, temp_path) = tempfile.mkstemp()
    temp_fp = os.fdopen(temp_fd, "w")
    pickle.dump(data, temp_fp)
    temp_fp.close()

    if os.path.exists(path):
      os.remove(path)
    os.rename(temp_path, path)

  def _get_key_path(self, key):
    try:
      hashed_key = md5(key).hexdigest()
    except TypeError:
      hashed_key = md5.new(key).hexdigest()

    return os.path.join(self.cache_dir, hashed_key)

  def _get_cache_time(self, key):
    path = self._get_key_path(key)
    if os.path.exists(path):
      return os.path.getmtime(path)
    else:
      return None


