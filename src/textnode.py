from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
	PLAIN = "plain"
	BOLD = "bold"
	ITALICS = "italics"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"



class TextNode():
	def __init__(self, text, text_type=TextType.PLAIN, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url
	def __eq__(self, other):
		if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
			return True
		else:
			return False
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.PLAIN:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALICS:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})
		case _:
			return Exception("not valid type")

def extract_markdown_images(text):
	matches = re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) #the first part means it should not be preceded by !
	return matches



