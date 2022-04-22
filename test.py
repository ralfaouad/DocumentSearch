import xml.etree.ElementTree as ET
import TED

doc1 = open("Documents/XML1.xml",'r')
doc2 = open("Documents/XML2.xml",'r')

tree1 = ET.parse(doc1).getroot()
tree2 = ET.parse(doc2).getroot()

treeA = TED.preprocessing(tree1)
treeB = TED.preprocessing(tree2)

children = [child for child in treeA]
print(children)