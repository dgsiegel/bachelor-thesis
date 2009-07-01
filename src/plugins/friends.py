import sys
import os
import string
import re

from markup import oneliner as e

from plugin import Plugin
from markup import escape
from util import bar_graph

import conf

class RepliesPlugin(Plugin):

  def __init__(self):
    self.data = None
    self.friends = {}
    self.followers = {}
    self.mutual = []
    self.out = {
      "Description": "description",
      "Profile Creation date": "created_at",
      "User ID": "id",
      "Followers": "followers_count",
      "Friends (Count)": "friends_count",
      "Location": "location",
      "Messages": "statuses_count",
      "Time Zone": "time_zone",
      "Homepage": "url",
      "Twitter": "screen_name",
    }

  def download(self, api, args):
    if (args and "id" in args):
      i = 1
      tmp = api.statuses.friends(id=args["id"], page=i)
      self.friends = tmp

      while tmp:
        i += 1
        tmp = api.statuses.friends(id=args["id"], page=i)
        if tmp:
          self.friends.extend(tmp)

      i = 1
      tmp = api.statuses.followers(id=args["id"], page=i)
      self.followers = tmp

      while tmp:
        i += 1
        tmp = api.statuses.followers(id=args["id"], page=i)
        if tmp:
          self.followers.extend(tmp)
    else:
      raise Exception("The User ID is needed for this plugin")

  def parse(self):
    for item in self.friends:
      if item in self.followers:
        self.mutual.append(item)

  def output(self, page):
    page.div(class_="block_top block_friends_top")
    page.div("List of friends")
    page.div.close()

    page.div(class_="clearboth")
    page.div.close()

    page.div(class_="block_friends_bottom")

    for v in self.mutual:
      page.div(class_="block_friends_entry")
      page.img(src=v["profile_image_url"])
      page.div(escape(str(v["name"])).encode("ascii", "xmlcharrefreplace") + " (" + v["screen_name"] + ")", class_="block_friends_entry_name")

      page.div(class_="clearboth")
      page.div.close()

      for item in self.out:
        page.div(item + ":", class_="block_friends_entry_key")
        if item == "Twitter":
          page.div("http://www.twitter.com/" + str(v[self.out[item]]), class_="block_friends_entry_value")
        else:
          if v[self.out[item]] != "" and v[self.out[item]] != None:
            page.div(escape(str(v[self.out[item]])).encode("ascii", "xmlcharrefreplace"), class_="block_friends_entry_value")
          else:
            page.div("<span style=\"font-style: italic;\">none</span>", class_="block_friends_entry_value")

      page.div.close()
      page.div(class_="clearboth")
      page.div.close()

    page.div.close()
