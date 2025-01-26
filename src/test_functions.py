import unittest

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from markdown_blocks import (text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_link,
        split_nodes_image,
        text_to_textnodes,
        markdown_to_blocks,
        block_to_block_type,
        heading_block_to_html,
        code_block_to_html,
        quote_block_to_html,
        UL_block_to_html,
        OL_block_to_html,
        paragraph_block_to_html,
        markdown_to_html_node,
        extract_title)


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

    def test_text_bold_leading(self):
        text = r"**This** is text with bold at the beginning"
        split_nodes = [TextNode("This", TextType.BOLD),
                       TextNode(" is text with bold at the beginning", TextType.NORMAL)
                       ]
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

class testHeadingToHtml(unittest.TestCase):
    def test_heading(self):
        block = "#### This is a heading"
        htmlnode = ParentNode("h4", [LeafNode(None, "This is a heading")])
        self.assertEqual(htmlnode, heading_block_to_html(block))

    def test_heading_inline(self):
        block = "### This **is** a heading"
        htmlnode = ParentNode("h3", [LeafNode(None, "This "),
                              LeafNode("b", "is"),
                              LeafNode(None, " a heading")])
        self.assertEqual(htmlnode, heading_block_to_html(block))

class testCodeToHtml(unittest.TestCase):
    def test_code(self):
        block = "```\nThis is a code block\n```"
        htmlnode = ParentNode("pre", [
            ParentNode("code", [
                LeafNode(None, "This is a code block")
            ])
        ])
        self.assertEqual(htmlnode, code_block_to_html(block))

    def test_code_inline(self):
        block = "```\nThis **is** a code block\n```"
        htmlnode = ParentNode("pre", [
            ParentNode("code", [
                LeafNode(None, "This "),
                LeafNode("b", "is"),
                LeafNode(None, " a code block")
            ])
        ])
        self.assertEqual(htmlnode, code_block_to_html(block))

class testQuoteToHtml(unittest.TestCase):
    def test_quote(self):
        block = "> This is a quote"
        htmlnode = ParentNode("blockquote", [LeafNode(None, "This is a quote")])
        self.assertEqual(htmlnode, quote_block_to_html(block))

    def test_multiline_quote(self):
        block = "> This is a\n> MULTILINE\n> quote"
        htmlnode = ParentNode("blockquote", [LeafNode(None, "This is a\nMULTILINE\nquote")])
        self.assertEqual(htmlnode, quote_block_to_html(block))

    def test_quote_with_inline(self):
        block = "> This is a\n> **MULTILINE**\n> quote"
        htmlnode = ParentNode("blockquote", [
                              LeafNode(None, "This is a\n"),
                              LeafNode("b", "MULTILINE"),
                              LeafNode(None, "\nquote")
                              ])
        self.assertEqual(htmlnode, quote_block_to_html(block))

class testULToHtml(unittest.TestCase):
    def test_UL(self):
        block = "- This is an unordered list"
        htmlnode = ParentNode("ul", [ParentNode("li", 
                                                [LeafNode(None, "This is an unordered list")])
                                     ])
        self.assertEqual(htmlnode, UL_block_to_html(block))

    def test_multiline_UL(self):
        block = "- This is an unordered list\n- With two items"
        htmlnode = ParentNode("ul", [
                              ParentNode("li", [
                                  LeafNode(None, "This is an unordered list")]),
                              ParentNode("li", [
                                  LeafNode(None, "With two items")])
        ])
        self.assertEqual(htmlnode, UL_block_to_html(block))

    def test_multiline_UL_inline(self):
        block = "- This is an **unordered** list\n- With **two** items"
        htmlnode = ParentNode("ul", [
                              ParentNode("li", [
                                  LeafNode(None, "This is an "),
                                  LeafNode("b", "unordered"),
                                  LeafNode(None, " list")]),
                              ParentNode("li", [
                                  LeafNode(None, "With "),
                                  LeafNode("b", "two"),
                                  LeafNode(None, " items")])
        ])
        self.assertEqual(htmlnode, UL_block_to_html(block))

    def test_UL_inline_beginning(self):
        block = "- **This** is an unordered list"
        htmlnode = ParentNode("ul", [
                              ParentNode("li", [
                                  LeafNode("b", "This"),
                                  LeafNode(None, " is an unordered list")
                              ])
        ])
        self.assertEqual(htmlnode, UL_block_to_html(block))

