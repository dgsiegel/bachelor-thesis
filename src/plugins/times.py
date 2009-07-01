import sys
import os
import string
import time
import calendar
import rfc822

from pylab import *

from markup import oneliner as e

from plugin import Plugin
from util import bar_date_graph


class TimesPlugin (Plugin):

  def __init__(self):
    self.data = None
    self.out = {}

    self.month = {}
    self.day = {}
    self.hour = {}

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
      t = time.gmtime(calendar.timegm(rfc822.parsedate(v["created_at"])))

      month = time.strftime("%m", t)
      day = time.strftime("%w", t)
      hour = time.strftime("%H", t)
      if month not in self.month:
        self.month[month] = 1
      else:
        self.month[month] += 1

      if day not in self.day:
        self.day[day] = 1
      else:
        self.day[day] += 1

      if hour not in self.hour:
        self.hour[hour] = 1
      else:
        self.hour[hour] += 1


  def output(self, page):
    page.div(class_="block_top block_times_top")
    page.div("Twitter Times Analysis")
    page.div.close()

    page.div(class_="clearboth")
    page.div.close()

    page.div(class_="block_times_bottom")

    bar_date_graph("month", self.month, output_name="figures/times_month.png")
    page.img(src="figures/times_month.png", width="720px")

    bar_date_graph("day", self.day, output_name="figures/times_day.png")
    page.img(src="figures/times_day.png", width="720px")

    bar_date_graph("hour", self.hour, output_name="figures/times_hour.png")
    page.img(src="figures/times_hour.png", width="720px")

    page.div.close()
