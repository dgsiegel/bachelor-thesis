import sys
import os

from plugin import Plugin
from twitterapi import TwitterAPI, dump

class TestPlugin (Plugin):
  def __init__ (self):
    self.data = None
  def download (self, api, args):
    if (args and "id" in args):
      self.data = api.users.show(id=args["id"])
    else:
      self.data = api.statuses.public_timeline()
  def parse (self):
    self.data = self.data['name']
  def output (self):
    print self.data
