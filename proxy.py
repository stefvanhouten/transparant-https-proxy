import requests
import json

from typing import Union, Optional, AnyStr, overload
from charset_normalizer import CharsetNormalizerMatches as CnM
from mitmproxy import ctx
from decode.contentDecoder import ContentDecoder
from htmlparser.parser import HTMLParser

def exclude_list():
    # res = requests.get('http://127.0.0.1:5000/proxy')
    # data = json.loads(res.content)
    # data.get('exclude', ['html', 'script', 'style'])
    return ['script', 'style']

class Parser:
  def request(self, flow):
    self.parser = HTMLParser(exclude_list())


  def response(self, flow):
    if not 'html' in flow.response.headers.get('Content-Type', ""):
      return

    decompressedContent = self.get_content(flow)

    if decompressedContent is not None:
      # Content could be uncompressed bytes, even though server-side could've compressed!
      utf8String = self.charset_normalizer(decompressedContent)
    else:
      utf8String = "Content could not be decompressed!"
    
    flow.response.headers['Content-Type'] = 'application/xml; charset=utf-8'

    try:
      flow.response.text = self.parser.parse(utf8String)
    except:
      flow.response.text = self.parser.parse("Parser could not convert to XML!")

  def get_content(self, flow) -> Union[None, str, bytes]:
      if flow.response.raw_content is None:
          return None

      ce = flow.response.headers.get('Content-encoding', '')
      encoding = ContentDecoder()

      if ce:
        content = encoding.decode(flow, ce)

        # A client may illegally specify a byte -> str encoding here (e.g. utf8)
        if isinstance(content, str):
          return "Illegally specified content-encoding!"
      else:
        # no content-header was provided
        # force decode to fail and try all possible decompressions
        # note: could be that there is no compression done server side, uncompressed will be returned
        content = encoding.decode(flow, ce)
      
      return content

  def charset_normalizer(self, byte_string):
    result = CnM.from_bytes(
      byte_string,
      threshold = 1, #Some websites simply are too different, they need a margin or else the prgram will simply fail
      preemptive_behaviour=True,  # Determine if we should look into my_byte_str (ASCII-Mode) for pre-defined encoding
      explain=False  # Print on screen what is happening when searching for a match (FOR DEBUGGING PURPOSES)
    ).best().first() #keep only the matches with the lowest ratio of chaos, return the first list from the element

    if result is not None:
      #encode to UTF-8
      utf8String = str(result)
      return utf8String
    else:
      return "Could not guess content-type! Either set the threshold higher, or the file is simply too malformed."

addons = [
    Parser()
]