import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "Some text")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>Some text</span></div>')

    def test_to_html_for_missing_tag_(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", "hello")
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()
    
    def test_to_html_for_missing_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", None)
            parent_node.to_html()

    def test_to_html_for_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_for_mixed_nodes(self):
        step_child = LeafNode("b", "stepchild")
        child_node = LeafNode("i", "child")
        parent_node = ParentNode("span", [step_child])
        grandparent_node = ParentNode("div", [parent_node, child_node])
        self.assertEqual(grandparent_node.to_html(), "<div><span><b>stepchild</b></span><i>child</i></div>") 

if __name__ == "__main__":
    unittest.main()