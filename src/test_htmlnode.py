import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_href(self):
        node = HTMLNode(props={"href": "Testing stuff"})
        self.assertEqual(node.props_to_html(), ' href="Testing stuff"')

    def test_props_to_html_noteq(self):
        node = HTMLNode(props={"href": "Testing stuff"})
        self.assertNotEqual(node.props_to_html(), ' href="No match"')

    def test_props_to_html_empty(self):
        node = HTMLNode(props={}) 
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
    
    def test_leaf_to_html_none(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

if __name__ == "__main__":
    unittest.main()