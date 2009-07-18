import sys
import os

PLUGIN_PATH = "plugins/"
PLUGINS_ENABLED = [
#    "testplugin",
    "user",
    "mail",
    "textsearch",
    "times",
    "replies",
    "sources",
    "interests",
    "location",
    "friends",
    ]


class Plugin(object):

  def download(self):
    pass

  def parse(self):
    pass

  def output(self):
    pass


def init_plugin_system():
  if not PLUGIN_PATH in sys.path:
    sys.path.insert(0, PLUGIN_PATH)
  for plugin in PLUGINS_ENABLED:
    __import__(plugin)


_instances = {}

def find_plugins():
  result = []
  for plugin in Plugin.__subclasses__():
    if not plugin in _instances:
      _instances[plugin] = plugin()
      result.append(_instances[plugin])
  return result
