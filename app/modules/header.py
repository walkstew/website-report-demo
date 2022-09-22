from .utils import load_template
import time


def get_data_time():
  """Gets the unix time in milliseconds of the max pageview in the db"""

  """ Hard coding value here.
  max_timestamp_query =
  select max(unix_millis(timestamp)) as timestamp
  from sunbound-website-analytics.sunbound_homes_production.pages


  max_timestamp = get_data(max_timestamp_query)
  data_time = max_timestamp.iloc[0, 0] """
  data_time = 1663692987045
  return data_time


def create_header(title, query_db=True):
  """ Formats page header

  args:
    title - title of webpage
    query_db - boolean, get time from database?

  behavior:
    Formats header html with current time in seconds,
    JS takes care of making it human readable.

  returns:
    html_str - html string for the page header
  """
  dat = {}
  dat['title'] = title
  if query_db:
    dat['data_time'] = get_data_time()

  dat['report_time'] = time.time() * 1000
  template = load_template("_header.html")
  html_str = template.render(**dat)
  return(html_str)
