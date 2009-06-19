import re
from pylab import *


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
    savefig(output_name)
