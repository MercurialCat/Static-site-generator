from textnode import TextNode, TextType
from markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = [] # This will be our final list and == a proper textnode that we can return. 
    for node in old_nodes:
        if node.text_type != TextType.NORMAL: # If the old node is already assigned anything other than normal text append.
            new_nodes.append(node)
        else:
            count = node.text.count(delimiter)
            if count % 2 != 0:
                raise Exception("Markdown delimiters not properly paired.")
            
            split = node.text.split(delimiter)
            for i, part in enumerate(split):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.NORMAL, None))
                else:
                    new_nodes.append(TextNode(part, text_type, None)) 

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            result = extract_markdown_images(node.text)
            if not result:
                new_nodes.append(node)
            else:
                if result:
                    first_result = result[0]
                    alt_text, image = first_result

                    markdown_pattern = f"![{alt_text}]({image})"
                    split = node.text.split(markdown_pattern, 1)
                    if split[0]:
                        new_nodes.append(TextNode(split[0], TextType.NORMAL, None)) # text before the image node if any

                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, image)) # image node 

                    if split[1]: 
                        last_node = TextNode(split[1], TextType.NORMAL, None) # any remaining text if any might need to work on this part
                        new_nodes.extend(split_nodes_image([last_node]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            result = extract_markdown_links(node.text)
            if not result:
                new_nodes.append(node)
            else:
                if result:
                    first_result = result[0]
                    link_text, url = first_result

                    markdown_pattern = f"[{link_text}]({url})"
                    split = node.text.split(markdown_pattern, 1)

                    if split[0]:
                        new_nodes.append(TextNode(split[0], TextType.NORMAL, None)) # text before the image node if any

                    new_nodes.append(TextNode(link_text, TextType.LINK, url)) # link node 

                    if split[1]: 
                        last_node = TextNode(split[1], TextType.NORMAL, None) # any remaining text if any might need to work on this part
                        new_nodes.extend(split_nodes_link([last_node]))
    return new_nodes
   
def text_to_textnodes(text):
    initial_node = [TextNode(text, TextType.NORMAL, None)] #initial node for our text

    #checking our nodes for delimiter attributes 
    node_bold_check = split_nodes_delimiter(initial_node, "**", TextType.BOLD)
    node_italic_check = split_nodes_delimiter(node_bold_check, "_", TextType.ITALIC)
    node_code_check = split_nodes_delimiter(node_italic_check, "`", TextType.CODE)

    #checking our nodes for images and links
    node_image_check = split_nodes_image(node_code_check)
    node_link_check = split_nodes_link(node_image_check)
    return node_link_check

    #can also get clean with it and just use g = split_nodes_link(split_nodes_image(split_nodes_delimiter(text)))