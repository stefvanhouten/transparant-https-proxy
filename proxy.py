import requests
import json

from typing import Union
from charset_normalizer import CharsetNormalizerMatches as CnM
from mitmproxy import ctx
from decode.contentDecoder import ContentDecoder
from htmlparser.parser import HTMLParser
from http import HTTPStatus

def exclude_list(config_ip, config_name):
    if config_ip is not None and config_name is not None:
      res = requests.get(f'http://127.0.0.1:5000/proxy/get_config/{config_ip}/{config_name}')
      if res.status_code == HTTPStatus.OK:
        data = json.loads(res.content)
        return data['config']['exclude_elements']
    return ['svg', 'script']

class Parser:
  def request(self, flow):
    config_ip = flow.request.headers.get('config_ip')
    config_name = flow.request.headers.get('config_name')
    self.parser = HTMLParser(exclude_list(config_ip, config_name))


  def response(self, flow):
    if not 'html' in flow.response.headers.get('Content-Type', ""):
      return
    flow.response.headers['Content-Type'] = 'application/xml; charset=utf-8'

    decompressedContent = self.get_content(flow)
    utf8String = flow.response.text

    if decompressedContent is not None:
      result = self.charset_normalizer(decompressedContent)
      if result is not None:
        utf8String = result

    try:
      flow.response.text = self.parser.parse(utf8String)
    except:
      flow.response.text = self.parser.parse("Parser could not convert to XML!")

    # Postman wont allow these headers at the same time
    if "Content-Length" in flow.response.headers and "transfer-encoding" in flow.response.headers:
      del flow.response.headers['Content-Length']


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
      threshold = 1,
      preemptive_behaviour=False,
    ).best().first() #keep only the matches with the lowest ratio of chaos, return the first list from the element

    if result is not None:
      utf8String = str(result)
      return utf8String


addons = [
    Parser()
]