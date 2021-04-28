import html5lib
import lxml.etree as etree
import bleach
import os

LOOKUP = {
  'p': 'text',
  'div':'content',
}
class HTMLParser:
  def __init__(self, file):
    self.html = ""
    self.xml = ""
    self._formatted_xml_string = ""

    self._file = file
    TreeBuilder = html5lib.getTreeBuilder("lxml")
    self._parser = html5lib.HTMLParser(tree=TreeBuilder)
    self._tree_walker = html5lib.getTreeWalker('lxml')
    self._dom_tree = self._create_dom_tree()
    self._stream = self._tree_walker(self._dom_tree)
    self._convert_html_to_xml()
    self._pretty_xml()

  def _create_dom_tree(self):
    with open(self._file, 'rb') as f:
      self.html = f.read()
      return self._parser.parse(self.html)

  def _convert_html_to_xml(self):
    self.xml += '<?xml version="1.0"?><data>'
    for item in self._stream:
      if 'name' in item:
        self._build_tag(item)
      else:
        if item['type'] in ('Characters', 'SpecialCharacters',):
          self.xml += bleach.clean(item['data'])
    self.xml += '</data>'

  def _build_tag(self, tag: dict) -> None:
    if tag['type'] == 'StartTag':
      self._build_start_tag(tag)
    elif tag['type'] == 'EndTag':
      self._build_end_tag(tag)

  def _build_start_tag(self, tag):
    converted_tag = LOOKUP.get(tag['name'], tag['name'])
    if converted_tag in ('script', 'noscript',):
      return
    self.xml += f'<{converted_tag}>'

  def _build_end_tag(self, tag: dict) -> None:
    converted_tag = LOOKUP.get(tag['name'], tag['name'])
    if converted_tag in ('script', 'noscript',):
      return
    self.xml += f'</{converted_tag}>'

  def _pretty_xml(self):
    root = etree.fromstring(self.xml)
    self._formatted_xml_string = etree.tostring(root, pretty_print=True).decode()
    FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(FOLDER, 'data/output.xml')
    with open(my_file, 'w+') as f:
      f.write(str(self._formatted_xml_string))

HTMLParser('D:/devel/transparant-https-proxy/html-parser/data/index.html')