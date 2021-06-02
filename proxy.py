import requests
import json

from typing import Optional
from charset_normalizer import CharsetNormalizerMatches as CnM
from mitmproxy import ctx
from decode.contentDecoder import ContentDecoder
from htmlparser.parser import HTMLParser

def exclude_list():
    # res = requests.get('http://127.0.0.1:5000/proxy')
    # data = json.loads(res.content)
    # data.get('exclude', ['html', 'script', 'style'])
    return ['html', 'script', 'style']

class Parser:
  def request(self, flow):
    self.parser = HTMLParser(exclude_list())
    self.encodings = self.content_encodings()

  def content_encodings(self):
    return [
      'gzip, compress, deflate, br',
      'gzip, compress, deflate',
      'gzip, compress, br',
      'gzip, deflate, br',
      'compress, deflate, br',
      'gzip, deflate',
      'gzip, br',
      'compress, br',
      'deflate, br',
      'gzip, compress',
      'compress, deflate',
      'compress',
      'br',
      'gzip'
    ]

  def response(self, flow):
    if not 'html' in flow.response.headers.get('Content-Type', ""):
      return

    decompressedContent = self.get_content(flow)

    if decompressedContent is not None:
      utf8String = self.charset_normalizer(decompressedContent)
    else:
      utf8String = "Content could not be decompressed!"
    
    flow.response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    flow.response.text = self.parser.parse(utf8String)


  def decode(self, flow):
    i = 0
    # Retrieve an integer once, rather then creating overhead in the if statement
    decodingsLength = len(self.decodings)

    while True:
      #if charset_normalizer(flow.response.content)
      try:
        flow.request.headers.set('Content-encoding', self.encodings[i])
        # after setting new content-encoding header, let mitmproxy try to decode with the new header
        flow.response.content
      except:
        i += 1
        if i > decodingsLength:
          break

    return None

  def get_content(self, flow) -> Optional[bytes]:
      """
      Similar to `Message.content`, but does not raise if `strict` is `False`.
      Instead, the compressed message body is returned as-is.
      """
      if flow.response.raw_content is None:
          return None
      ce = flow.response.headers["Content-encoding"]##THSI WORKS PROGRESS TOMROW
      if ce:
          try:
              encoding = ContentDecoder()
              content = encoding.decode(flow, ce)
              return content
              # A client may illegally specify a byte -> str encoding here (e.g. utf8)
              if isinstance(content, str):
                  #return None
                  raise Exception("INSTANCE OF STR!")
              return content
          except:
              #return flow.response.raw_content
              raise Exception("TRY IN GET_CONTENT DID NOT WORK")
      else:
          #return flow.response.raw_content
          raise Exception("NO HEADER FOUND IN GET_CONTENT")

  def charset_normalizer(self, byte_string):
    result = CnM.from_bytes(
      byte_string,
      threshold = 0.2, #threshold has been explicitly set for further maintenance
      preemptive_behaviour=True,  # Determine if we should look into my_byte_str (ASCII-Mode) for pre-defined encoding
      explain=False  # Print on screen what is happening when searching for a match (FOR DEBUGGING PURPOSES)
    ).best().first() #keep only the matches with the lowest ratio of chaos, return the first list from the element

    if result is not None:
      #encode to UTF-8
      utf8String = str(result)
      return utf8String

    return None

addons = [
    Parser()
]