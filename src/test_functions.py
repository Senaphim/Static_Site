import unittest

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from main import (text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_link,
        split_nodes_image,
        text_to_textnodes,
        markdown_to_blocks,
        block_to_block_type)


class testTextNodeToHTML(unittest.TestCase):
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

    def test_split_link(self):
        textnode = TextNode(r"This is a [test](www.google.com) node", TextType.NORMAL)
        split_nodes = [TextNode("This is a ", TextType.NORMAL),
                       TextNode("test", TextType.LINKS, "www.google.com"),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_link([textnode]))

    def test_multiple_links(self):
        textnode = TextNode(r"This [is](www.boot.dev) a [test](www.google.com) node",
                            TextType.NORMAL)
        split_nodes = [TextNode("This ", TextType.NORMAL),
                       TextNode("is", TextType.LINKS, "www.boot.dev"),
                       TextNode(" a ", TextType.NORMAL),
                       TextNode("test", TextType.LINKS, "www.google.com"),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_link([textnode]))

    def test_split_image(self):
        textnode = TextNode(r"This is a ![test](www.google.com) node", TextType.NORMAL)
        split_nodes = [TextNode("This is a ", TextType.NORMAL),
                       TextNode("test", TextType.IMAGES, "www.google.com"),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_image([textnode]))

    def test_multiple_image(self):
        textnode = TextNode(r"This ![is](www.boot.dev) a ![test](www.google.com) node",
                            TextType.NORMAL)
        split_nodes = [TextNode("This ", TextType.NORMAL),
                       TextNode("is", TextType.IMAGES, "www.boot.dev"),
                       TextNode(" a ", TextType.NORMAL),
                       TextNode("test", TextType.IMAGES, "www.google.com"),
                       TextNode(" node", TextType.NORMAL)]
        self.assertEqual(split_nodes, split_nodes_image([textnode]))

class testExtractFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

class testTextToTextnode(unittest.TestCase):
    def test_all_nodetypes(self):
        text = r"This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        split_nodes = [TextNode("This is ", TextType.NORMAL),
                       TextNode("text", TextType.BOLD),
                       TextNode(" with an ", TextType.NORMAL),
                       TextNode("italic", TextType.ITALIC),
                       TextNode(" word and a ", TextType.NORMAL),
                       TextNode("code block", TextType.CODE),
                       TextNode(" and an ", TextType.NORMAL),
                       TextNode("obi wan image", TextType.IMAGES,
                                "https://i.imgur.com/fJRm4Vk.jpeg"),
                       TextNode(" and a ", TextType.NORMAL),
                       TextNode("link", TextType.LINKS, "https://boot.dev"),]
        self.assertEqual(split_nodes, text_to_textnodes(text))

class testMarkdownToBlocks(unittest.TestCase):
    def test_heading(self):
        markdown = "# This is a heading"
        blocks = ["# This is a heading"]
        self.assertEqual(blocks, markdown_to_blocks(markdown))

    def test_multiple_rawtext(self):
        markdown = "This is paragraph 1\n\nThis is paragraph 2\n\n\nThis is paragraph 3"
        blocks = ["This is paragraph 1",
                  "This is paragraph 2",
                  "This is paragraph 3"]
        self.assertEqual(blocks, markdown_to_blocks(markdown))

    def test_list(self):
        markdown = "* This is list item 1\n* This is list item 2\n* This is list item 3"
        blocks = ["* This is list item 1\n* This is list item 2\n* This is list item 3"]
        self.assertEqual(blocks, markdown_to_blocks(markdown))

    def test_combination(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = ["# This is a heading",
                  "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                  "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(blocks, markdown_to_blocks(markdown))

class testBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "##### This is a heading"
        block_type = "HEADING"
        self.assertEqual(block_type, block_to_block_type(block))

    def test_unordered_list(self):
        block = "- This is an unordered list\n- This is line 2\n- This is line 3"
        block_type = "UNORDERED LIST"
        self.assertEqual(block_type, block_to_block_type(block))

    def test_ordered_list(self):
        block = "1. This is an ordered list\n2. This is item 2\n3. This is item 3"
        block_type = "ORDERED LIST"
        self.assertEqual(block_type, block_to_block_type(block))

if __name__ == "__main__":
    unittest.main()

