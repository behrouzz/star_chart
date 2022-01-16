from io import StringIO
import pandas as pd
from constellations import constellations
from hipparcos import hip_stars

def load_constellations():
    data = constellations.split('\n')[1:-1]
    dc = {}
    for i in data:
        name = i.split(' ')[0]
        stars = i.split(' ')[2:]
        stars = [int(j) for j in stars]
        edges = [tuple(stars[k:k+2]) for k in [*range(0,len(stars),2)]]
        dc[name] = edges
    return dc

def create_edges(dc):
    """
    Create edges (lines) connecting each pair of stars
    
    Arguments
    ---------
        dc : dictionary of constellations
    Returns
    -------
        edges : list of all edges
    """
    edges = []
    for k,v in dc.items():
        for i in v:
            edges.append(i)
    return edges

def load_hipparcos():
    return pd.read_csv(StringIO(hip_stars)).set_index('hip')



dc = load_constellations()

const2star = {}
for k,v in dc.items():
    ls = []
    for i in range(len(v)):
        ls = ls + list(v[i])
    const2star[k] = list(set(ls))
    
star2const = {}
for k,v in const2star.items():
    for i in v:
        star2const[i] = k
