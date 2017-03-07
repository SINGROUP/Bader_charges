import numpy,sys
from copy import deepcopy

# Some command line reading and fixing
args = sys.argv[1:]
if len(args)!=2:
    print 'Supply a XYZ and Bader analysis file'
    sys.exit()
inxyz = args[0]
inbader = args[1]
basename = inxyz.split('_')[0]
newfile = basename+'_charges.'

# Read the XYZ file
f = open(inxyz,'r')
xyz = f.readlines()
f.close()
f = open(inbader,'r')
bader = f.readlines()
f.close()

# Dictionary with valence numbers
valence = {'C':4,'H':1,'N':5,'O':6, 'Co':17}

# Start reading the XYZ file and determine the charge from the Bader file
# Skip the first two lines as they contain other information
atomnames = []
charges = []
positions = []
for i,line in enumerate(xyz):
    line = line.strip()
    if i<2: continue
    xline = line.split()
    bline = bader[i].split()
    atomname = xline[0]
    x = float(xline[1])
    y = float(xline[2])
    z = float(xline[3])
    atomnames.append(atomname)
    positions.append([x,y,z])
    atomvalence = valence[atomname]
    badercharge = float(bline[4])
    partialcharge = atomvalence - badercharge
    charges.append(partialcharge)

positions = numpy.array(positions,'float32')
charges = numpy.array(charges,'float32')

# Start reading the XYZ file and determine the charge from the Bader file
# Skip the first two lines as they contain other information
g = open(newfile+'pdb','w')
h = open(newfile+'xyz','w')
g.write('REMARK Charge checking file\n')
h.write('%d\n\n' % len(charges))
for i in range(len(charges)):
    atomname = atomnames[i]
    x = positions[i,0]
    y = positions[i,1]
    z = positions[i,2]
    partialcharge = charges[i]
    g.write('ATOM      1  %3s     X   1      %6.3f  %6.3f  %6.3f %+5.3f 0.00        %3s\n' % (atomname,x,y,z,partialcharge,atomname))
    h.write('%-5s  %10.5f  %10.5f  %10.5f  %+8.5f\n' % (atomname,x,y,z,partialcharge))
g.write('END\n')
g.close()
h.close()
