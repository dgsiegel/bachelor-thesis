import re
import time
import os
from pylab import *
import locale

import conf


def strip_html_tags(text):
  return re.sub(r"<[^>]*?>", "", text)


def bar_graph(name_value_dict, graph_title="", output_name="bargraph.png"):
    #fig = figure(figsize=(7.2, 7.2))
    fig = figure()
    title(graph_title, size="x-small")

    sortedvalues, sortedkeys = zip(*sorted(zip(name_value_dict.values(),
                                   name_value_dict.keys()), reverse=True))

    for i, value in zip(range(len(sortedvalues)), sortedvalues):
        bar(i + 0.25, value, color="#73d216")

    xticks(arange(0.65, len(sortedkeys)),
        [("%s: %d" % (name, value)) for name, value in
        zip(sortedkeys, sortedvalues)],
        size="x-small")

    if max(sortedvalues) < 10:
      tick_range = arange(0, 11, 1)
      yticks(tick_range, size="xx-small")
    else:
      yticks(size="x-small")

    gca().yaxis.grid(which="major")

    fig.autofmt_xdate()

    if not os.path.exists(os.path.dirname(output_name)):
      os.mkdir(os.path.dirname(output_name))

    savefig(output_name)

def bar_date_graph(format, name_value_dict, graph_title="", output_name="bargraph.png"):
    locale.setlocale(locale.LC_TIME, conf.locale)

    #fig = figure(figsize=(7.2, 7.2))
    fig = figure()
    title(graph_title, size="x-small")

    sortedkeys, sortedvalues = zip(*sorted(zip(name_value_dict.keys(),
                                   name_value_dict.values()), reverse=False))

    for i, value in zip(range(len(sortedvalues)), sortedvalues):
        bar(i + 0.25, value, color="#73d216")

    if format == "month":
      xticks(arange(0.65, len(sortedkeys)),
          [("%s: %d" % (time.strftime("%B", time.strptime(name, "%m")), value))
            for name, value in zip(sortedkeys, sortedvalues)],
          size="x-small")
    elif format == "day":
      xticks(arange(0.65, len(sortedkeys)),
          [("%s: %d" % (time.strftime("%A", time.strptime(name, "%w")), value))
            for name, value in zip(sortedkeys, sortedvalues)],
          size="x-small")
    elif format == "hour":
      xticks(arange(0.65, len(sortedkeys)),
          [("%sh: %d" % (name, value)) for name, value in
          zip(sortedkeys, sortedvalues)],
          size="x-small")
    else:
      xticks(arange(0.65, len(sortedkeys)),
          [("%s: %d" % (name, value)) for name, value in
          zip(sortedkeys, sortedvalues)],
          size="x-small")

    if max(sortedvalues) < 10:
      tick_range = arange(0, 11, 1)
      yticks(tick_range, size="xx-small")
    else:
      yticks(size="x-small")

    gca().yaxis.grid(which="major")

    fig.autofmt_xdate()

    if not os.path.exists(os.path.dirname(output_name)):
      os.mkdir(os.path.dirname(output_name))

    savefig(output_name)
