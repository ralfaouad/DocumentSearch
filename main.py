import TED
import xml.etree.ElementTree as ET

TED
doc1 = TED.preprocessing(ET.parse(open("Documents/XML1.xml",'r')).getroot())
doc2 = TED.preprocessing(ET.parse(open("Documents/XML2.xml",'r')).getroot())
print("TED Similarity: ",TED.TED(doc1,doc2))

# ! i) text document pre-processing
# ? In this step, we will be differenciating between input XML file and textual files/simple queries.
# * If input is XML 
#  TODO using XML validator
# * If input is .txt/query
#  TODO

# ! ii) document vector representation
# ? In this step, we will be transforming each document to a vector representation.
# ? But first, we need to tokenize, stem, lemmatize
# * Tokenization
#  TODO using libraries (sltk)
# * Stop word removal, stemming
# TODO 
# * Lemmatization
####
# ? Optional: User can choose which of the following 3 approches to use
# TODO
# * Augmented Vectors
# TODO
# * Term-context
# TODO
# * Matrix model

# ! iii) term weighing and iv) document vector similarity evaluation
# ? In this step, we will be computing the vectors and their dimensions
###
# ? Needed: User can choose which of the following to activate/deactivate.
# * TF
# TODO
# * IDF
# TODO
# * TF-IDF
# TODO
###
# ? Needed: User can choose which measure to use.
# * Cosine
# TODO
# * PCC
# TODO
# * Euclidian, Manhattan, Tanimoto & Dice

# ! v) comparison with project #1's TED measure
# ? In this step, we will compare TED and IR in terms of:
# * Time performance
# TODO
# * Quality performance
# TODO

# ! vi) building index structure
# ? In this step, we will build the inverted indexing technique
# * Add To indexing table
# TODO
# * Run against current indexing table

# ! vii) using querying interface
# ? This step can be merged to step i)
# TODO
