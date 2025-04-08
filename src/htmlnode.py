#import ?


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value 
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError(("Child classes must implement this method"))


    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        else:
            g = [f'{key}="{value}"' for key, value in self.props.items()]
            h = " ".join(g)
            j = " " + h
            return j         

    def __repr__(self):
        return(f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})")

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("All leafnodes must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value 
        props_list = [f'{key}="{value}"' for key, value in (self.props or {}).items()]
        props_string = " ".join(props_list)
        if self.props:
            opening_tag = f"<{self.tag} {props_string}>"
        else:
            opening_tag = f"<{self.tag}>"
        closing_tag = f"</{self.tag}>"
        html_setup = opening_tag + self.value + closing_tag
        return html_setup
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.original_children = children
        super().__init__(tag, None, children, props)    

    def to_html(self):
        if self.tag is None:
            raise ValueError("Must have a tag")
        
        if self.original_children is None:
            raise ValueError("Must have a child")
        
        start_tag = f"<{self.tag}{self.props_to_html()}>"
        end_tag = f"</{self.tag}>"

        if len(self.children) == 0:
            return start_tag + end_tag

        child_list = []
        for child in self.children:
            g = child.to_html()
            child_list.append(g)
        h = "".join(child_list)
        final_text = start_tag + h + end_tag
        return final_text            
        