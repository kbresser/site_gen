from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class BlockNode:
    def __init__(self, block_type, content):
        self.block_type = block_type
        self.content = content

    def __eq__(self, other):
        return (self.block_type == other.block_type and 
                self.content == other.content)
        
    def __repr__(self):
        return f"BlockNode({self.block_type.value}, {self.content})"