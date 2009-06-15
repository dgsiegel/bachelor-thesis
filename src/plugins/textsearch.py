import sys
import os
import string

from markup import oneliner as e

from plugin import Plugin
from markup import escape

class TestPlugin (Plugin):
  def __init__ (self):
    self.data = None
    self.out = []
    self.keywords = ["Obama", "health"]
  def download (self, api, args):
    if (args and "id" in args):
      self.data = api.statuses.user_timeline(id=args["id"], count=50)
    else:
      raise Exception("The User ID is needed for this plugin")
  def parse (self):

    for v in self.data:
      for k in self.keywords:
        if k in v["text"]:
          found = False
          for w in self.out:
            if w["id"] == v["id"]:
              found = True
          if not found:
            self.out.append(v)


  def output (self, page):
    page.div(class_="block_top block_textsearch_top")
    page.div("Text search for: " + string.join(self.keywords, ", "))
    page.div.close()

    page.div(class_="clearboth")
    page.div.close()

    page.div(class_="block_textsearch_bottom")

    for v in self.out:
      v["text"] = escape(v["text"]).encode('ascii', 'xmlcharrefreplace')
      for k in self.keywords:
        if k in v["text"]:
          v["text"] = v["text"].replace(k, "<span class=\"keyword\">"+k+"</span>")

      page.div(class_="block_textsearch_entry")
      page.div(v["text"], class_="block_textsearch_entry_value")

      page.span("Posted on " + v["created_at"] + " using " + v["source"], class_="block_textsearch_entry_value_info")
      if v["in_reply_to_status_id"] != None:
        page.span("In reply to status id: " + str(v["in_reply_to_status_id"]), class_="block_textsearch_entry_value_info")
      if v["in_reply_to_screen_name"] != None:
        page.span("In reply to screen name: " + str(v["in_reply_to_screen_name"]), class_="block_textsearch_entry_value_info")

      page.div.close()

    page.div.close()
