import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
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


    #our first basic test used bold as the base case so no need to check again.
    
    #Test cases that might need to be added in the future: test mixed node types, delims at the start or end of a string. 