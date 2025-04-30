import unittest

from textnode import TextNode, TextType
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

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html(self):
        child1 = LeafNode("span", "Hello")
        child2 = LeafNode("span", "world")
        node = ParentNode("div", [child1, child2])
        self.assertEqual(node.to_html(), "<div><span>Hello</span><span>world</span></div>")

    def test_parent_to_html_no_tag(self):
        child1 = LeafNode("span", "Hello")
        child2 = LeafNode("span", "world")
        node = ParentNode(None, [child1, child2])
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_parent_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()