from mitmproxy import ctx
from htmlparser.parser import HTMLParser

EXCLUDE = (
  'script',
  'noscript',
  'html',
  'style',
  'doctype',
  'meta',
  )

parser = HTMLParser(EXCLUDE)
class Parser:
  def response(self, flow):
    if not 'html' in flow.response.headers['Content-Type']:
      return

    flow.response.headers['Content-Type'] = 'application/xml'
    flow.response.text = parser.parse(flow.response.text)

addons = [
    Parser()
]