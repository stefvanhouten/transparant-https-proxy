from typing import Any, BinaryIO, Optional, Tuple
import html5lib
import lxml.etree as etree
import bleach
import os
import re

def str_to_int(s, default, base=10):
  if int(s, base) < 0x10000:
      return chr(int(s, base))
  return default

def remove_control_characters(html):
  html = re.sub(r"&#(\d+);?", lambda c: str_to_int(c.group(1), c.group(0)), html)
  html = re.sub(r"&#[xX]([0-9a-fA-F]+);?", lambda c: str_to_int(c.group(1), c.group(0), base=16), html)
  html = re.sub(r"[\x00-\x08\x0b\x0e-\x1f\x7f]", "", html)
  return html

class HTMLParser:
  def __init__(self, EXCLUDE: list):
    """Constructs and prepares the HTMLParser class to be ready for use.

    Args:
      EXCLUDE (list[str]): A list of strings containing the elements to not include into
                           the parser XML.
    """
    self.xml = ""
    self.html = ""
    self.skipping_tag = False
    self._formatted_xml_string = ""
    self.EXCLUDE = EXCLUDE
    TreeBuilder = html5lib.getTreeBuilder("lxml")
    self._parser = html5lib.HTMLParser(tree=TreeBuilder)
    self._tree_walker = html5lib.getTreeWalker('lxml')

  def parse(self, file: str, output_location: str=None, pretty_xml: bool=True) -> str:
    """Parses the given HTML file to an XML file.

    Args:
      file (string): The path to the HTML file or the HTML as a string.
      output_location (string, optional): The path to the file where the output should be saved. Defaults to None.
      pretty_xml (bool): Determines whether the output is prettified or not.
    Returns:
      string: The formatted XML string.
    """
    # file = remove_control_characters(file)
    self.html, self._dom_tree = self._create_dom_tree(file)
    self._stream = self._tree_walker(self._dom_tree)

    self.xml = self._convert_html_to_xml()
    # with open(output_location, 'w+') as f:
    #   f.write(self.xml)
    return self._pretty_xml(output_location, pretty_xml)

  def _create_dom_tree(self, file: str) -> Tuple[str, Any]:
    """Determines whether the given string is a path or the HTML, then either reads the file or converts
    the given HTML the a dom tree.

    Args:
      file (string): The path to the file or the HTML as a string.
    Returns:
     Tuple[string, domtree]: Tuple containing the raw HTML and a the HTML in the form of a dom tree.
    """
    if os.path.exists(os.path.dirname(file)):
      return self._create_dom_tree_from_file(file)

    dom_tree = self._parser.parse(file)
    return file, dom_tree

  def _create_dom_tree_from_file(self, file: BinaryIO) -> Tuple[str, Any]:
    """Reads the HTML file an creates a dom tree like object.

    Args:
      file (BinaryIO): The file to extract the HTML from
    Returns:
      tuple[string, domtree]: Tuple containing the HTML and the parsed HTML in the form of a dom tree.
    """
    with open(file, 'rb') as f:
      html = f.read()
      dom_tree = self._parser.parse(html)
      return html, dom_tree

  def _convert_html_to_xml(self) -> str:
    """Attempts to convert HTML to XML and filters out elements from the blocklist.

    Returns:
      string: Unformatted XML string.
    """
    INTERESTED_CHARACTERS = ('Characters', 'SpecialCharacters',)

    converted_html = ""
    for item in self._stream:
      if 'name' in item:
        tag = self._build_tag(item)
        if tag is not None:
          converted_html += tag
        continue
      if item['type'] in INTERESTED_CHARACTERS and not self.skipping_tag:
        converted_html += bleach.clean(item['data'])
    return f'<data>{converted_html}</data>'

  def _build_tag(self, tag: dict) -> Optional[str]:
    """Attempts to build a XML tag for given HTML tag.

    Args:
      tag (dict): The HTML tag containing all the information from the tag.
    Returns:
      string: Formatted XML tag when a tag could be created, otherwise None.
    """
    type = tag['type']
    if type == 'StartTag':
      return self._build_start_tag(tag)

    if type == 'EndTag':
      return self._build_end_tag(tag)

    if type == 'EmptyTag':
      if tag['name'] == 'img':
        return
        return self._build_img_tag(tag)

  def _build_start_tag(self, tag) -> Optional[str]:
    """Attempts to build the starting XML tag from the given HTML tag.

    Args:
      tag (dict): The HTML tag containing all the information from the tag.
    Returns:
      string: Formatted XML starting tag when a tag could be created, otherwise None.
    """
    self.skipping_tag = False
    tag_name = tag['name']
    if tag_name in self.EXCLUDE:
      self.skipping_tag = True
      return
    return f'<{tag_name}>'

  def _build_end_tag(self, tag: dict) -> Optional[str]:
    """Attempts to build the ending XML tag from the given HTML tag.

    Args:
      tag (dict): The HTML tag containing all the information from the tag.
    Returns:
      string: Formatted XML ending tag when a tag could be created, otherwise None.
    """
    tag_name = tag['name']
    if tag_name in self.EXCLUDE:
      self.skipping_tag = False
      return
    return f'</{tag_name}>'

  def _build_img_tag(self, tag: dict) -> str:
    """Attempts to build an img XML tag from the given HTMl tag.

    Args:
      tag (dict): The HTML tag containing all the information from the tag.
    Returns:
      string: Formatted IMG tag containing attributes such as src and alt.
    """

    new_tag = ""
    for tag, value in tag['data'].items():
      _, tag_name = tag
      new_tag += f'<{tag_name}>{bleach.clean(value)}</{tag_name}>'
    return f'<img>{new_tag}</img>'

  def _pretty_xml(self, output_location, pretty_xml):
    root = etree.fromstring(self.xml)
    self._formatted_xml_string = str(etree.tostring(root, pretty_print=True).decode())

    if output_location is not None:
      with open(output_location, 'w+') as f:
        if pretty_xml:
          f.write(self._formatted_xml_string)
        else:
          f.write(self.xml)

    if pretty_xml:
      return self._formatted_xml_string
    return self.xml

# EXCLUDE = (
#   'script',
#   'style',
#   'noscript',
#   # 'html',
#   )

# parser = HTMLParser(EXCLUDE)
# f = open("/home/stef/devel/transparant-https-proxy/sample.html", "r")
# parser.parse(f.read(), output_location="/home/stef/devel/transparant-https-proxy/output.html")

# # data = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta http-equiv="X-UA-Compatible" content="IE=edge">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Document</title>
# </head>
# <body>
#   <p>test</p>
#   <section>
#     <p>Content 1</p>
#   </section>
#   <section>
#     <div>
#       <p>Content 2</p>
#       <img src="test.png" alt="test">
#     </div>
#   </section>
# </body>
# </html>
# """
# print(parser.parse(data))
