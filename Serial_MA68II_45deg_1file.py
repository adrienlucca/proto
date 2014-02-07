'''
Created on 28 janv. 2014

@author: gary
'''

import serial  # requires pyserial library
import csv

f     = open('data/colornames.csv', 'rb')
rgb_names = csv.reader(f, delimiter=',')

ser  = serial.Serial(0)

print "please make sure a previous version of this software isn't still opened to avoid error"
print "if an [ERROR 5] appears under windows, Kill Python.exe and try again"

for row in rgb_names:


# find a way to command measurements by their names
    ofile = file('measurementsMA68II.csv', 'a')
    
    name = row[0]
    print "mesurer la couleur : " + name
    first = True

    while True:
        line = ser.readline()
        if first:
            print "  Data incoming..."
            first = False
        split = line.split()
        if 10 <= len(split):
            try:
                wavelength = int(split[0])
                ofile.write(str(name) + "," + str(wavelength) + "," + split[6] + '\n')
                """"http://stackoverflow.com/questions/21419574/python-export-to-file-via-ofile-without-bracket-characters#21419589"""
                 
            except ValueError:
                pass    # handles the table heading
        if line[:3] == "110":
            break
    
    print "  Data gathered."
    
print "bye bye"