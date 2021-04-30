import pytest
from htmlparser.parser import HTMLParser

EXCLUDE = (
  'script',
  'noscript',
  'html',
)

@pytest.fixture(scope='module')
def htmlparser():
  yield HTMLParser(EXCLUDE)

@pytest.fixture(scope='module')
def tests():
  yield [

  ]

def test_incomplete_html(htmlparser):
  output = htmlparser.parse('<p>', pretty_xml=False)
  EXPECTED = '<data><head></head><body><p></p></body></data>'
  assert output == EXPECTED

def match_output_vs_expected(tests, subtests, htmlparser):
  for testcase in tests:
    with subtests.test(test=testcase['test']):
      output = htmlparser.parse(testcase['test'], pretty_xml=False)
      assert output == testcase['expected']

def test_broken_html(htmlparser, subtests):
  tests = [
    {'test': '<p></b>', 'expected': '<data><head></head><body><p></p></body></data>'},
    {'test': '<div><h1>hello world</p></div>', 'expected': '<data><head></head><body><div><h1>hello world<p></p></h1></div></body></data>'},
  ]
  match_output_vs_expected(tests, subtests, htmlparser)

def test_html_entities(htmlparser, subtests):
  tests = [
    {'test': '&lt;', 'expected': '<data><head></head><body>&lt;</body></data>'},
    {'test': '&gt;', 'expected': '<data><head></head><body>&gt;</body></data>'},
    {'test': '&lt;p&gt;', 'expected': '<data><head></head><body>&lt;p&gt;</body></data>'},
    {'test': '&amp;', 'expected': '<data><head></head><body>&amp;</body></data>'},
    {'test': '&quot;', 'expected': '<data><head></head><body>"</body></data>'}, #Apparently &qout is accepted to escape to "
    {'test': '&apos;', 'expected': "<data><head></head><body>'</body></data>"}, #Same here for &apos to be '
  ]
  match_output_vs_expected(tests, subtests, htmlparser)