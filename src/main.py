print("hello world")
from textnode import *
from file_based_functions import *
def main():
   #ob = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(ob)
    clean_b("public")
    copy_from_a_to_b("static", "public")
    generate_pages_recursive("content", "template.html", "public")

    
main()
