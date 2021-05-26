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

    utf8String = self.charset_normalizer(flow.response.get_content(False))
    flow.response.headers['Content-Type'] = 'application/xml'
    flow.response.text = self.parser.parse(utf8String)

  def charset_normalizer(self, byte_string):
    result = CnM.from_bytes(
      byte_string,
      threshold = 100, #threshold is set to high, to prevent filtering, change to desired threshold when deploying
      preemptive_behaviour=True,  # Determine if we should look into my_byte_str (ASCII-Mode) for pre-defined encoding
      explain=True  # Print on screen what is happening when searching for a match (FOR DEBUGGING PURPOSES)
    ).best().first() #KEEP ONLY THE MATCHES WITH THE LOWEST RATIO OF CHAOS - SELECT THE FIRST MATCH AVAILABLE

    #ENCODE TO UTF-8
    utf8String = str(result)

    return utf8String


addons = [
    Parser()
]