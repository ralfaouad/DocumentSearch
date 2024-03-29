import os
import json, TED, path
import xml.etree.ElementTree as ET
import collections

# In this file: Everything related to Indexing Tables

directory = 'Documents'

def process_XML(filename, indexing_table):
    doc = open(directory + "/" + filename,'r')
    tree = TED.preprocessing(ET.parse(doc).getroot())

    terms = path.TC(tree)

    for term in terms:
        if(term in indexing_table):
            if filename not in indexing_table[term]:
                (indexing_table[term]).append(filename)
        else:
            indexing_table[term] = [filename]
    sorted_index = collections.OrderedDict(sorted(indexing_table.items()))
    return sorted_index

def save_toJSON(indexing_table):
    with open('IndexingTable.json', 'w') as f:
        json.dump(indexing_table, f, indent=2)

def process_XML_TB(filename, indexing_table):
    doc = open(directory + "/" + filename,'r')
    tree = TED.preprocessing(ET.parse(doc).getroot())
    terms = path.tag_based(tree)
    for term in terms:
        if(term in indexing_table):
           (indexing_table[term]).append(filename)
        else:
            indexing_table[term] = [filename]
    sorted_index = collections.OrderedDict(sorted(indexing_table.items()))
    return sorted_index

def save_toJSON_TB(indexing_table):
    with open('IndexingTableTags.json', 'w') as f:
        json.dump(indexing_table, f, indent=2)

# Add file to directory -> Update Indexing Table
def add(filename):
    with open('IndexingTable.json', 'r') as f:
        indexing_table = json.loads(f.read())
    new_indexing_table = process_XML(filename, indexing_table)
    save_toJSON(new_indexing_table)

# Delete file from directory -> Update Indexing Table
def delete(filename):
    with open('IndexingTable.json', 'r') as f:
        indexing_table = json.loads(f.read())

    for key in indexing_table:
        if(indexing_table[key][filename]):
            indexing_table[key].pop(filename)

    save_toJSON(indexing_table)

# Compute Indexing Table with the available corpus in file "Documents"
def compute_indexing_table():
    indexing_table1 = {}      
    indexing_table2 = {}
    for filename in os.listdir(directory):
        if filename.endswith((".xml",".XML")):
            tr = process_XML(filename, indexing_table1)
            tb = process_XML_TB(filename, indexing_table2)
    save_toJSON(tr)
    save_toJSON_TB(tb)

compute_indexing_table()