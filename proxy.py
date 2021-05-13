"""
Basic skeleton of a mitmproxy addon.

Run as follows: mitmproxy -s anatomy.py
"""
from mitmproxy import ctx
from htmlparser.parser import HTMLParser

EXCLUDE = (
  'script',
  'noscript',
  'html',
  'style',
  'doctype',
  'meta'
  )

parser = HTMLParser(EXCLUDE)

class Counter:
    def response(self, flow):
        flow.response.headers['Content-Type'] = 'application/xml'
        flow.response.text = parser.parse(flow.response.text)

addons = [
    Counter()
]