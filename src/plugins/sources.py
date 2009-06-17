import sys
import os
import string

from pylab import *

from markup import oneliner as e

from plugin import Plugin
from markup import escape
from util import strip_html_tags, bar_graph

class SourcesPlugin (Plugin):
  def __init__ (self):
    self.data = None
    self.out = {}
    self.count = 0
  def download (self, api, args):
    if (args and "id" in args):
      i = 1

      # FIXME: keep attention on the max limit
      tmp = api.statuses.user_timeline(id=args["id"], count=200, page=i)
      self.data = tmp

      while tmp:
        i += 1
        tmp = api.statuses.user_timeline(id=args["id"], count=200, page=i)
        if tmp:
          self.data.extend(tmp)

    else:
      raise Exception("The User ID is needed for this plugin")
  def parse (self):

    self.count = self.data[0]["user"]["statuses_count"]
    for v in self.data:
      src = str(strip_html_tags(v["source"]))

      if src not in self.out:
        self.out[src] = 1
      else:
        self.out[src] += 1

  def output (self, page):
    page.div(class_="block_top block_sources_top")
    page.div("Twitter Input Sources")
    page.div.close()

    page.div(class_="clearboth")
    page.div.close()

    page.div(class_="block_sources_bottom")

    bar_graph(self.out, output_name="figures/inputsources.png")
    page.img(src="figures/inputsources.png", width="720px")
    page.div.close()
