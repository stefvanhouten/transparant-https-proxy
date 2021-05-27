import requests
import json

from charset_normalizer import CharsetNormalizerMatches as CnM
from mitmproxy import ctx
from htmlparser.parser import HTMLParser

def charset_normalizer(byte_string, fallback):
    result = CnM.from_bytes(
        byte_string,
        preemptive_behaviour=True,
        explain=False
    ).best().first()

    if result is not None and getattr(result, 'encoding'):
        return str(byte_string.decode(encoding=result.encoding))
    return fallback

def exclude_list():
    # res = requests.get('http://127.0.0.1:5000/proxy')
    # data = json.loads(res.content)
    # data.get('exclude', ['html', 'script', 'style'])
    return ['html', 'script', 'style']
class Parser:
  def request(self, flow):
    self.parser = HTMLParser(exclude_list())

  def response(self, flow):
    if not 'html' in flow.response.headers.get('Content-Type', ""):
      return

    utf8String = charset_normalizer(flow.response.raw_content, flow.response.text)

    flow.response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    flow.response.text = self.parser.parse(utf8String)


addons = [
    Parser()
]