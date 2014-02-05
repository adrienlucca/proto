import geometry
import csv
import numpy as np
import random
import cv2

S = 0


img = cv2.imread("MAP.tif", -1)
height, width = img.shape

accomplished = 0

ppm = file("wall.ppm", 'w')

ppm.write("P3" + "\n" + str(width) + " " + str(height) + "\n" + "255" + "\n")
# PPM file header

all_colors = [(name, float(X), float(Y), float(Z))
              for name, X, Y, Z in csv.reader(open('XYZcolorlist.csv'))]

# background is marked SUPPORT
support_i = [i for i, color in enumerate(all_colors) if color[0] == '255 255 255']
if len(support_i)>0:
    support = np.array(all_colors[support_i[0]][1:])
    del all_colors[support_i[0]]
else:
    support = None

tg, hull_i = geometry.tetgen_of_hull([(X,Y,Z) for name, X, Y, Z in all_colors])
colors = [all_colors[i] for i in hull_i]

print ("thrown out: "
       + ", ".join(set(zip(*all_colors)[0]).difference(zip(*colors)[0])))

targets = [(name, float(X), float(Y), float(Z), float(BG))
           for name, X, Y, Z, BG in csv.reader(open('targets.csv'))]

for target in targets:
    PP = accomplished / (float(height)*float(width))
    
    name, X, Y, Z, BG = target
    
    target_point = support + (np.array([X,Y,Z]) - support)/(1-BG)
    
    tet_i, bcoords = geometry.containing_tet(tg, target_point)
           
    if tet_i == None:
        #print str("out")    
        ppm.write(str("255 255 255") + "\n")
        
        print str(PP)
        
        accomplished += 1
        
        continue 
        # not in gamut
        
    else:

        A = bcoords[0]
        B = bcoords[1]
        C = bcoords[2]
        D = bcoords[3]
          
        R = random.uniform(0,1)
        
        names = [colors[i][0] for i in tg.tets[tet_i]]
                      
        if R <= A:
            S = names[0] 
          
        elif R <= A+B:
            S = names[1]
          
        elif R <= A+B+C:
            S = names[2]
          
        else:
            S = names[3]
              
        ppm.write(str(S) + "\n")
          
        print str(100*PP) + str(" %")
          
        accomplished += 1
  
print "done"
ppm.close()
