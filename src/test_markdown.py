import unittest
from markdown_functions import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://i.imgur.com/zjjcJKZ.png)")

        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png"), 
            ("image2", "https://i.imgur.com/zjjcJKZ.png")
            ], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and another [to boot dev2](https://www.boot.dev/lessons/url2)")
                                         
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to boot dev2", "https://www.boot.dev/lessons/url2")
            ], matches)

    def test_mixed_content(self):
        test_case1 = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)")
        test_case2 = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)")

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], test_case1)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], test_case2)

    def test_empty_string(self):
        test_case1 = extract_markdown_images("")
        test_case2 = extract_markdown_links("")

        self.assertListEqual([], test_case1)
        self.assertListEqual([], test_case2)

    def test_malformed_markdown(self):
        test_case = "Here's a valid ![image](https://example.com) followed by malformed ones: ![missing closing](https://bad.com ![no-parentheses] [missing exclamation](https://wrong.com)"
        matches = extract_markdown_images(test_case)
        self.assertListEqual([("image", "https://example.com")], matches)

    def test_markdown_to_blocks(self):
        markdown = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ], )


    def test_markdown_to_multiple_blank_lines(self):
        markdown = """
    This is **bolded** paragraph

    

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",     
            ], )

    def test_empty_or_whitespace_only_docs(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("\n\n\n"), [])
        self.assertEqual(markdown_to_blocks("  \t\n\n  "), [])

    def test_single_block_docs(self):
        self.assertEqual(markdown_to_blocks("just one block"), ["just one block"])


    def test_heading_block(self): #this can probably be a loop but unsure of the method atm. This seems like a simple and clear example anyways
        heading1 = "# "
        heading2 = "## "
        heading3 = "### "
        heading4 = "#### "
        heading5 = "##### "
        heading6 = "###### "
        
        self.assertEqual(block_to_block_type(heading1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading4), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading5), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading6), BlockType.HEADING)

    def test_code_block(self):
        block = "``` jello ```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> I love jello\n> I hate jello"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- jello\n- sugar\n- love"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)   

    def test_ordered_list(self):
        block = "1. jello\n2. sugar\n3. love"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "I love jello"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()