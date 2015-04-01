
import numpy as N
import math

def vector(tuple):
    ## numpy:
    ##  return N.array(tuple, dtype=float)
    
    return N.array(tuple, N.Float)

def norm(vect):
    ## numpy:
    ## return N.linalg.norm(vect)
    return math.sqrt(N.sum(N.innerproduct(vect, vect)))
    
