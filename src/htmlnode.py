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