import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


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
    def test_repr(self):
        leaf_node = LeafNode("h1", "This is a leaf node")
        self.assertEqual("LeafNode(h1, This is a leaf node, None)", repr(leaf_node))
        
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

class TestParentNode(unittest.TestCase):
    def test_repr(self):
        leaf_node = LeafNode("h2", "This is a leaf node")
        parent_node = ParentNode("h1", [leaf_node])
        self.assertEqual(
            "ParentNode(h1, [LeafNode(h2, This is a leaf node, None)], None)", repr(parent_node)
        )

    def test_one_leaf(self):
        leaf_node = LeafNode("h2", "This is a leaf node")
        parent_node = ParentNode("h1", [leaf_node])
        self.assertEqual(
            "<h1><h2>This is a leaf node</h2></h1>", parent_node.to_html()
        )

    def test_two_leaves(self):
        leaf1 = LeafNode("h2", "This is one leaf node")
        leaf2 = LeafNode("h2", "This is another leaf node")
        parent_node = ParentNode("h1", [leaf1, leaf2])
        self.assertEqual(
            "<h1><h2>This is one leaf node</h2><h2>This is another leaf node</h2></h1>", 
                parent_node.to_html()
        )

    def test_parent_in_parent(self):
        leaf_node = LeafNode("h2", "This is a leaf node")
        parent1 = ParentNode("h1", [leaf_node])
        parent2 = ParentNode("h1", [parent1])
        self.assertEqual(
            "<h1><h1><h2>This is a leaf node</h2></h1></h1>", parent2.to_html()
        )

if __name__ == "__main__":
    unittest.main()

