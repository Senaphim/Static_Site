import re

from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGES:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            ret.append(old_node)
            continue
        string_split = re.split(delimiter, node.text)
        if len(string_split) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        new_type = False
        for string in string_split:
            if string == "":
                new_type = not new_type
                continue
            if not new_type:
                ret.append(TextNode(string, node.text_type))
                new_type = True
            else:
                ret.append(TextNode(string, text_type))
                new_type = False
    return ret


def main():
    text_node = TextNode("This is a textnode", TextType.NORMAL, "https://www.boot.dev")

    print(text_node)

main()

