from modules.utils import DATA_LABELS, WEEKS_WANTED, load_template
import pandas as pd

# Dictionary mapping webpage name to SQL name of underlying data
LABEL_DICT = {"Hits": 'rolling_view_avg', "Unique Users": "rolling_uu_avg",
              "Form Submissions": "rolling_form_avg"}

# Row indicies of most recent and 7 day trailing entry in dataframe
TODAY = -1
WEEK_AGO = -8

# Column indicies of sums, implied by variable name
HITS_SUM = 7
UU_SUM = 8
FS_SUM = 9


def get_top_data():
  '''Runs SQL query for data to generate top section of the report,
  returns dataframe'''
  """
  Old Query
  top_stats_query = load_query('top_stats')
  data = get_data(top_stats_query)
  """
  data = pd.read_csv("app/sql_queries/top_stats.csv")
  return data


def get_trailing_7(dat):
  ''' Gets total hits, unique users, and form submissions from past week
  and two weeks ago. Uses index locations to get each one.

  args:
    dat - dataframe of top_stats SQL query

  returns:
    sev - list of the 6 relevant numbers
  '''
  hits = dat.iloc[TODAY, HITS_SUM], dat.iloc[WEEK_AGO, HITS_SUM]
  uu = dat.iloc[TODAY, UU_SUM], dat.iloc[WEEK_AGO, UU_SUM]
  forms = dat.iloc[TODAY, FS_SUM], dat.iloc[WEEK_AGO, FS_SUM]
  sev = [hits[0], uu[0], forms[0], hits[1], uu[1], forms[1]]
  return sev


def get_label_dict(data):
  ''' Formats data so it can be passed in as an argument to d3.js

  args:
    dat - dataframe of top_stats SQL query

  behavior:
    loops over each of the data_labels, adds list of dates and
    values to dictionary

  returns:
    out - dictionary containing lists of dates and values for each label

  '''
  data = data.iloc[-(7 * WEEKS_WANTED):]
  data['date'] = data['date'].astype(str)  # to make JS easier
  out = {}
  for label in DATA_LABELS:
    out[label] = data[['date', LABEL_DICT[label]]].values.tolist()
  return out


def create_topgraphs():
  """Reads top_graphs HTML template into Python and formats it

  returns:
    html_str - string containing html for top section of report
  """
  dat = get_top_data()
  sev = get_trailing_7(dat)
  out = get_label_dict(dat)

  dat = {
    'hits_data': out['Hits'],
    'uu_data': out['Unique Users'],
    'fs_data': out['Form Submissions'],
    'hits': sev[0],
    'uu': sev[1],
    'fs': sev[2],
    'ohits': sev[3],
    'ouu': sev[4],
    'ofs': sev[5],
  }
  template = load_template("_top_graphs.html")
  html_str = template.render(dat=dat)
  return html_str
