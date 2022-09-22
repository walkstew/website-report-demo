import pandas as pd
from modules.utils import WEEKS_WANTED, load_template, read_from_outfile

#  Number of blog posts to include
BLOG_POST_COUNT = 5


def get_blog_breakdown():
  """Filters data based on whether doing week or day analysis

  args:
    data - dataframe output by transformations.py

  behavior:
    Aggregates individual blog post hits, then gets top (default) 5
    blog posts by hits in the last (default) 4 weeks, writes a dataframe
    containing relevent information about each post.

  returns:
    html table containing blog post names, hits, and users
  """

  """
  Code from main version of report

  result = defaultdict(int)
  data = data[(data['path'].str[2:6] == 'blog') & (
    data['title'] != 'Blog | Sunbound')]
  data['date'] = data['date'].astype("datetime64")
  off = pd.DateOffset(days=WEEKS_WANTED * 7)
  min = max(data['date']) - off
  data = data[data['date'] > min]
  top_posts = data['title'].value_counts().index.tolist()[:BLOG_POST_COUNT]
  for i in range(len(top_posts)):
    temp = data[data['title'] == top_posts[i]]
    name = top_posts[i].replace('| Sunbound Blog', '', 1)
    hits = len(temp)
    viewers = len(temp['anonymous_id'].unique())
    result[i] = [name, hits, viewers]
  """

  result = read_from_outfile("app/sql_queries/blog_data.json")
  df = pd.DataFrame.from_dict(result, orient='index',
                              columns=['Title', 'Hits', 'Viewers'])
  return df.to_html(index=False)


def create_blog():
  '''Formats blog html template'''
  content = get_blog_breakdown()
  template = load_template("_blog.html")
  html_str = template.render(blog=content, blog_days=WEEKS_WANTED * 7)
  return html_str
