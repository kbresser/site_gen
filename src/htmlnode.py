class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        if self.children is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        if self.value is None:
            return f"<{self.tag}>{children_html}</{self.tag}>"
        
        return f"<{self.tag}>{self.value}{children_html}</{self.tag}>"
    
    def props_to_html(self):
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()]) if self.props else ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value if self.value is not None else ""
        if self.value is None:
            return f"<{self.tag}></{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        # Initialize with the opening tag
        result = f"<{self.tag}>"
        
        # Add content from all children (if any)
        for child in self.children:
            result += child.to_html()
        
        # Close the tag and return
        result += f"</{self.tag}>"
        return result

    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"