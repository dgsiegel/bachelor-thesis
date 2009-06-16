import sys
import os

from markup import oneliner as e

from plugin import Plugin

class UserPlugin (Plugin):
  def __init__ (self):
    self.data = None
    self.out = {}
  def download (self, api, args):
    if (args and "id" in args):
      self.data = api.users.show(id=args["id"])
    else:
      raise Exception("The User ID is needed for this plugin")
  def parse (self):
    self.out = {
      "Real name": "name",
      "Username": "screen_name",
      "Description": "description",
      "Profile Creation date": "created_at",
      "User ID": "id",
      "Followers": "followers_count",
      "Friends (Count)": "friends_count",
      "Location": "location",
      "Image": "profile_image_url",
      "Messages": "statuses_count",
      "Time Zone": "time_zone",
      "Homepage": "url",
    }
    for k, v in self.out.iteritems():
      if self.data[v] != "" and self.data[v] != None:
        self.out[k] = str(self.data[v])
      else:
        self.out[k] = "<span style=\"font-style: italic;\">none</span>"

  def output (self, page):
    page.div(class_="block_top block_user_top")
    page.img(src=self.out["Image"])
    page.div(self.out["Real name"] + " (" + self.out["Username"] + ")")
    page.div.close()

    del self.out["Real name"]
    del self.out["Image"]

    page.div(class_="clearboth")
    page.div.close()

    page.div(class_="block_user_bottom")

    for v in self.out:
      page.div(class_="block_user_entry")
      page.div(v + ":", class_="block_user_entry_key")
      page.div(self.out[v], class_="block_user_entry_value")
      page.div.close()

    page.div.close()

