import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node3 = TextNode("This is not a text node", TextType.BOLD, url=None)
        self.assertNotEqual(node, node3)

    def test_text_type_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node4 = TextNode("This is a text node", TextType.ITALIC, url=None)
        self.assertNotEqual(node, node4)

    def test_not_equal_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node5 = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev")
        self.assertNotEqual(node,node5)

if __name__ == "__main__":
    unittest.main()
