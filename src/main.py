print("hello world")
from textnode import *
from file_based_functions import *
import sys

if len(sys.argv) > 1:
    base_path = sys.argv[1]
else:
    base_path = "/"

def main():
   #ob = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(ob)
    clean_b("docs")
    copy_from_a_to_b("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)


main()
