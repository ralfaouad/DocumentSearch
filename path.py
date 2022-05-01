from copy import copy
import xml.etree.ElementTree as ET
from matplotlib.style import context
import TED

doc1 = open("Documents/XML1.xml",'r')
doc2 = open("Documents/XML2.xml",'r')

tree1 = ET.parse(doc1).getroot()
tree2 = ET.parse(doc2).getroot()

treeA = TED.preprocessing(tree1)
treeB = TED.preprocessing(tree2)


# Path-Based Approach: Root Path 
# def root_path(tree, path=[], all=[]):
#     # Base Case
#     if tree is None:
#         return None
#     current = tree
#     tag = TED.element_name(current.tag)
#     path.append(tag)

#     # If current node has children, recursively construct the path    
#     if current:
#         for child in current:
#             root_path(child)
#         path.pop()
    
#     # If we reach a leaf node, store the current path in all and remove the last added node (go up in the tree)
#     else:
#         copy_path = copy(path)
#         all.append(copy_path)
#         path.pop()
#         return path
#     return  list("/".join(path) for path in all)  

# Tag-based Approach
def tag_based(tree):
    # Returning all elements in the tree.
    return [TED.element_name(x)[1:] for x in tree.iter()]

def term_context(tree):
    rp = root_path(tree)
    tc = []
    for path in rp:
        p = path.split("/")
        term =  p.pop()
        context = p
        tc.append(str(term + ", " + "/".join(context)))
    return tc

def TC(tree):
    TC_list = []

    for element in tree.iter():
        if TED.element_type(element) == "text":
            TC_list.append(str(TED.element_name(element)[1:] + "," + root_path(element, tree)))

    return TC_list       

def root_path(element, tree):
    toReturn = []
    current = TED.path(element).split(".")

    for counter in range(1, len(current)):
        target = ".".join(current[0:counter])
        toReturn.append(TED.element_name(TED.get_tree(target, tree))[1:])

    return ("/").join(toReturn)

# tc = TC(treeA)
# print(tc)


