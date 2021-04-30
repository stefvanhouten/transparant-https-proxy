import pytest
from htmlparser.parser import HTMLParser

EXCLUDE = (
  'script',
  'noscript',
  'html',
)

@pytest.fixture(scope="module")
def htmlparser():
  yield HTMLParser(EXCLUDE)

def test(htmlparser):
  print(htmlparser.parse(r'D:\devel\transparant-https-proxy\htmlparser\data\index.html'))