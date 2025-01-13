import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertTrue(node != node2)

    def test_texttype_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertTrue(node != node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://bootdev.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertTrue(node != node2)

    def test_url_default_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()
