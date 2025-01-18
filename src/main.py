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
            ret.append(node)
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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    ret = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            ret.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            ret.append(node)
            continue
        text = node.text
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                ret.append(TextNode(sections[0], TextType.NORMAL))
            ret.append(TextNode(link[0], TextType.LINKS, link[1]))
            text = sections[1]
        if text != "":
            ret.append(TextNode(sections[1], TextType.NORMAL))
    return ret

def split_nodes_image(old_nodes):
    ret = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            ret.append(node)
            continue
        links = extract_markdown_images(node.text)
        if len(links) == 0:
            ret.append(node)
            continue
        text = node.text
        for link in links:
            sections = text.split(f"![{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                ret.append(TextNode(sections[0], TextType.NORMAL))
            ret.append(TextNode(link[0], TextType.IMAGES, link[1]))
            text = sections[1]
        if text != "":
            ret.append(TextNode(sections[1], TextType.NORMAL))
    return ret

def text_to_textnodes(text):
    textnode = TextNode(text, TextType.NORMAL)
    ret = [textnode]
    ret = split_nodes_image(ret)
    ret = split_nodes_link(ret)
    ret = split_nodes_delimiter(ret, r"\*\*", TextType.BOLD)
    ret = split_nodes_delimiter(ret, r"\*", TextType.ITALIC)
    ret = split_nodes_delimiter(ret, r"`", TextType.CODE)
    return ret

def markdown_to_blocks(markdown):
    markdown_n = markdown + "\n\n"
    line_split = markdown_n.splitlines()
    final_lines = []
    i = 0
    while i < (len(line_split)):
        line = line_split[i]
        line = line.strip()
        if line == "":
            i = i + 1
            continue
        if line[0] == r"*":
            j = i + 1 
            while j < len(line_split):
                if line_split[j].strip() == "":
                    i = j
                    break
                if line_split[j][0] == r"*":
                    line += "\n" + line_split[j].strip()
                else:
                    i = j
                    break
                j += 1
        final_lines.append(line)
        i += 1
    return final_lines

def main():
    text_node = TextNode("This is a textnode", TextType.NORMAL, "https://www.boot.dev")

    print(text_node)

main()

