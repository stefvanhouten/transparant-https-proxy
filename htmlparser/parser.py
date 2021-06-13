import os
from typing import Any, BinaryIO, List, Optional, Tuple

import bleach
import html5lib
import lxml.etree as etree

class HTMLParser:
    def __init__(self, exclude: List[str], keep_attributes: bool = True):
        """Constructs and prepares the HTMLParser class to be ready for use.

        Args:
          exclude (list[str]): A list of strings containing the elements to not include into
                               the parser XML.
          keep_attributes (bool): Determines whether or not to add HTML tag attributes to the XML output.
                                  Default value is True.
        """
        self.xml = ""
        self.html = ""
        self._formatted_xml_string = ""
        self.keep_attributes = keep_attributes
        self.skipping_tag = False
        self.exclude = exclude

        self._parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("lxml"))
        self._tree_walker = html5lib.getTreeWalker("lxml")

    def parse(
        self, file: str
    ) -> str:
        """Parses the given HTML file to an XML file.

        Args:
          file (string): The path to the HTML file or the HTML as a string.
        Returns:
          string: The formatted XML string.
        """
        self.html, self._dom_tree = self._create_dom_tree(file)
        self._stream = self._tree_walker(self._dom_tree)
        self.xml = self._convert_html_to_xml()
        return self.xml

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
        with open(file, "rb") as f:
            html = f.read()
            dom_tree = self._parser.parse(html)
            return html, dom_tree

    def _convert_html_to_xml(self) -> str:
        """Attempts to convert HTML to XML and filters out elements from the blocklist.

        Returns:
          string: Unformatted XML string.
        """
        INTERESTED_CHARACTERS = (
            "Characters",
            "SpecialCharacters",
        )

        converted_html = ""
        for item in self._stream:
            if "name" in item:
                tag = self._build_tag(item)
                if tag is not None:
                    converted_html += tag
                continue

            if item["type"] in INTERESTED_CHARACTERS and not self.skipping_tag:
                converted_html += bleach.clean(item["data"])
        return f"<data>{converted_html}</data>"

    def _build_tag(self, tag: dict) -> Optional[str]:
        """Attempts to build a XML tag for given HTML tag.

        Args:
          tag (dict): The HTML tag containing all the information from the tag.
        Returns:
          string: Formatted XML tag when a tag could be created, otherwise None.
        """
        type = tag["type"]
        if type == "StartTag":
            return self._build_start_tag(tag)

        if type == "EndTag":
            return self._build_end_tag(tag)

        if type == "EmptyTag":
            if tag["name"] == "img":
                return self._build_img_tag(tag)

    def _build_start_tag(self, tag) -> Optional[str]:
        """Attempts to build the starting XML tag from the given HTML tag.

        Args:
          tag (dict): The HTML tag containing all the information from the tag.
        Returns:
          string: Formatted XML starting tag when a tag could be created, otherwise None.
        """
        tag_name = tag["name"]

        if tag_name in self.exclude or self.skipping_tag:
            self.skipping_tag = True
            return

        if self.keep_attributes and tag["data"]:  # Contains the attributes of a tag
            attributes = self._extract_attributes(tag["data"])
            if attributes:
                return f"<{tag_name} {attributes}>"
        return f"<{tag_name}>"

    def _extract_attributes(self, attributes):
        """Extracts attributes out of a tag.

        Args:
          attributes (OrderedDict): The dict containing the attribute name and the value.
        Returns:
          string: Formatted string containing the tag name and value in the following format: tag="value"
        """
        extracted_attributes = []
        for key, value in attributes.items():
            _, attribute = key
            if attribute in ("class", "href", "id"):
                # XXX: Quotes are an issue here, however they shouldn't be in HTML attributes. This doesn't mean they wont be there though :).
                # if attribute == 'href':
                #   print(value)
                extracted_attributes.append(f"{attribute}='{bleach.clean(value)}'")
        if len(extracted_attributes) >= 1:
            return " ".join(extracted_attributes)

    def _build_end_tag(self, tag: dict) -> Optional[str]:
        """Attempts to build the ending XML tag from the given HTML tag.

        Args:
          tag (dict): The HTML tag containing all the information from the tag.
        Returns:
          string: Formatted XML ending tag when a tag could be created, otherwise None.
        """
        tag_name = tag["name"]

        if tag_name in self.exclude:
            self.skipping_tag = False
            return

        if self.skipping_tag:
            return

        return f"</{tag_name}>"

    def _build_img_tag(self, tag: dict) -> str:
        """Attempts to build an img XML tag from the given HTMl tag.

        Args:
          tag (dict): The HTML tag containing all the information from the tag.
        Returns:
          string: Formatted IMG tag containing attributes such as src and alt.
        """

        new_tag = ""
        for tag, value in tag["data"].items():
            _, tag_name = tag
            new_tag += f"<{tag_name}>{bleach.clean(value)}</{tag_name}>"
        return f"<img>{new_tag}</img>"