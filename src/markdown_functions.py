import re 
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    #below will be a few different if statements checking for different block types
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")): #Headings check
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"): #code check
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") for line in lines): #quote check
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines): #unordered list check
        return BlockType.UNORDERED_LIST

    
    if all(line.startswith(f"{count+1}. ") for count, line in enumerate(lines)): #ordered list check 8) enumerate is op
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return(matches)

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return(matches)

def markdown_to_blocks(markdown):
    raw_block = markdown.split("\n\n")
    new_blocks = []
    for block in raw_block:
        stripped = block.strip()
        if stripped:
            lines = stripped.split('\n')
            fixed_lines = [line.strip() for line in lines]
            fixed_block = '\n'.join(fixed_lines)
            new_blocks.append(fixed_block)
    return new_blocks
