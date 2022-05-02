import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import regex as re
import time


# STEP 1: Document Preprocessing
def preprocessing(elt,depth=0,path=""):
    if elt is None:
        return None
    newtree = Element(path + str(depth) + ".&" + str(elt.tag))

    new_path = path + str(depth) + "." 
    d = 0

    for key,value in sorted(elt.attrib.items()):
        attr_path = new_path + str(d) + "."
        attr_key = SubElement(newtree, attr_path + "@" + str(key))
        attr_value = SubElement(attr_key, attr_path + "0." + "#" + str(value))
        d += 1
    
    for child in elt:
        newtree.append(preprocessing(child, d, new_path))
        d += 1

    if elt.text is not None:
        tokens = elt.text.split()
        for token in tokens:
            tk = SubElement(newtree, new_path + str(d) + ".#" + str(token))
            d+=1
    return newtree   

# STEP 2: Document Differencing
costs_del = {}
costs_ins = {}
edit_scripts = {}

def degree(root):
    deg = 0
    for child in root:
        deg+=1
    return deg
    
def cost_ins(n):
    return 1

def cost_del(n):
    return 1

def cost_upd(n1,n2):
    return 0 if (re.split('@|#|&',n1.tag)[1]) == (re.split('@|#|&',n2.tag)[1]) else 1

def cost_ins_tree(treeA, treeB):
    # print("cost_ins_tree(",treeA,",",treeB,": ",1 if contained_in(treeA,treeB) else len(list(treeA.iter())))
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))

def cost_del_tree(treeA, treeB):
    # print("cost_del_tree(",treeA,",",treeB,": ",1 if contained_in(treeA,treeB) else len(list(treeA.iter())))
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))
        
def get_size(root):
    # includes root
    count = 0
    for element in root.iter():
        count +=1
    return count

def contained_in(treeA, treeB):
    rootA = re.split('@|#|&',treeA.tag)[1]
    rootB = re.split('@|#|&',treeB.tag)[1]
    
    if(rootA == rootB):
        if get_size(treeA) == 1 and get_size(treeB) == 1:
            return True

        if get_size(treeA) > 1:
            a = True

            children_A = []
            for child_A in treeA:
                children_A.append(child_A)

            children_B = []
            for child_B in treeB:
                children_B.append(child_B)

            for child_A in treeA:
                if(not children_B):
                    a = False
                    break
                while(children_B):
                    if re.split('@|#|&',child_A.tag)[1] == re.split('@|#|&',children_B[0].tag)[1] :
                        a = a and contained_in(child_A,children_B[0])
                        children_A.pop(0)
                        children_B.pop(0)
                        break
                    children_B.pop(0)
            
            if(children_A): a = False
            return a
    
    a = False
    for child_B in treeB:
        a = a or contained_in(treeA, child_B)
    return a

def get_tree(path,tree):
    path_list = path.split(".")
    if(len(path_list) == 1):#2):
        return tree
    target = int(path_list[1])

    children =[]
    for child in tree:
        children.append(child)
    # print("children list: \t"+str(children))
    if(len(children) == 0):
        return tree
    else: return get_tree(".".join(path_list[1:]) , children[target])

def path(element):
    return re.split('.@|.#|.&',element.tag)[0]

def element_name(element):
    l = (element.tag).split(".")
    return l[-1]  

def element_type(element):
    if('@' in element.tag):
        return "attribute"
    elif('&' in element.tag):
        return "element"
    else: return "text"

def calculcate_costs(treeA,treeB):
    for subA in treeA.iter():
        path = re.split('@|#|&',subA.tag)[0]
        cdel = cost_del_tree(subA,treeB)
        costs_del[path] = cdel
    print(costs_del)

    for subB in treeB.iter():
        path = re.split('@|#|&',subB.tag)[0]
        cins = cost_ins_tree(subB,treeA)
        costs_ins[path] = cins
    print(costs_ins)



def TED_Nierman(A,B):
    M = degree(A)
    N = degree(B)
    
    listA = []
    for subA in A:
        listA.append(subA) 

    listB = []
    for subB in B:
        listB.append(subB)

    Dist = [[0 for i in range(N+2)] for j in range(M+2)]

    # Headers:
    Dist[0][0] = "A  B"
    Dist[1][0] = A.tag
    Dist[0][1] = B.tag
    for i in range(2,len(Dist)):
        Dist[i][0] = listA[i-2].tag
    
    for j in range(2,len(Dist[0])):
        Dist[0][j] = listB[j-2].tag

    # Actual TED Matrix:
    Dist[1][1] = cost_upd(A,B)

    for i in range(2,len(Dist)):
        Dist[i][1] = int(Dist[i-1][1]) + costs_del[re.split('@|#|&',listA[i-2].tag)[0]]
    
    for j in range(2,len(Dist[0])):
        Dist[1][j] = int(Dist[1][j-1]) + costs_ins[re.split('@|#|&',listB[j-2].tag)[0]]

    for i in range(2,len(Dist)):
        for j in range(2,len(Dist[0])):
            if(element_name(A)[0] == element_name(B)[0]):
                update = int(Dist[i-1][j-1])+TED_Nierman(listA[i-2],B[j-2])
                delete = int(Dist[i-1][j])+int(costs_del[re.split('@|#|&',listA[i-2].tag)[0]])
                insert = int(Dist[i][j-1])+int(costs_ins[re.split('@|#|&',listB[j-2].tag)[0]])
                Dist[i][j] = min(insert,delete,update)
            else:
                delete = int(Dist[i-1][j])+int(costs_del[re.split('@|#|&',listA[i-2].tag)[0]])
                insert = int(Dist[i][j-1])+int(costs_ins[re.split('@|#|&',listB[j-2].tag)[0]])
                Dist[i][j] = min(insert,delete)
    # for i  in range(len(Dist)):
    #     for j in range(len(Dist[i])):
    #         print( Dist[i][j],end="\t"*2)
    #     print()

    return(int(Dist[M+1][N+1]))

def TED(A,B):
    start = time.time()
    calculcate_costs(A,B)
    distance = TED_Nierman(A,B)
    print("dist: ",distance)
    end = time.time()
    similarity = str(float(1/(1+distance)))
    delay = end-start
    print("t",delay)
    return similarity

doc1 = open("UploadedDocuments/SampleDoc1_original_v1.xml", 'r')
doc2 = open("UploadedDocuments/SampleDoc1_original.xml", 'r')

tree1 = preprocessing(ET.parse(doc1).getroot())
tree2 = preprocessing(ET.parse(doc2).getroot())

# for x in tree1.iter():
#     print(x)

# for x in tree2.iter():
#     print(x)
# print("CD: ",costs_del)
# print("CI: ",costs_ins)
print(TED(tree1,tree2))








    










