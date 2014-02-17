'''
Created on 6 fevr. 2014

@author: gary
'''

import csv
import numpy as np
import scipy.spatial
import cv2
import random

"""loading files"""

points = np.array([(int(R), int(G), int(B), float(X), float(Y), float(Z))
              for R, G, B, X, Y, Z in csv.reader(open('data/colorlist.csv'))])
    # load X,Y,Z coordinates of 'points' in a np.array 
print "colorlist loaded"
    
targets = np.array([(float(X), float(Y), float(Z))
           for name, X, Y, Z in csv.reader(open('data/targets.csv'))])
    # load the XYZ target values in a np.array
print "targets loaded"

img = cv2.imread("data/MAP.tif", -1)
height, width = img.shape
total = height * width
# load dimensions of tif image
print "MAP loaded"

ppm = file("data/walladrien.ppm", 'w')
ppm.write("P3" + "\n" +  str(height) + " " + str(width) +"\n" + "255" + "\n")
# write PPM file header


"""doing geometry"""

tri = scipy.spatial.Delaunay(points[:,[3,4,5]], furthest_site=False) # True makes an almost BW picture
# Delaunay triangulation

indices = tri.simplices
# indices of vertices

vertices = points[indices]
# the vertices for each tetrahedron

# tet = tri.find_simplex(targets[:,[1,2,3]])
# find which tetrahedron each target belongs to

tet = tri.find_simplex(targets)

U = tri.transform[tet,:3]
V = targets - tri.transform[tet,3]   # targets[:,[1,2,3]]
b = np.einsum('ijk,ik->ij', U, V)
bcoords = np.c_[b, 1 - b.sum(axis=1)]
# find the barycentric coordinates of each point

print "shapes:"
print "points     ", points.shape, type(points)
print "indices    ", indices.shape, type(indices)
print "vertices   ", vertices.shape, type(vertices)
print "tetrahedra ", tet.shape, type(tet)
print "bcoords    ", bcoords.shape, type(bcoords)

print 'hull computed', '\n'


# data = np.column_stack((tet, bcoords))
# 
# print "data       ", data.shape, type(data), '\n'
# print "example:", "\n", data[0]
# problem: this converts the indices into doubles!!!


"""looping through data"""

i = 0
 
for i in range(total):
            
    if tet[i] == -1:
        # this means that the point lies outside the convex hull
         
        R = G = B = 255 
         
        ppm.write(str(R) + ' ' + str(G) + ' ' + str(B) + "\n")  # writes a pixel 
        
         
    else: 

        R0 = int(vertices[tet[i]][0][0])
        G0 = int(vertices[tet[i]][0][1])
        B0 = int(vertices[tet[i]][0][2]) 
        R1 = int(vertices[tet[i]][1][0])
        G1 = int(vertices[tet[i]][1][1])
        B1 = int(vertices[tet[i]][1][2])
        R2 = int(vertices[tet[i]][2][0])
        G2 = int(vertices[tet[i]][2][1])
        B2 = int(vertices[tet[i]][2][2])
        R3 = int(vertices[tet[i]][3][0])
        G3 = int(vertices[tet[i]][3][1])
        B3 = int(vertices[tet[i]][3][2])
          
        rand = random.uniform(0,1)
          
        BC_0 = bcoords[i][0]
        BC_1 = bcoords[i][1]
        BC_2 = bcoords[i][2]
        BC_3 = bcoords[i][3]
       
        i += 1 
  
        if rand <= BC_0:
            ppm.write(str(R0) + ' ' + str(G0) + ' ' + str(B0) + "\n")  # writes a pixel        
              
        elif rand <= BC_0 + BC_1:
            ppm.write(str(R1) + ' ' + str(G1) + ' ' + str(B1) + "\n")  # writes a pixel 
                  
        elif rand <= BC_0 + BC_1 + BC_2:
            ppm.write(str(R2) + ' ' + str(G2) + ' ' + str(B2) + "\n")  # writes a pixel 
                  
        else:
            ppm.write(str(R3) + ' ' + str(G3) + ' ' + str(B3) + "\n")  # writes a pixel 
                            
ppm.close()
print 'done'