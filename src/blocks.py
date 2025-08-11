from enum import Enum
from htmlnode import *
from textnode import *
from split_nodes import text_to_textnodes, text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = []
    initial = [string.strip() for string in markdown.split("\n\n")]
    for i in initial:
        if i != "":
            blocks.append(i)
    return blocks


class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered list"
	ORDERED_LIST = "ordered list"
      
def block_to_block_type(markdown_block):
    for times in range(1, 7):
        hashtag = "#" * times
        if markdown_block.startswith(f"{hashtag} "):
            return BlockType.HEADING
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
         return BlockType.CODE
    linesplit = markdown_block.split("\n")
    quote_block = bool_block_type(linesplit, ">", BlockType.QUOTE)
    if quote_block is not None:
        return quote_block
    unordered_list_block = bool_block_type(linesplit, "- ", BlockType.UNORDERED_LIST)
    if unordered_list_block is not None:
        return unordered_list_block
    count = 1
    success_timer = 0
    for line in linesplit:
        if not line.startswith(f"{count}. "):
            break
        else:
            success_timer += 1
        count += 1
     
    if success_timer == len(linesplit):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def bool_block_type(line_list, characteristic, blocktype):
    if not line_list:
        return None
    for line in line_list:
        if not line.startswith(characteristic):
            return None
    return blocktype

def markdown_to_html_node(markdown):
    supernodelist= []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        child_nodes = []
        blocktype = block_to_block_type(block)
        tag = block_to_tag(block, blocktype)
        if blocktype != BlockType.CODE:
            if blocktype == BlockType.UNORDERED_LIST or blocktype == BlockType.ORDERED_LIST:
                for i in split_n_strip_list_blocks(block, blocktype):
                    if i != "":
                        child_nodes.append(ParentNode("li", text_to_children(i)))
            else:
                if blocktype == BlockType.QUOTE:
                    lines = [line.lstrip("> ").rstrip() for line in block.split("\n")]
                    block = " ".join(lines)
                elif blocktype == BlockType.HEADING:
                    position = 0
                    while position < len(block) and block[position] == "#":
                        position += 1
                    block = block[position:].strip()
                else:  
                    block = block.replace("\n", " ")  
                html_list = text_to_children(block)
                for node in html_list:
                    child_nodes.append(node)
        else:
            block = block.replace("```", "").lstrip("\n")
            child_nodes.append(text_node_to_html_node(TextNode(block, TextType.CODE)))
        
        overnode = ParentNode(tag, child_nodes)
        supernodelist.append(overnode)
    supernode = ParentNode("div", supernodelist)
    return supernode

def text_to_children(block):
    html_list = [text_node_to_html_node(node) for node in text_to_textnodes(block)]
    return html_list
def split_n_strip_list_blocks(block, blocktype):
    match blocktype:
        case BlockType.UNORDERED_LIST:
            blocklist = [i.lstrip("- ") for i in block.split("\n")]
            return blocklist
        case BlockType.ORDERED_LIST:
            blocklist = block.split("\n")
            for ind, val in enumerate(blocklist):
                space_index = val.find(" ")
                if space_index != -1:
                    blocklist[ind] = val[space_index + 1:]
            return blocklist

def block_to_tag(block, blocktype):
    match blocktype:
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.CODE:
            return "pre"
        case BlockType.HEADING:
            num = block.count("#")
            return f"h{num}"
        case BlockType.PARAGRAPH:
            return "p"
        case _:
            return Exception("not valid type")


            
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith("# "):
            block = block[2:].strip()
            return block
        else:
            raise Exception("Missing title")
        



                  
            
           