import sys
import os
import string
import re

from markup import oneliner as e

from plugin import Plugin
from markup import escape

import conf

class MailPlugin(Plugin):

  def __init__(self):
    self.data = None
    self.out = []

  def download(self, api, args):
    if (args and "id" in args):
      i = 1

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

   for v in self.data:
      m = re.findall("[a-zA-Z0-9\._%-\+]+@[a-zA-Z0-9\._%-]+\.[a-zA-Z]{2,6}", v["text"])

      if m:
        found = False
        for w in self.out:
          if w["id"] == v["id"]:
            found = True
        if not found:
          self.out.append(v)

  def output(self, page):
    page.div(class_="block_top block_mail_top")
    page.div("Mail addresses")
    page.div.close()

    page.div(class_="clearboth")
    page.div.close()

    page.div(class_="block_mail_bottom")

    if self.out:
      for v in self.out:
        v["text"] = escape(v["text"]).encode("ascii", "xmlcharrefreplace")
        v["text"] = re.sub("([a-zA-Z0-9\._%-\+]+@[a-zA-Z0-9\._%-]+\.[a-zA-Z]{2,6})", "<span class=\"value\">\\1</span>", v["text"])

        page.div(class_="block_mail_entry")
        page.div(v["text"], class_="block_mail_entry_value")

        page.span("Posted on " + v["created_at"] + " using " + v["source"], class_="block_mail_entry_value_info")
        if v["in_reply_to_status_id"] != None:
          page.span("In reply to status id: " + str(v["in_reply_to_status_id"]), class_="block_mail_entry_value_info")
        if v["in_reply_to_screen_name"] != None:
          page.span("In reply to screen name: " + str(v["in_reply_to_screen_name"]), class_="block_mail_entry_value_info")

        page.div.close()
    else:
      page.span("No matches found")

    page.div.close()
