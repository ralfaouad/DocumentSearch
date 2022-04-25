from copy import copy
import xml.etree.ElementTree as ET
import TED

doc1 = open("Documents/XML1.xml",'r')
doc2 = open("Documents/XML2.xml",'r')

tree1 = ET.parse(doc1).getroot()
tree2 = ET.parse(doc2).getroot()

treeA = TED.preprocessing(tree1)
treeB = TED.preprocessing(tree2)


# Path-Based Approach: Root Path 
def root_path(tree, path=[], all=[]):
    # Base Case
    if tree is None:
        return None
    current = tree
    tag = TED.element_name(current.tag)
    path.append(tag)

    # If current node has children, recursively construct the path    
    if current:
        for child in current:
            root_path(child)
        path.pop()
    
    # If we reach a leaf node, store the current path in all and remove the last added node (go up in the tree)
    else:
        copy_path = copy(path)
        all.append(copy_path)
        path.pop()
        return path
    return  list("/".join(path) for path in all)  

# Tag-based Approach
def tag_based(tree):
    # Returning all elements in the tree.
    return [TED.element_name(x.tag) for x in tree.iter()]

    
            
# x = root_path(treeA)
# print(x)

# x = tag_based(treeA)
# print(x)

