import json
import jinja2
from datetime import datetime

# In static version of report, cannot be changed
WEEKS_WANTED = 4

# Labels to track throughout report
DATA_LABELS = ["Hits", "Unique Users", "Form Submissions"]

# Columns not needed in html report
DROP_COLS = [
  'Hits nan', 'Hits Herefish', 'Hits legal',
  'Unique Users nan', 'Unique Users Herefish',
  'Unique Users legal', 'Form Submissions nan', 'Form Submissions Herefish'
]


def announce(message):
  '''Prints to terminal time and user inputted message'''
  print("{0}: {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          message))


def get_current(data, unit, weeks):
  """Gets the rows of the data in the specified week or day"""
  selector_col = 'week' if weeks == 1 else 'date'
  return data[data[selector_col] == unit]


def format_key(label, descriptor):
  """Returns concatenated string in constant format for dictionary key"""
  return label + " " + str(descriptor)


def get_campaign_temp(df, campaign):
  """Returns temporary dataframe used for calculating breakdown by
  campaign"""
  return df[df['campaign'].isnull()] if campaign is None else df[
    df['campaign'] == campaign]


def write_to_html(html_str, filename):
  """Writes string properly formatted html to filename"""
  f = open(filename, 'w')
  f.write(html_str)
  f.close()


def extract_results(results):
  """Pulls the daily and weekly dictionaries and campaigns out of the bigger
  results list output by calculate_results"""
  result = [results[0][0], results[1][0]]
  campaigns = results[0][1]
  return result, campaigns


def write_to_outfile(results, file_name):
  '''Writes a list of dictionaries to json file'''
  with open(file_name, 'w') as outfile:
    json_result = json.dumps(results)
    outfile.write(json_result)
    outfile.write('\n')


def read_from_outfile(file):
  with open(file) as json_file:
    data = json.load(json_file)
    return data


'''
def get_data(query_string):
  """Downloads SQL results into Python, represented as a DataFrame"""
  bqclient = bigquery.Client()

  data = (bqclient.query(query_string).result().to_dataframe(
    create_bqstorage_client=True, ))
  return data
'''


def load_template(template_path):
  '''Loads,initializes and returns jinja template'''
  template_loader = jinja2.FileSystemLoader(searchpath='app/templates')
  template_env = jinja2.Environment(loader=template_loader)
  template = template_env.get_template(template_path)
  return template
