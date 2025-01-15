import unittest

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from main import text_node_to_html_node


class testFunctions(unittest.TestCase):
    def test_text(self):
        textnode = TextNode("This is a test node", TextType.NORMAL)
        leafnode = LeafNode(None, "This is a test node")
        self.assertEqual(leafnode, text_node_to_html_node(textnode))
        
    def test_link(self):
        textnode = TextNode("This is a test node", TextType.LINKS, "www.google.com")
        leafnode = LeafNode("a", "This is a test node", {"href": "www.google.com"})
        self.assertEqual(leafnode, text_node_to_html_node(textnode))

    def test_picture(self):
        textnode = TextNode("This is a test node", TextType.IMAGES, "www.google.com")
        leafnode = LeafNode("img", "", {"src": "www.google.com", "alt": "This is a test node"})
        self.assertEqual(leafnode, text_node_to_html_node(textnode))

if __name__ == "__main__":
    unittest.main()

