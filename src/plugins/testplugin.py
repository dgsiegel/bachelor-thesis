import sys
import os

from plugin import Plugin
from api import TwitterAPI, dump

class TestPlugin (Plugin):
  def download (self, api, data):
    if (data and "id" in data):
      dump(api.users.show(id=data["id"]))
    else:
      dump(api.statuses.public_timeline())
