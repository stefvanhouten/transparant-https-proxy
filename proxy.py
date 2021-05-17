import requests
import json

from charset_normalizer import CharsetNormalizerMatches as CnM
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

    utf8String = charset_normalizer(flow.response.content)

    flow.response.text = self.parser.parse(utf8String)

  def charset_normalizer(self, byte_string):
    result = CnM.from_bytes(
      byte_string,
      preemptive_behaviour=True  # Determine if we should look into my_byte_str (ASCII-Mode) for pre-defined encoding
    ).best().first() #KEEP ONLY THE MATCHES WITH THE LOWEST RATIO OF CHAOS - SELECT THE FIRST MATCH AVAILABLE

    if len(result) > 0:
      #ENCODE TO UTF-8
      utf8String = str(result)
      return utf8String


addons = [
    Parser()
]