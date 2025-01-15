import unittest

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from main import text_node_to_html_node


class testFunctions(unittest.TestCase):
    def test_text(self):
        textnode = TextNode("This is a test node", TextType.NORMAL)
        leafnode = LeafNode(None, "This is a test node")
        self.assertEqual(leafnode, text_node_to_html_node(textnode))
        

if __name__ == "__main__":
    unittest.main()

