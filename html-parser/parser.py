import html5lib
import lxml.etree as etree
import bleach
import os

EXCLUDE = (
  'script',
  'noscript',
  'html',
  )

class HTMLParser:
  def __init__(self):
    self.xml = ""
    self.html = ""
    self._formatted_xml_string = ""

    TreeBuilder = html5lib.getTreeBuilder("lxml")
    self._parser = html5lib.HTMLParser(tree=TreeBuilder)
    self._tree_walker = html5lib.getTreeWalker('lxml')

  def parse(self, file):
    self.html, self._dom_tree = self._create_dom_tree(file)
    self._stream = self._tree_walker(self._dom_tree)

    self.xml = self._convert_html_to_xml()
    return self._pretty_xml()

  def _create_dom_tree(self, file):
    with open(file, 'rb') as f:
      html = f.read()
      dom_tree = self._parser.parse(html)
      return html, dom_tree

  def _convert_html_to_xml(self):
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

  def _build_tag(self, tag: dict) -> None:
    type = tag['type']
    if type == 'StartTag':
      return self._build_start_tag(tag)

    if type == 'EndTag':
      return self._build_end_tag(tag)

    if type == 'EmptyTag':
      if tag['name'] == 'img':
        return self._build_img_tag(tag)

  def _build_start_tag(self, tag):
    tag_name = tag['name']
    if tag_name in EXCLUDE:
      return
    return f'<{tag_name}>'

  def _build_end_tag(self, tag: dict) -> None:
    tag_name = tag['name']
    if tag_name in EXCLUDE:
      return
    return f'</{tag_name}>'

  def _build_img_tag(self, tag: dict):
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

parser = HTMLParser()
print(parser.parse('D:/devel/transparant-https-proxy/html-parser/data/index.html'))