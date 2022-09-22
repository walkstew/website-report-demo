import numpy as np

# Possible webpage categories
CATEGORY_VALUES = ["seo", "info", "lead", 'legal', 'job']


def add_categories(data):
  """Adds the category each webpage to the pages and forms dataframes

  args:
    data — dataframe of raw data from pages_forms SQL query

  behavior:
    Categorizes pages into one of 5 buckets, uses regex-like
    logic to implement this by parsing the url.

  returns:
    dataframe with category column populated
  """
  def check_condition(data, category):
    if category == 'seo':
      series = (data['path'].str[2:6] == 'blog') | \
               (data['path'].str[2:11] == 'directory') | \
               (data['path'].str[2:8] == 'commun')
    elif category == 'info':
      series = (data['path'] == '//') | \
               (data['path'].str[2:5] == 'faq') | \
               (data['path'].str[2:5] == 'our') | \
               (data['path'].str[2:11] == 'free-move')
    elif category == 'lead':
      series = (data['path'].str[2:8] == 'robson') | \
               (data['path'].str[2:6] == 'form')
    elif category == 'legal':
      series = (data['path'].str[2:7] == 'terms-') | \
               (data['path'].str[2:9] == 'privacy') | \
               (data['path'].str[2:11] == 'licenses-')
    elif category == 'job':
      series = (data['path'].str[2:18] == 'job-descriptions')
    else:
     raise ValueError('Unimplemented category %s' % category)
    return series

  conditions = [check_condition(data, category)
                for category in CATEGORY_VALUES]

  data['category'] = np.select(conditions, CATEGORY_VALUES)
  return data


def get_first_visit_info(data):
  """ Adds record of user's initial ad-campaign and page visit
  to row containing each of their hits.

  args:
    data — dataframe of raw data from pages_forms SQL query (ordered by
    timestamp),modified by check_condition

  behavior:
    Finds the first instance of a user in the data, sets all of that user's
    campaign and first_hit columns to be the campaign and category of the
    first hit.

    Additionally, removes all rows that are outside the timeframe of the
    report, were only necesary to ensure a user's first visit wasn't missed.

  returns:
    dataframe with campaign and first_hit columns populated
  """

  anon = data['anonymous_id'].unique()
  data['campaign'] = ""
  data['first_hit'] = ""

  source_index = data.columns.get_loc('context_campaign_source')
  path_index = data.columns.get_loc('path')

  for id in anon:
    first_index = (data.anonymous_id.values == id).argmax()
    source = data.iloc[first_index, source_index]
    path = data.iloc[first_index, path_index]
    data.loc[data['anonymous_id'] == id, 'campaign'] = source
    data.loc[data['anonymous_id'] == id, 'first_hit'] = path

  # filters pages and forms dataframes to only include hits within the
  # specified time period.
  data = data[data['week_cat']]

  return data


def transform_data(data):
  """Adds categories and first visit columns to dataframe (data)"""
  data = add_categories(data)
  return get_first_visit_info(data)
