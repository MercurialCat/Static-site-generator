from textnode import TextNode, TextType

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
    