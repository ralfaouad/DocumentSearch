from copy import copy
import xml.etree.ElementTree as ET
from matplotlib.style import context
import TED

# Tag-based Approach
def tag_based(tree):
    # Returning all elements in the tree.
    return [TED.element_name(x)[1:] for x in tree.iter()]

# Term-context Approach
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


