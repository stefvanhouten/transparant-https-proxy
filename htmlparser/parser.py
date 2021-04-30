from typing import Any, BinaryIO, Optional, Tuple
import html5lib
import lxml.etree as etree
import bleach
import os
class HTMLParser:
  def __init__(self, EXCLUDE: list):
    """Constructs and prepares the HTMLParser class to be ready for use.

    Args:
      EXCLUDE (list[str]): A list of strings containing the elements to not include into
                           the parser XML.
    """
    self.xml = ""
    self.html = ""
    self._formatted_xml_string = ""
    self.EXCLUDE = EXCLUDE
    TreeBuilder = html5lib.getTreeBuilder("lxml")
    self._parser = html5lib.HTMLParser(tree=TreeBuilder)
    self._tree_walker = html5lib.getTreeWalker('lxml')

  def parse(self, file: BinaryIO):
    """Parses the given HTML file to an XML file.

    Args:
      file (BinaryIO): The file to extract the HTML from
    Returns:
      string: The formatted XML string.
    """
    self.html, self._dom_tree = self._create_dom_tree(file)
    self._stream = self._tree_walker(self._dom_tree)

    self.xml = self._convert_html_to_xml()
    return self._pretty_xml()

  def _create_dom_tree(self, file: BinaryIO) -> Tuple[str, Any]:
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
      if item['type'] in INTERESTED_CHARACTERS:
        converted_html += bleach.clean(item['data'])
    return f'<?xml version="1.0"?><data>{converted_html}</data>'

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
        return self._build_img_tag(tag)

  def _build_start_tag(self, tag) -> Optional[str]:
    """Attempts to build the starting XML tag from the given HTML tag.

    Args:
      tag (dict): The HTML tag containing all the information from the tag.
    Returns:
      string: Formatted XML starting tag when a tag could be created, otherwise None.
    """
    tag_name = tag['name']
    if tag_name in self.EXCLUDE:
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
      new_tag += f'<{tag_name}>{value}</{tag_name}>'
    return f'<img>{new_tag}</img>'

  def _pretty_xml(self):
    root = etree.fromstring(self.xml)
    self._formatted_xml_string = str(etree.tostring(root, pretty_print=True).decode())
    FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(FOLDER, 'data/output.xml')
    with open(my_file, 'w+') as f:
      f.write(self._formatted_xml_string)
    return self._formatted_xml_string

EXCLUDE = (
  'script',
  'noscript',
  'html',
  )

# parser = HTMLParser(EXCLUDE)
# print(parser.parse('D:/devel/transparant-https-proxy/html-parser/data/index.html'))