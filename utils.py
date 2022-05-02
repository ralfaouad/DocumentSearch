import math
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from sklearn.feature_selection import r_regression
import numpy as np
from scipy.spatial import distance

def cosine(v1, v2):
    num = denom = denom1 = denom2 =  0
    for i in range(len(v1)):
        num+= v1[i]*v2[i]
        denom1+= v1[i]**2
        denom2+= v2[i]**2
    denom = math.sqrt(denom1*denom2)
    # print(num,"/",denom)
    return float(num/denom)

# print(cosine([1,1,1,1,0,0,0,0,0],[1,0,2,2,1,1,0,0,0]))
    
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
    # print(num,"/", denom)
    return num/denom

# print(PCC([1,1,0,0,0,0],[2,2,1,0,0,0]))

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
    # terms = set(dimension.split(",")[0] for dimension in dimensions)
    
    # trm = 0
    # tot = 0
    # for term in terms:
    #     for i in len(dimensions):
    #         if term == dimensions[i].split(",")[0]:
    #             trm += v1[i]*v2[i]*sim_context(dimensions.split(",")[1],dimensions.split(",")[1])
    dict = {}

    for i in range(0, len(dimensions)):
        dimension = dimensions[i]
        if(dimension.split(",")[0] in dict):
            dict[dimension.split(",")[0]][dimension.split(",")[1]] = i
        else: dict[dimension.split(",")[0]] = { dimension.split(",")[1] : i }

    print(dict)
