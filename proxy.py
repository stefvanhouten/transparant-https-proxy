import requests
import json

from charset_normalizer import CharsetNormalizerMatches as CnM
from mitmproxy import ctx
from htmlparser.parser import HTMLParser

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

    utf8String = self.charset_normalizer(flow.response.content)
    flow.response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    flow.response.text = self.parser.parse(utf8String)

  def charset_normalizer(self, byte_string):
    result = CnM.from_bytes(
      byte_string,
      threshold = 0.2, #threshold has been explicitly set for further maintenance
      preemptive_behaviour=True,  # Determine if we should look into my_byte_str (ASCII-Mode) for pre-defined encoding
      explain=False  # Print on screen what is happening when searching for a match (FOR DEBUGGING PURPOSES)
    ).best().first() #keep only the matches with the lowest ratio of chaos, select the first one from the returned list

    #encode to UTF-8
    utf8String = str(result)

    return utf8String

addons = [
    Parser()
]