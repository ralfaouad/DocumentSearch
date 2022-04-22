from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from sklearn.feature_selection import r_regression
import numpy as np
from scipy.spatial import distance

def cosine(v1, v2):
    return cosine_similarity(v1, v2)

#! Pearson Measure
# def PCC(v1, v2):
#     return pearsonr(v1,v2)

def euclidian(v1,v2):
    return float(1/(1+euclidean_distances(v1,v2)))

def manhattan(v1,v2):
    return float(1/(1+manhattan_distances(v1,v2)))

def tanimoto(v1,v2):
    return float(distance.rogerstanimoto(v1,v2))

    
