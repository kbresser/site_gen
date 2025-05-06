import unittest

from textnode import TextNode, TextType
from text_functions import *
from block_functions import *
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_txt(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_dif_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_html_format(self):
        node = HTMLNode("a", "This is a text node", props={"href": "https://www.boot.dev"})
        node2 = HTMLNode("a", "This is a different text node", props={"href": "https://www.boot.dev"})
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_to_textnodes_mixed_markdown(self):
        input_str = "This is **bold** and _italic_ and `code` and ![img](img.png) and [link](example.com)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "example.com"),
        ]
        output = text_to_textnodes(input_str)
        self.assertEqual(output, expected)

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_leaf_to_html_no_value(self):
        # Create a LeafNode with a tag but no value
        node = LeafNode("p", None)
        # The expected result should be an empty paragraph tag
        self.assertEqual(node.to_html(), "<p></p>")

    def test_parent_to_html_with_children(self):
        # Create a parent node with two child nodes
        parent = ParentNode("div", [
            LeafNode("p", "First child"),
            LeafNode("p", "Second child")
        ])
        
        # The expected output should have both children properly nested in the parent
        expected_html = "<div><p>First child</p><p>Second child</p></div>"
        self.assertEqual(parent.to_html(), expected_html)
    
    def test_parent_to_html_no_children(self):
        # Create a parent node with no children
        parent = ParentNode("div", [])
        
        # The expected output should be an empty div tag
        expected_html = "<div></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\nprint('Hello, World!')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> on multiple lines"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_bock_to_block_type_order_skipped(self):
       block = "1. Item 1\n3. Item 2\n4. Item 3"
       block_type = block_to_block_type(block)
       self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_bock_to_block_type_order_skipped(self):
       block = "3. Item 1\n4. Item 2\n5. Item 3"
       block_type = block_to_block_type(block)
       self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_bock_to_block_type_order_whitespace(self):
       block = " 1. Item 1\n2. Item 2\n3. Item 3"
       block_type = block_to_block_type(block)
       self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        input_str = "# This is a title"
        expected_title = "This is a title"
        title = extract_title(input_str)
        self.assertEqual(title, expected_title)

    def test_extract_bad_title(self):
        with self.assertRaises(ValueError):
            input_str = "This is not a title"
            title = extract_title(input_str)

    def test_extract_bad_title2(self):
        with self.assertRaises(ValueError):
            input_str = "## This is not a title"
            title = extract_title(input_str)




if __name__ == "__main__":
    unittest.main()