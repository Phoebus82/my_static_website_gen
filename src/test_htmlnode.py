import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import *

class TestTextNode(unittest.TestCase):
    def test_eq_url(self):
        node = HTMLNode("a", "this is a link", {"href":"https://www.google.com"})
        anode = HTMLNode("a", "this is a link", {"href":"https://www.google.com"})
        self.assertEqual(node, anode)
        
    def test_not_eq(self):
        node = HTMLNode("p", "this is some text")
        node3 = HTMLNode("a", "this is not some text")
        self.assertNotEqual(node, node3)

    def test_not_eq_tag(self):
        node = HTMLNode("a", "this is a link", {"href":"https://www.google.com"})
        node2 = HTMLNode("h1", "title")
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')

    def test_leaf_to_html_a_not(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertNotEqual(node.to_html(), '<a href="https://www.google.com">Hello, word!</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
    
    def test_to_html_with_mult_children(self):
        child_node = LeafNode(tag="b", value="child")
        child_node2 = LeafNode(tag="p", value="childish")
        parent_node = ParentNode("div", children=[child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><b>child</b><p>childish</p></div>",
            )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(
            ValueError,
            parent_node.to_html,
            )
        
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
    def test_title_extract(self):
        md = """
# Heeeey

>yoyoyo

### heeeey"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "Heeeey"
        )
    
    def test_another_title_extract(self):
        md = """
# Heeeey

>yoyoyo

# heeeey"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "Heeeey"
        )


if __name__ == "__main__":
    unittest.main()