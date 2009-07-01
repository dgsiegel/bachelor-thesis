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
    self.out = {}
    self.keywords = conf.keywords

  def download(self, api, args):
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

  def parse(self):
    from twitterapi import dump
    for v in self.data:
      if v["in_reply_to_screen_name"] != None:
        if v["in_reply_to_screen_name"] not in self.out:
          self.out[str(v["in_reply_to_screen_name"])] = 1
        else:
          self.out[v["in_reply_to_screen_name"]] += 1

    for key in list(self.out.keys()):
      if key in self.out and self.out[key] <= conf.replies_min:
        del self.out[key]

  def output(self, page):
    page.div(class_="block_top block_replies_top")
    page.div("Replies")
    page.div.close()

    page.div(class_="clearboth")
    page.div.close()

    page.div(class_="block_replies_bottom")

    if self.out:
      bar_graph(self.out, output_name="figures/replies.png")
      page.img(src="figures/replies.png", width="720px")
    else:
      page.span("No replies found")
    page.div.close()
