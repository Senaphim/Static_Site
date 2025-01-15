import unittest

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter


class testToHTML(unittest.TestCase):
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

class testSplitNodes(unittest.TestCase):
    def test_italics(self):
        textnode = TextNode(r"This is a *test* node", TextType.NORMAL)
        split_nodes = [TextNode("This is a ", TextType.NORMAL),
                       TextNode("test", TextType.ITALIC),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_delimiter([textnode], r"\*", TextType.ITALIC))

    def test_bold(self):
        textnode = TextNode(r"This is a **test** node", TextType.NORMAL)
        split_nodes = [TextNode("This is a ", TextType.NORMAL),
                       TextNode("test", TextType.BOLD),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_delimiter([textnode], r"\*\*", TextType.BOLD))

    def test_multiple_sections(self):
        textnode = TextNode(r"*This* is a *test* node", TextType.NORMAL)
        split_nodes = [TextNode("This", TextType.ITALIC),
                       TextNode(" is a ", TextType.NORMAL),
                       TextNode("test", TextType.ITALIC),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_delimiter([textnode], r"\*", TextType.ITALIC))

    def test_multiple_nodes(self):
        textnode1 = TextNode(r"This is a *test* node", TextType.NORMAL)
        textnode2 = TextNode(r"This is also a *test* node", TextType.NORMAL)
        node_list = [textnode1, textnode2]
        split_nodes = [TextNode("This is a ", TextType.NORMAL),
                       TextNode("test", TextType.ITALIC),
                       TextNode(" node", TextType.NORMAL),
                       TextNode("This is also a ", TextType.NORMAL),
                       TextNode("test", TextType.ITALIC),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_delimiter(node_list, r"\*", TextType.ITALIC))

if __name__ == "__main__":
    unittest.main()

