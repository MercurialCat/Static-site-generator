import unittest
from markdown import extract_markdown_images, extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()