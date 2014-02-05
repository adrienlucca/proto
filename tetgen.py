'''
Created on 2 fevr. 2014

@author: gary
'''
import tempfile, subprocess, os

class TetGen:
    def __init__(self, points):
        self.points = points
        
        node_f = tempfile.NamedTemporaryFile(suffix=".node", delete=False);
        node_f.write("%i 3 0 0\n" % len(points))
        for i, point in enumerate(points):
            node_f.write("%i %f %f %f\n" % (i, point[0], point[1], point[2]))
        node_f.close()
        
        subprocess.call(["tetgen", node_f.name], stdout=open(os.devnull, 'wb'))
        #subprocess.call(["C:\Users\gary\Documents\eclipse\Light Transformer Setup\tetgen", node_f.name], stdout=open(os.devnull, 'wb'))
        ele_f_name = node_f.name[:-5] + ".1.ele"
        face_f_name = node_f.name[:-5] + ".1.face"

        ele_f_lines = [line.split() for line in open(ele_f_name)][1:-1]
        face_f_lines = [line.split() for line in open(face_f_name)][1:-1]

        self.tets = [map(int, line[1:]) for line in ele_f_lines]
        self.hull = [map(int, line[1:]) for line in face_f_lines]

if __name__ == '__main__':
    from pprint import pprint
    points = [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)]
    tg = TetGen(points)
    pprint(tg.tets)
    pprint(tg.hull)
