import cv2
import csv

"""test algorithm to create the solution (a bitmap RGB file), 
from an XYZ set of colors and a tiff MAP"""

S = cv2.imread("data/MAP.tif", -1)

height, width = S.shape
min_luminance = S.min()

pix = height * width

p = 1

print "image has:        " + str(pix) + " cells"

print "min luminance is: " + str(min_luminance)

# white is indexed as color num 314

f = open('data/XYZcolorlist.csv')
reader = csv.reader(f, delimiter = ',')

COLORS = dict()

for row in reader:
    COLORS[row[0]] = {'X':row[1], 'Y':row[2], 'Z':row[3]}
    # file structure is: name, R, G, B

for name in COLORS.keys():
    
    Ref_X = COLORS['255 255 255']['X'] # key should be white (314)
    Ref_Y = COLORS['255 255 255']['Y']
    Ref_Z = COLORS['255 255 255']['Z']

print "reference white is XYZ : " + str(Ref_X) + ',' + str(Ref_Y) + ',' + str(Ref_Z)

f = open('data/targets.csv', 'w')

for x in range(width):
    for y in range(height):
        luminance = S[x,y]
      
        at = 0
      
        toDoX = (min_luminance*float(Ref_X))/luminance
        toDoY = (min_luminance*float(Ref_Y))/luminance
        toDoZ = (min_luminance*float(Ref_Z))/luminance
      
        #target = p, toDoX, toDoY, toDoZ, at
        
        f.write(str(p) + "," + str(toDoX) + "," + str(toDoY) + "," + str(toDoZ) + "," + str(at) + "\n")
        p += 1
        P = 100*p/pix
    
        print str(P) + str(' % complete')
    
