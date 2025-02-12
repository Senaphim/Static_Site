class HTMLNode():

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props 

    def to_html(self):
        raise NotImplementedError("to_html method not implemented") 

    def props_to_html(self):
        if self.props is None:
            return ""
        prop_string = ""
        for prop in self.props:
            prop_string += f' {prop}="{self.props[prop]}"'
        return prop_string

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        if (self.tag == other.tag and self.value == other.value
                and self.value == other.value and self.children == other.children):
            return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNodes must have a value")
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNodes must have a tag")
        if self.children is None:
            raise ValueError("ParentNodes must have children")
        ret = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            ret += child.to_html()
        ret += f"</{self.tag}>"
        return ret
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

