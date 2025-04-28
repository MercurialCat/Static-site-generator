import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    # All delimiter splitting tests here
    def test_split_nodes_delimiter(self): #Basic test with a simple delimiter (e.g., **bold**)
        node = TextNode("This sentence has a **bold** word", TextType.NORMAL, None)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This sentence has a ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        
    def test_multiple_delimiter(self): #Test with multiple instances of the same delimiter (e.g., **bold** and **bold again**)
        node = TextNode("This text is **bold** and **bold again**", TextType.NORMAL, None)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "This text is ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        self.assertEqual(result[3].text, "bold again")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "")
        self.assertEqual(result[4].text_type, TextType.NORMAL)

    def test_empty_string_delimiter(self): #Test with an empty string between delimiters (e.g., ****)
        node = TextNode("wow empty **** bold", TextType.NORMAL, None)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "wow empty ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " bold")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_no_delimiters(self): #Test with no delimiters present
        node = TextNode("wow not a lot of delimiters here", TextType.NORMAL, None)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "wow not a lot of delimiters here")
        self.assertEqual(result[0].text_type, TextType.NORMAL)


    def test_unmatched_delimiters(self): #Test with unmatched delimiters (should raise an exception)
        node = TextNode("something seems **to be missing", TextType.NORMAL, None)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_non_text_node(self): #Test with a non-text node (should remain unchanged)
        node = TextNode("im already bold", TextType.BOLD, None)
        result = split_nodes_delimiter([node], "**", TextType.ITALIC)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "im already bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
                         

    def test_italic_delimiter(self): #Tests with different types of delimiters below (e.g., "`", "**", "_")
        node = TextNode("I swear im an _italian_ you gotta believe me!", TextType.NORMAL, None)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "I swear im an ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "italian")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " you gotta believe me!")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_code_delimiter(self):
        node = TextNode("This is valid `code` professor snape", TextType.NORMAL, None)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is valid ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " professor snape")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    # Our first basic test used bold as the base case so no need to check again.
    # Test cases that might need to be added in the future: test mixed node types, delims at the start or end of a string. 

class TestSplitNodesImage(unittest.TestCase):
    # All image splitting tests here
    def test_split_nodes_image_basic(self):
        node = TextNode("This is text with an ![image](https://example.com/img.png)", TextType.NORMAL, None)
        new_nodes = split_nodes_image([node])

        self.assertListEqual([
            TextNode("This is text with an ", TextType.NORMAL, None),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png")
            ], new_nodes)

    def test_split_nodes_no_image(self):
        node = TextNode("I seem to have lost my image...", TextType.NORMAL, None)
        new_node = split_nodes_image([node])

        self.assertListEqual([node], new_node)

    def test_split_image_multiple_images(self):
        node = TextNode("This is text with an ![image](https://example.com/img.png) and another ![image](https://example.com/img.png)", TextType.NORMAL, None)
        new_nodes = split_nodes_image([node])

        self.assertListEqual([
            TextNode("This is text with an ", TextType.NORMAL, None),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and another ", TextType.NORMAL, None),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png")
            ], new_nodes)

    def test_split_image_special_characters(self):
        node = TextNode("This node will have special ![im$age with spa©es](https://example.com/path/to/image%20with%20spaces.jpg)", TextType.NORMAL, None)
        new_nodes = split_nodes_image([node])

        self.assertListEqual([
            TextNode("This node will have special ", TextType.NORMAL, None),
            TextNode("im$age with spa©es", TextType.IMAGE, "https://example.com/path/to/image%20with%20spaces.jpg")
        ], new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    # All link splitting tests here    
    def split_nodes_link_basic_test(self):
        node = TextNode("This is text with an [link](https://www.boot.dev/dashboard)", TextType.NORMAL, None)
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("This is text with an ", TextType.NORMAL, None),
            TextNode("link", TextType.LINK, "https://www.boot.dev/dashboard")
            ], new_nodes)

    def test_split_nodes_no_link(self):
        node = TextNode("I seem to have lost my link...", TextType.NORMAL, None)
        new_node = split_nodes_link([node])

        self.assertListEqual([node], new_node)

    def test_split_link_multiple_links(self):
        node = TextNode("This is text with an [link](https://www.boot.dev/dashboard) and another [link](https://www.boot.dev/dashboard)", TextType.NORMAL, None)
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("This is text with an ", TextType.NORMAL, None),
            TextNode("link", TextType.LINK, "https://www.boot.dev/dashboard"),
            TextNode(" and another ", TextType.NORMAL, None),
            TextNode("link", TextType.LINK, "https://www.boot.dev/dashboard")
            ], new_nodes)
        
    def test_split_link_special_characters(self):
        node = TextNode("This node will have special [li$nk with spa©es](https://example.com/path/to/image%20with%20spaces.jpg)", TextType.NORMAL, None)
        new_nodes = split_nodes_link([node])

        self.assertListEqual([
            TextNode("This node will have special ", TextType.NORMAL, None),
            TextNode("li$nk with spa©es", TextType.LINK, "https://example.com/path/to/image%20with%20spaces.jpg")
        ], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual([
            TextNode("This is ", TextType.NORMAL, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.NORMAL, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.NORMAL, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an ", TextType.NORMAL, None),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL, None),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], new_nodes) 






























if __name__ == "__main__":
    unittest.main()

   