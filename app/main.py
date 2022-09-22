import pandas as pd
from collections import defaultdict
import warnings
from app.modules.utils import read_from_outfile
from modules.top_graphs import create_topgraphs
from modules.header import create_header
from modules.blog import create_blog
from modules.graph_detail import create_detail_graphs
from modules.transformations import CATEGORY_VALUES
from modules.utils import (announce, get_current, get_campaign_temp,
                           format_key, write_to_html, load_template,
                           DATA_LABELS, DROP_COLS)

# A .env file with values for these env vars should exist in your local

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)

# To suppress false positive warnings
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore', message='.*line style*', )

# Global Constants
S3_HTML = "file.html"
S3_CSS = "main.css"


def prepare_data(data, weeks):
  """Filters data based on whether doing week or day analysis

  args:
    data - dataframe output by transformations.py
    weeks - 1 if week analysis, 0 if days

  behavior:
    For week anaysis, removes incomplete weeks.
    For both, sets time unit to be the relevant dates,
    adds it to result

  returns:
    data - filtered dataframe
    time_unit - weeks or days to look at
    result - default dict initialized with the list of dates
    campaigns - list of all campaigns in data
  """

  result = defaultdict(list)

  campaigns = data['campaign'].unique()
  if weeks == 1:
    data = data[data['week_complete']]
    result['Week'] = list(data['week'].unique())
  time_unit = data['week'].unique()
  if weeks == 0:
    dates = data['date'].unique()
    time_unit = dates
    result['Date'] = list(dates)

  return data, time_unit, result, campaigns


def get_hits_results(curr, result, campaigns):
  '''Adds hits by campaign and category to result dict'''
  label = DATA_LABELS[0]
  result[label].append(len(curr))

  for campaign in campaigns:
    temp = get_campaign_temp(curr, campaign)
    key = format_key(label, campaign)
    result[key].append(len(temp))

  for cat in CATEGORY_VALUES:
    temp = curr[curr['category'] == cat]
    key = format_key(label, cat)
    result[key].append(len(temp))

  return result


def get_unique_user_results(curr, result, campaigns):
  '''Adds unique users by campaign and category to result dict'''
  label = DATA_LABELS[1]
  result[label].append(len(curr['anonymous_id'].unique()))

  for campaign in campaigns:
    temp = get_campaign_temp(curr, campaign)
    key = format_key(label, campaign)
    result[key].append(len(temp['anonymous_id'].unique()))

  for cat in CATEGORY_VALUES:
    temp = curr[curr['category'] == cat]
    key = format_key(label, cat)
    result[key].append(len(temp['anonymous_id'].unique()))
  return result


def get_form_results(curr, result, campaigns):
  """Adds form submissions by campaign to result dict"""
  label = DATA_LABELS[2]
  curr = curr[~curr['form'].isnull()]  # filters out all non-form submissions
  result[label].append(len(curr))
  for campaign in campaigns:
    temp = get_campaign_temp(curr, campaign)
    key = format_key(label, campaign)
    result[key].append(len(temp))
  return result


def calculate_results(data, weeks):
  """Calculates hits, unique users, and form submissions across specified date
  range, weeks if weeks=1, or days if weeks=0
  Filters data based on whether doing week or day analysis

  args:
    data - dataframe output by transformations.py
    weeks - 1 if week analysis, 0 if days

  behavior:
    Loops through dates, invokes helpers for the 3 labels to populate
    the result dictionary.

  returns:
    result - default dict of lists. First list is dates, each ensuing list
    contains data from the 5 different breakdowns (same 5 as the area graphs)
    campaigns - list of all campaigns in data
  """

  data, time_unit, result, campaigns = prepare_data(data, weeks)

  for unit in time_unit:
    curr = get_current(data, unit, weeks)
    for curr_label in DATA_LABELS:
      if curr_label == DATA_LABELS[0]:
        result = get_hits_results(curr, result, campaigns)
      elif curr_label == DATA_LABELS[1]:
        result = get_unique_user_results(curr, result, campaigns)
      elif curr_label == DATA_LABELS[2]:
        result = get_form_results(curr, result, campaigns)

  return result, campaigns


def time_dfs(results, index):
  ''' Transforms results into a html table'''
  full = pd.DataFrame.from_dict(results[index])
  out = (full.drop(DROP_COLS,
                   axis=1).to_html(index=False))
  return out


def get_html_string(sections):
  """Reads HTML template into Python and formats it"""
  template = load_template('index.html')
  html_str = template.render(dat=sections)
  return html_str


def main(stage_locally=True, write_to_s3=False):
  """ Creates website report. Invokes helper methods

  args: controlled by command line flags
    stage_locally - whether to write locally
    write_to_s3 - whether to write result to s3

  behavior:
    Inovkes helper functions to build website report, announces to
    terminal at each stage. Writes resulting report to index.html
    if stage_locally is True, writes to analytics website if write_to_s3
    is True.
  """
  announce("Starting script")
  sections = {}
  announce("Building Header Module")
  sections['header'] = create_header('Launchpad')
  """
  Code from original version of report

  announce('Pulling monolithic user, form, pages dataset')
  pages_forms_query = load_query('pages_forms',
                                 **{'NUM_WEEKS': WEEKS_WANTED + 1})
  data = get_data(pages_forms_query)
  announce("Transforming data")
  data = transform_data(data)
  announce("Calculating results")
  results = [calculate_results(data, 1), calculate_results(data, 0)]
  results, campaigns = extract_results(results)
  """
  announce("Pulling results")
  results = [read_from_outfile("app/sql_queries/week_results.json"),
             read_from_outfile("app/sql_queries/day_results.json")]
  campaigns = read_from_outfile("app/sql_queries/campaigns.json")
  announce("Getting Top Section")
  sections['topgraph'] = create_topgraphs()
  announce("Creating Blog Module")
  sections['blog'] = create_blog()
  announce("Creating Detailed Graphs")
  sections['graph_detail'] = create_detail_graphs(results, campaigns)
  announce("Creating Tables")
  sections['week_table'] = time_dfs(results, 0)
  sections['day_table'] = time_dfs(results, 1)
  announce("Formatting HTML File")
  html_str = get_html_string(sections)

  if stage_locally:
    announce("Writing HTML File")
    write_to_html(html_str, 'static/index.html')

  announce("Done")
  return 0


if __name__ == "__main__":
  main()
