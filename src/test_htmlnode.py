import unittest

from htmlnode import HTMLNode


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

