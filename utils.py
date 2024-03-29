import math
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

def clean_text(text):
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    # Removing non alphabetic tokens
    words = [word for word in tokens if word.isalnum()]
    # Stop word removal
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(word) for word in words]
    return (" ").join(lemmatized)

def cosine(v1, v2):
    num = denom = denom1 = denom2 =  0
    for i in range(len(v1)):
        num+= v1[i]*v2[i]
        denom1+= v1[i]**2
        denom2+= v2[i]**2
    denom = math.sqrt(denom1*denom2)
    return float(num/denom)
    
def PCC(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    mean1 = sum1/len(v1)
    mean2 = sum2/len(v2)
    num = denom1 = denom2 = denom = 0
    for i in range(len(v1)):
        num+= (v1[i]-mean1)*(v2[i]-mean2)
        denom1 += (v1[i]-mean1)**2
        denom2 += (v2[i]-mean2)**2
    denom = math.sqrt(denom1*denom2)
    return num/denom

def euclidian(v1,v2):
    dist = 0
    for i in range(len(v1)):
        dist+=(v1[i]-v2[i])**2
    dist = math.sqrt(dist)
    return 1/(1+dist)

def manhattan(v1,v2):
    dist = 0
    for i in range(len(v1)):
        dist+= abs(v1[i]-v2[i])
    return 1/(1+dist)


def jaccard(v1,v2):
    num=v1.intersection(v2)
    denom=v1.union(v2)

    similarity=len(num)/len(denom)

    return similarity

def dice(v1,v2):
    num=2*(v1.intersection(v2))
    denom=(abs(v1)+abs(v2))    
    similarity=num/denom
    return similarity

def e_cosine(dimensions, v1 , v2):
    dict = {}

    for i in range(0, len(dimensions)):
        dimension = dimensions[i]
        term = dimension.split(",")[0]
        context = dimension.split(",")[1]

        if(term in dict):
            dict[term][context] = i
        else: dict[term] = { context : i }

    num = denom = denom1 = denom2 =  0

    for i in range(len(v1)):
        dimension = dimensions[i]
        term = dimension.split(",")[0]
        context = dimension.split(",")[1]
        numc = 0
        for key, val in dict[term].items():
            b = sim_context(context, key)
            print(v1[i], "*", v2[val], "*", b, "+")
            numc += (v1[i] * v2[val] * b)
        num+=numc

    for i in range(len(v1)):
        denom1+= float(v1[i])**2
        denom2+= float(v2[i])**2
    denom = math.sqrt(denom1*denom2)
    return num/denom

def WF(c1, c2):
    c1 = clean_text(c1)
    c2 = clean_text(c2)

    c1 = list(c1)
    c2 = list(c2)
    # WF
    Dist = np.ndarray(shape=(len(c1),len(c2)))
    Dist[0] = 0
    for i in range(1,len(c1)):
        Dist[i][0] = Dist[i-1][0] + costDel(c1[i])
    for j in range(1,len(c2)):
        Dist[0][j] = Dist[0][j-1] + costIns(c2[j])
    
    for i in range(1,len(c1)):
        for j in range(1,len(c2)):
            Dist[i][j] = min(
                Dist[i-1][j-1] + costUpd(c1[i],c2[j]),
                Dist[i-1][j] + costDel(c1[i]),
                Dist[i][j-1] + costIns(c2[j])
            )
    return Dist[i][j]
    
            
def sim_context(c1, c2):
    if c1==c2: return 1
    c1 = c1.split("/")
    c2 = c2.split("/")
    # WF
    Dist = np.ndarray(shape=(len(c1)+1,len(c2)+1))
    Dist[0][0] = 0

    for i in range(1,len(c1)+1):
        Dist[i][0] = Dist[i-1][0] + costDel(c1[i-1])
    for j in range(1,len(c2)+1):
        Dist[0][j] = Dist[0][j-1] + costIns(c2[j-1])
        
    for i in range(1,len(c1)+1):
        for j in range(1,len(c2)+1):
            Dist[i][j] = min(
                Dist[i-1][j-1] + costUpd(c1[i-1],c2[j-1]),
                Dist[i-1][j] + costDel(c1[i-1]),
                Dist[i][j-1] + costIns(c2[j-1])
            )
    return 1/(1+Dist[i][j])

def costUpd(a,b):
    return 0 if a==b else 1

def costIns(a):
    return 1

def costDel(b):
    return 1

def binarySearch(L, target):
    start = 0
    end = len(L) - 1

    while start <= end:
        middle = (start + end)// 2
        midpoint = L[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return middle
