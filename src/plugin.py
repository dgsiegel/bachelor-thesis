import sys
import os

import conf

PLUGIN_PATH = "plugins/"

class Plugin(object):

  def download(self, api, args):
    pass

  def parse(self):
    pass

  def output(self, page):
    pass


def init_plugin_system():
  if not PLUGIN_PATH in sys.path:
    sys.path.insert(0, PLUGIN_PATH)
  for plugin in conf.PLUGINS_ENABLED:
    __import__(plugin)


_instances = {}

def find_plugins():
  result = []
  for plugin in Plugin.__subclasses__():
    if not plugin in _instances:
      _instances[plugin] = plugin()
      result.append(_instances[plugin])
  return result
