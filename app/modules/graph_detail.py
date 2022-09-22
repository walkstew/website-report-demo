from copy import deepcopy
from modules.transformations import CATEGORY_VALUES
from modules.utils import format_key, load_template, DATA_LABELS

# Color palatte to use
COLORS = ["darkgoldenrod", "coral", "darkseagreen", "blueviolet", "darycyan",
          "aqua", "darksalmon", "dimgrey", "dodgerblue", "honeydew",
          "green", "lavender", "lawngreen"]

# Titles of the 5 graphs
TITLES = ["Hits by Source", "Hits by Page", "Unique Users by Source",
          "Unique Users by Page", "Form Submissions by Source"]


def add_values(out, generic, labels):
  '''Adds layer to each of the 3 lists supplied'''
  out['data'].append(generic)
  out['labels'].append(labels)
  out['colors'].append(COLORS[0:len(labels)])
  return out


def get_generics(results):
  ''' Creates generic week and day dictionaries

  args:
    results - dictionary of results calculated in main.py

  behavior:
    Represents all dates as strings for easier JS functionality,
    segments results by week and day to create 2 generic lists.

  returns:
    week_generic, day_generic - list of 1 pair dictionaries, to
    be populated by format_data()
  '''
  week_dates = results[0]['Week']
  day_dates = results[1]['Date']
  week_generic = []
  day_generic = []
  for date in week_dates:
    week_generic.append({"date": str(date)})
  for date in day_dates:
    day_generic.append({"date": str(date)})
  return week_generic, day_generic


def format_data(results, campaigns):
  ''' Creates generic week and day dictionaries

  args:
    results - dictionary of results calculated in main.py
    campaigns - list of campaigns calculated in main.py

  behavior:
    For the week and day results, adds campaign and category
    data to the proper generic dictionary, then invokes add_values
    to put output into variables to be returned.

  returns:
    week_out, day_out - dictionary of lists, containing hits, unique user,
    and form submission datapoints with the correct time frame, as well as the
    labels for each datapoint and the color it should be graphed in.
  '''

  week_gen, day_gen = get_generics(results)
  week_out = {"data": [], "labels": [], "colors": []}
  day_out = {"data": [], "labels": [], "colors": []}

  for result in results:
    week = 1 if "Week" in result else 0
    for curr_label in DATA_LABELS:
      generic = deepcopy(week_gen) if week == 1 else deepcopy(day_gen)
      labels = []
      for item in campaigns:
        key = format_key(curr_label, item)
        labels.append(key)
      for i in range(len(generic)):
        for label in labels:
          # Generic is essentially flipping the dict/list structure of result
          generic[i][label] = result[label][i]
      if week:
        week_out = add_values(week_out, generic, labels)
      else:
        day_out = add_values(day_out, generic, labels)

      if curr_label != DATA_LABELS[2]:
        generic = deepcopy(week_gen) if week == 1 else deepcopy(day_gen)
        labels = []
        for item in CATEGORY_VALUES:
          key = format_key(curr_label, item)
          labels.append(key)
        for i in range(len(generic)):
          for label in labels:
            generic[i][label] = result[label][i]
        if week:
          week_out = add_values(week_out, generic, labels)
        else:
          day_out = add_values(day_out, generic, labels)
  return week_out, day_out


def create_detail_graphs(results, campaigns):
  """ Formats graph_detail.html"""
  week_out, day_out = format_data(results, campaigns)
  template = load_template("_graph_detail.html")
  html_str = template.render(week_out=week_out, day_out=day_out, titles=TITLES)
  return html_str
