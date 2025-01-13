import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1", "This is a htmlnode", [], {"href": "https://google.com"})
        self.assertEqual(
            "HTMLNode(h1, This is a htmlnode, [], {'href': 'https://google.com'})", repr(node)
        )

    def test_default_to_none(self):
        node = HTMLNode()
        self.assertEqual(None, node.tag)
        self.assertEqual(None, node.value)
        self.assertEqual(None, node.children)
        self.assertEqual(None, node.props)

    def test_props_to_html(self):
        node = HTMLNode(props = {"href": "https://google.com"})
        self.assertEqual(" href=\"https://google.com\"", node.props_to_html())
        node2 = HTMLNode()
        self.assertEqual("", node2.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf_node = LeafNode("h1", "This is a leaf node", {"href": "https://goggle.com"})
        self.assertEqual(
            "<h1 href=\"https://goggle.com\">This is a leaf node</h1>", leaf_node.to_html()
        )

    def test_no_children(self):
        leaf_node = LeafNode("h1", "This is a leaf node")
        self.assertEqual(None, leaf_node.children)

    def test_no_tag(self):
        leaf_node = LeafNode(None, "This is a leaf node")
        self.assertEqual("This is a leaf node", leaf_node.to_html())

if __name__ == "__main__":
    unittest.main()

