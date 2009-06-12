import sys
import os

from plugin import Plugin

class TestPlugin (Plugin):
  def __init__ (self):
    self.data = None
    self.out = {}
  def download (self, api, args):
    if (args and "id" in args):
      self.data = api.users.show(id=args["id"])
    else:
      raise Exception("The User ID is needed for this plugin")
  def parse (self):
    self.out["Real name"] = self.data["name"]
    self.out["Username"] = self.data["screen_name"]
    self.out["Description"] = self.data["description"]
    self.out["Profile Creation date"] = self.data["created_at"]
    self.out["User ID"] = repr(self.data["id"])
    self.out["Followers"] = repr(self.data["followers_count"])
    self.out["Friends"] = repr(self.data["friends_count"])
    self.out["Location"] = self.data["location"]
    self.out["Image"] = self.data["profile_image_url"]
    self.out["Messages"] = repr(self.data["statuses_count"])
    self.out["Time Zone"] = self.data["time_zone"]
    self.out["Homepage"] = self.data["url"]

  def output (self):
    ret = ""
    for v in self.out:
      ret += v + ": " + self.out[v] + "\n"
    return ret
