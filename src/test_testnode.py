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
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertTrue(node != node2)

    def test_url_default_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(
                "TextNode(This is a text node, Bold, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()
