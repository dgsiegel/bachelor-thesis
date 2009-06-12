import sys
import os

from plugin import Plugin
from twitterapi import TwitterAPI, dump

class TestPlugin (Plugin):
  def __init__ (self):
    self.data = None
  def download (self, api, args):
    if (args and "id" in args):
      print "args with id"
    else:
      print "args without id"
  def parse (self):
    print "parsing"
    #self.data = self.data['name']
  def output (self):
    print "output"
