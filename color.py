'''
Created on 4 fevr. 2014

@author: gary
'''

class Color(object):
    def __init__(self, name, x=None, y=None, z=None, r=None, g=None, b=None, spectrum=None):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        self.spectrum = spectrum
        
    def getX(self):
        if self.x is None:
            print "not availlable! "
            self.x = 0
        return self.x
    
    def getY(self):
        if self.y is None:
            print "not availlable!"
            self.y = 0
        return self.y
    
    def getZ(self):
        if self.z is None:
            print "not availlable!"
            self.z = 0
        return self.z
    
    def getR(self):
        if self.r is None:
            print "not availlable! "
            self.r = 0
        return self.r
    
    def getG(self):
        if self.g is None:
            print "not availlable!"
            self.g = 0
        return self.g
    
    def getB(self):
        if self.b is None:
            print "not availlable!"
            self.b = 0
        return self.b
    
    def __str__(self):
        return str(self.name) + str(self.spectrum)
    
    
class Spectrum(object):
    def __init__(self, args):
        self.data = dict()
        for arg in args:
            self.data[arg[0]] = arg[1]
            
    def __str__(self):
        return str(self.data)
    
    def getValue(self, wavelength):
        return self.data[wavelength]
    
    
    
if __name__ == '__main__':
    
    s = Spectrum((400,0.33), (420, 0.22))
    
    print s.getValue(420)