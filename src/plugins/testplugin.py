import sys
import os

from plugin import Plugin


class TestPlugin (Plugin):

  def __init__(self):
    self.data = None

  def download(self, api, args):
    if (args and "id" in args):
      print "args with id"
    else:
      print "args without id"

  def parse(self):
    print "parsing"

  def output(self):
    print "output"
