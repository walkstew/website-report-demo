import unittest
from app.modules.header import create_header
from app.modules.blog import create_blog
from app.modules.utils import read_from_outfile
from app.modules.top_graphs import create_topgraphs
from app.modules.graph_detail import create_detail_graphs


class TestDataMethods(unittest.TestCase):
  ''' Testing for remaining functions'''
  def test_header(self):
    self.assertEqual(create_header("Test")[0:46],
                     """<h2>Sunbound Website Report</h2>\n<h2>Test</h2>""")

  campaigns = read_from_outfile("app/sql_queries/campaigns.json")

  def test_reading(self):
    self.assertEqual(['adwords', 'nan', 'outbrain', 'fb_paid',
                      'hs_automation', 'google_paid', 'Herefish',
                      'hs_email', 'facebook'], self.campaigns)

  def test_blog(self):
    blog = create_blog()
    self.assertTrue("<td>981</td>" in blog)
    self.assertTrue("<td>Is Georgia a Good Place to Retire to?</td>" in blog)
    self.assertFalse("<td>5860</td>" in blog)

  results = [read_from_outfile("app/sql_queries/week_results.json"),
             read_from_outfile("app/sql_queries/day_results.json")]

  def test_graphs(self):
    top_graphs = create_topgraphs()
    area_graphs = create_detail_graphs(self.results, self.campaigns)
    self.assertTrue("['8/29/22', 227.4]" in top_graphs)
    self.assertFalse("['8/30/22', 306.9]" in top_graphs)
    self.assertTrue("{'date': '9/12/22', 'Form Submissions adwords': 46"
                    in area_graphs)
    self.assertFalse("'Form Submissions outbrain': 522" in area_graphs)


if __name__ == '__main__':
  unittest.main()
