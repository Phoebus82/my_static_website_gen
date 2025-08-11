from textnode import *
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type.value != "plain":
            nodes.append(node)
        else:
            split_by_delimiter_list = node.text.split(delimiter)
            if len(split_by_delimiter_list) % 2 == 0:
                 raise Exception("improper markdown syntax, make sure to have matching delimiters")
            for i in range(0, len(split_by_delimiter_list)):
                if i % 2 == 0:
                        k = TextNode(split_by_delimiter_list[i], TextType.PLAIN)
                        if k.text != "":
                            nodes.append(k)
                else:
                    k = TextNode(split_by_delimiter_list[i], text_type)
                    nodes.append(k)
    return nodes

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type.value != "plain":
            nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text):
            if match.start() > last_index:
                plain = text[last_index:match.start()]
                if plain:
                    nodes.append(TextNode(plain, TextType.PLAIN))
            alt = match.group(1)
            url = match.group(2)
            nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_index = match.end()
        if last_index < len(text):
            plain = text[last_index:]
            if plain:
                nodes.append(TextNode(plain, TextType.PLAIN))
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type.value != "plain":
            nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text):
            if match.start() > last_index:
                plain = text[last_index:match.start()]
                if plain:
                    nodes.append(TextNode(plain, TextType.PLAIN))
            alt = match.group(1)
            url = match.group(2)
            nodes.append(TextNode(alt, TextType.LINK, url))
            last_index = match.end()
        if last_index < len(text):
            plain = text[last_index:]
            if plain:
                nodes.append(TextNode(plain, TextType.PLAIN))
    return nodes

def text_to_textnodes(text):
    return split_nodes_link(split_nodes_image(split_nodes_delimiter((
        split_nodes_delimiter(
            split_nodes_delimiter([TextNode(text, TextType.PLAIN)],"**", TextType.BOLD), 
        "_", TextType.ITALICS)), 
        "`", TextType.CODE)))
    









'''
This would be my solution

old_nodes = [TextNode(
    "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) yeahy",
    TextType.PLAIN,
)]
nodes = []
for node in old_nodes:
    if extract_markdown_images(node.text) == []:
        text = TextNode(node.text, TextType.PLAIN)
        nodes.append(text)
    while extract_markdown_images(node.text) != []:
        matches = extract_markdown_images(node.text)
        sections = node.text.split(f"![{matches[0][0]}]({matches[0][1]})", 1)
        if sections[0] != "":
            text = TextNode(sections[0], TextType.PLAIN)
            nodes.append(text)
        img = TextNode(matches[0][0], TextType.IMAGE, matches[0][1])
        nodes.append(img)
        node.text = sections[1]
        if node.text != "" and extract_markdown_images(node.text) == []:
            text = TextNode(node.text, TextType.PLAIN)
            nodes.append(text)
        if node.text != "":
            nodes.append(node.text)
    print(nodes)

'''