import requests
import json

from mitmproxy import ctx
from htmlparser.parser import HTMLParser
class Parser:
  def request(self, flow):
    res = requests.get('http://127.0.0.1:5000/proxy')
    data = json.loads(res.content)
    self.parser = HTMLParser(data.get('exclude', ['html', 'script', 'style']))

  def response(self, flow):
    if not 'html' in flow.response.headers['Content-Type']:
      return

    flow.response.headers['Content-Type'] = 'application/xml'
    flow.response.text = self.parser.parse(flow.response.text)

addons = [
    Parser()
]