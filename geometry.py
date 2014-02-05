'''
Created on 2 fevr. 2014

@author: gary
'''
import numpy as np
import numpy.linalg as la
import tetgen

def barycentric_coords(vertices, point):
    T = (np.array(vertices[:-1])-vertices[-1]).T
    v = np.dot(la.inv(T), np.array(point)-vertices[-1])
    v.resize(len(vertices))
    v[-1] = 1-v.sum()
    return v

def tetgen_of_hull(points):
    tg_all = tetgen.TetGen(points)
    
    hull_i = set().union(*tg_all.hull)
    hull_points = [points[i] for i in hull_i]
    
    tg_hull = tetgen.TetGen(hull_points)
    return tg_hull, hull_i

def containing_tet(tg, point):
    for i, tet in enumerate(tg.tets):
        verts = [tg.points[j] for j in tet]
        bcoords = barycentric_coords(verts, point)
        if (bcoords >= 0).all():
            return i, bcoords
    return None, None
