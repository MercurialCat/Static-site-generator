from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"
	NORMAL = "normal"

class TextNode:
	def __init__(self, text, text_type, url):
		self.text = text 
		self.text_type = text_type
		self.url = url 

	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	
def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.NORMAL:
		return LeafNode(None, text_node.text)
	
	elif text_node.text_type == TextType.BOLD:
		return LeafNode("b", text_node.text)
	
	elif text_node.text_type == TextType.ITALIC:
		return LeafNode("i", text_node.text)
	
	elif text_node.text_type == TextType.CODE:
		return LeafNode("code", text_node.text)
	
	elif text_node.text_type == TextType.LINK:
		if not text_node.url:
			raise ValueError("Link type must include a valid url")
		return LeafNode("a", text_node.text, {"href" : text_node.url})
	
	elif text_node.text_type == TextType.IMAGE:
		if not text_node.url:
			raise ValueError("Image must be a valid src url")
		return LeafNode("img","",{"src": text_node.url, "alt": text_node.text})

	
	raise ValueError("Unknown TextType: please check your file and verify correct text_type")