class testOLToHtml(unittest.TestCase):
    def test_OL(self):
        block = "1. This is an ordered list"
        htmlnode = ParentNode("ol", [ParentNode("li", [
                              LeafNode(None, "This is an ordered list")])
        ])
        self.assertEqual(htmlnode, OL_block_to_html(block))

    def test_multiline_OL(self):
        block = "1. This is an ordered list\n2. With two items"
        htmlnode = ParentNode("ol", [
                              ParentNode("li", [
                                  LeafNode(None, "This is an ordered list")]),
                              ParentNode("li", [
                                  LeafNode(None, "With two items")])
        ])
        self.assertEqual(htmlnode, OL_block_to_html(block))

    def test_multiline_OL_inline(self):
        block = "1. This is an **ordered** list\n2. With **two** items"
        htmlnode = ParentNode("ol", [
                              ParentNode("li", [
                                  LeafNode(None, "This is an "),
                                  LeafNode("b", "ordered"),
                                  LeafNode(None, " list")]),
                              ParentNode("li", [
                                  LeafNode(None, "With "),
                                  LeafNode("b", "two"),
                                  LeafNode(None, " items")])
        ])
        self.assertEqual(htmlnode, OL_block_to_html(block))

class testParagraphToHtml(unittest.TestCase):
    def test_para(self):
        block = "This is a plain old paragraph"
        htmlnode = ParentNode("p", [LeafNode(None, "This is a plain old paragraph")])
        self.assertEqual(htmlnode, paragraph_block_to_html(block))

    def test_para_inline(self):
        block = "This is a **plain** old paragraph"
        htmlnode = ParentNode("p", [
                              LeafNode(None, "This is a "),
                              LeafNode("b", "plain"),
                              LeafNode(None, " old paragraph")
        ])
        self.assertEqual(htmlnode, paragraph_block_to_html(block))

class testMarkdownToHtmlNode(unittest.TestCase):
    def test_two_para(self):
        markdown = "This is paragraph one\n\nThis is paragraph two"
        htmlnode = ParentNode("div", [
                              ParentNode("p", [
                                  LeafNode(None, "This is paragraph one")]),
                              ParentNode("p", [
                                  LeafNode(None, "This is paragraph two")])
        ])
        self.assertEqual(htmlnode, markdown_to_html_node(markdown))

    def test_ol_para(self):
        markdown = "A paragraph\n\n1. Item one\n2. Item two\n\nSecond paragraph"
        htmlnode = ParentNode("div", [
                              ParentNode("p", [
                                  LeafNode(None, "A paragraph")]),
                              ParentNode("ol", [
                                  ParentNode("li", [
                                      LeafNode(None, "Item one")]),
                                  ParentNode("li", [
                                      LeafNode(None, "Item two")])
                                  ]),
                              ParentNode("p", [
                                  LeafNode(None, "Second paragraph")])
        ])
        self.assertEqual(htmlnode, markdown_to_html_node(markdown))

class testExtractHeader(unittest.TestCase):
    def test_header_extract(self):
        markdown = "# This is h1"
        string = "This is h1"
        self.assertEqual(string, extract_title(markdown))

    def test_header_multiline(self):
        markdown = "# This is h1\n\nThis is a paragraph"
        string = "This is h1"
        self.assertEqual(string, extract_title(markdown))

    def test_header_multiples(self):
        markdown = "# This is h1\n\n## This is h2"
        string = "This is h1"
        self.assertEqual(string, extract_title(markdown))

if __name__ == "__main__":
    unittest.main()

