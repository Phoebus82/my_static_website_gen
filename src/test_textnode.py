import unittest
from textnode import *
from split_nodes import *
from blocks import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.ITALICS)
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node3)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,"https://www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "/images")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props_to_html(), ' src="/images" alt="This is an image"')

    def test_split_delimiter(self):
        node = TextNode("This is a text with two **bold** blocks **hey**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with two ", TextType.PLAIN),
    TextNode("bold", TextType.BOLD),
    TextNode(" blocks ", TextType.PLAIN),
    TextNode("hey", TextType.BOLD),

        ])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with an [link](https://boot.dev)"
    )
        self.assertListEqual([("link", "https://boot.dev")], matches)
    
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN,
    )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
    def test_split_link(self):
        node = TextNode(
        "This is text with an [link](https://google.com) and another [link2](https://gogo.com)",
        TextType.PLAIN,
    )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://google.com"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "link2", TextType.LINK, "https://gogo.com"
            ),
        ],
        new_nodes,
    )
    def test_text_to_textnodes(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png) I _love_ you **Ellie** and this is an ![image](https://i.imgur.com/zjjcJKZ.png) and **this** is a [link](https://gogo.com) that _shows_ it"
        self.assertListEqual(
            [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" I ", TextType.PLAIN),
            TextNode("love", TextType.ITALICS),
            TextNode(" you ", TextType.PLAIN),
            TextNode("Ellie", TextType.BOLD),
            TextNode(" and this is an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("this", TextType.BOLD),
            TextNode(" is a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://gogo.com"),
            TextNode(" that ", TextType.PLAIN),
            TextNode("shows", TextType.ITALICS),
            TextNode(" it", TextType.PLAIN),
            ]
            ,text_to_textnodes(text))
        

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

    def test_block_to_block_type(self):
        md = """
>This is **bolded** paragraph

## This is another paragraph with _italic_ text and `code` here

``` This is the same paragraph on a new line ```

- This is a list
- with items

1. jfd
2. 313
3. fjds

fdskfahksfash
    """
        listo = []
        blocks = markdown_to_blocks(md)
        for i in blocks:
            listo.append(block_to_block_type(i))
        self.assertListEqual(
            listo,
            [BlockType.QUOTE, BlockType.HEADING, BlockType.CODE, BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST, BlockType.PARAGRAPH]
        )

        
        
if __name__ == "__main__":
    unittest.main()