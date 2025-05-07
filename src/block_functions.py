from blocknode import *
from htmlnode import *
from text_functions import *
import re

def markdown_to_blocks(markdown):
    new_blocks = []
    if markdown:
        split_markdown = markdown.split("\n\n")
        for block in split_markdown:
            # Strip whitespace from the entire block first
            block = block.strip()
            if block:
                # For multi-line blocks, normalize line indentation
                lines = block.split("\n")
                # Strip whitespace from each line
                normalized_lines = [line.strip() for line in lines]
                # Join the lines back together
                normalized_block = "\n".join(normalized_lines)
                new_blocks.append(normalized_block)
    return new_blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        lines = block.split("\n")
        if all(line == ">" or line.startswith("> ") for line in lines):
            return BlockType.QUOTE
    if block.startswith("- "):
        lines = block.split("\n")
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        lines = block.split("\n")
        if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_node = HTMLNode("div", None, [], None)  # Create the parent div node
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            div_node.children.append(convert_paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            div_node.children.append(convert_heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            div_node.children.append(convert_code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            div_node.children.append(convert_quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            div_node.children.append(convert_unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            div_node.children.append(convert_ordered_list_to_html_node(block))
    
    return div_node

def text_to_children(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)

    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def convert_paragraph_to_html_node(text):
    text = text.replace("\n", " ")
    children = text_to_children(text)
    return HTMLNode("p", None, children, None)

def convert_heading_to_html_node(text):
    h_number = 0
    for char in text:
        if char == "#":
            h_number += 1
        else:
            break
    content = text[h_number:].strip()
    return HTMLNode(f"h{h_number}", None, text_to_children(content), None)

def convert_code_to_html_node(text):
    lines = text.split("\n")
    content = "\n".join(lines[1:-1]) + "\n"
    text_node = TextNode(content, TextType.TEXT)
    plain_text = text_node_to_html_node(text_node)
    code_node = HTMLNode("code", None, [plain_text], None)
    return HTMLNode("pre", None, [code_node], None)

def convert_quote_to_html_node(text):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
    
def convert_unordered_list_to_html_node(text):
    items = text.split("\n")
    children = []
    for item in items:
        item = item.strip()
        if not item:  # Skip empty lines
            continue
        if item.startswith("- "):
            item = item[2:]  # Remove the "- " prefix
            children.append(HTMLNode("li", None, text_to_children(item), None))
    return HTMLNode("ul", None, children, None)

def convert_ordered_list_to_html_node(text):
    items = text.split("\n")
    children = []
    for item in items:
        item = item.strip()
        if not item:  # Skip empty lines
            continue
        # Check if it starts with a number followed by a period and space
        import re
        match = re.match(r"^\d+\.\s+(.*)", item)
        if match:
            item_content = match.group(1)
            children.append(HTMLNode("li", None, text_to_children(item_content), None))
    return HTMLNode("ol", None, children, None)