import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("textbold", TextType.BOLD, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "textbold")

    def test_italic(self):
        node = TextNode("textitalic", TextType.ITALIC, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "textitalic")

    def test_code(self):
        node = TextNode("textcode", TextType.CODE, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "textcode")

    def test_link(self):
        node = TextNode("textlink", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "textlink")
        self.assertEqual(html_node.props["href"], "https://www.boot.dev")

    def test_link_with_none_url(self):
        node = TextNode("no url", TextType.LINK, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
        
    def test_link_with_empty_url(self):
        node = TextNode("empty url", TextType.LINK, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image(self):
        node = TextNode("", TextType.IMAGE, url="https://www.boot.dev/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"],"https://www.boot.dev/image.png") 
        self.assertIn("alt", html_node.props) # To check if the image provided an alt key

    def test_image_with_none_url(self):
        with self.assertRaises(ValueError):
            node = TextNode("", TextType.IMAGE, None)
            text_node_to_html_node(node)

    def test_image_with_empty_url(self):
        node = TextNode("", TextType.IMAGE, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
