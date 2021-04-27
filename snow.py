"""
Snow.py
Read in the elevation file (snowslope.txt) provided for the exercise.
Calculate maximum gradient at every point. 
Write the maximum gradient to an output file.
"""

import matplotlib.pyplot
import numpy as np

# Read snowslope.txt using numpy.loadtext, the file is read into a numpy.array
elevation = np.loadtxt("snowslope.txt")

nrows = elevation.shape[0]
ncols = elevation.shape[1]

maxgrad = np.zeros_like(elevation) # max gradient at each point
grad = np.zeros(4)                 # temporary gradient array
sqrt2 = np.sqrt(2)                 # distance between diagonal cells

# calculate average gradient in each direction
# assuming first row is furthest north, as shown in the giff image provided
for i in range(1,nrows-1):
    for j in range(1,ncols-1):
        grad[0] = abs((elevation[i-1,j]-elevation[i+1,j])/2)              # n-s
        grad[1] = abs((elevation[i-1,j+1]-elevation[i+1,j-1])/(2*sqrt2))  # ne-sw
        grad[2] = abs((elevation[i,j+1]-elevation[i,j-1])/2 )             # e-w
        grad[3] = abs((elevation[i-1,j-1]-elevation[i+1,j+1])/(2*sqrt2))  # nw-se
        maxgrad[i,j] = np.amax(grad)      # maximum gradient 

# for north boundary
i=0
for j in range(1,ncols-1):
    grad[0] = abs((elevation[i,j]-elevation[i+1,j]))             # north-south
    grad[1] = abs((elevation[i,j]-elevation[i+1,j-1])/(sqrt2))   # ne-sw
    grad[2] = abs((elevation[i,j+1]-elevation[i,j-1])/2)         # east-west
    grad[3] = abs((elevation[i,j]-elevation[i+1,j+1])/(sqrt2))   # nw-se
    maxgrad[i,j] = np.amax(grad)         # maximum gradient

# for south boundary
i=nrows-1
for j in range(1,ncols-1):
    grad[0] = abs((elevation[i-1,j]-elevation[i,j]))             # north-south
    grad[1] = abs((elevation[i-1,j+1]-elevation[i,j])/(sqrt2))   # ne-sw
    grad[2] = abs((elevation[i,j+1]-elevation[i,j-1])/2)         # east-west
    grad[3] = abs((elevation[i-1,j-1]-elevation[i,j])/(sqrt2))   # nw-se
    maxgrad[i,j] = np.amax(grad)         # maximum gradient

# for west boundary
j=0
for i in range(1,nrows-1):
    grad[0] = abs((elevation[i-1,j]-elevation[i+1,j])/2)         # north-south
    grad[1] = abs((elevation[i-1,j+1]-elevation[i,j])/(sqrt2))   # ne-sw
    grad[2] = abs((elevation[i,j+1]-elevation[i,j]))             # east-west
    grad[3] = abs((elevation[i,j]-elevation[i+1,j+1])/(sqrt2))   # nw-se
    maxgrad[i,j] = np.amax(grad)         # maximum gradient
    
# for east boundary
j=ncols-1
for i in range(1,nrows-1):
    grad[0] = abs((elevation[i-1,j]-elevation[i+1,j])/2)         # north-south
    grad[1] = abs((elevation[i,j]-elevation[i+1,j-1])/(sqrt2))   # ne-sw
    grad[2] = abs((elevation[i,j]-elevation[i,j-1]))             # east-west
    grad[3] = abs((elevation[i-1,j-1]-elevation[i,j])/(sqrt2))   # nw-se
    maxgrad[i,j] = np.amax(grad)         # maximum gradient

# for north west corner
i=0
j=0
grad[0] = abs((elevation[i,j]-elevation[i+1,j]))             # north-south
grad[1] = 0                                                  # ne-sw
grad[2] = abs((elevation[i,j+1]-elevation[i,j]))             # east-west
grad[3] = abs((elevation[i,j]-elevation[i+1,j+1])/(sqrt2))   # nw-se
maxgrad[i,j] = np.amax(grad)         # maximum gradient

# for north east corner
i=0
j=ncols-1
grad[0] = abs((elevation[i,j]-elevation[i+1,j]))             # north-south
grad[1] = abs((elevation[i,j]-elevation[i+1,j-1])/(sqrt2))   # ne-sw
grad[2] = abs((elevation[i,j]-elevation[i,j-1]))             # east-west
grad[3] = 0                                                  # nw-se
maxgrad[i,j] = np.amax(grad)         # maximum gradient

# for south east corner
i=nrows-1
j=ncols-1
grad[0] = abs((elevation[i-1,j]-elevation[i,j]))             # north-south
grad[1] = 0                                                  # ne-sw
grad[2] = abs((elevation[i,j]-elevation[i,j-1]))             # east-west
grad[3] = abs((elevation[i-1,j-1]-elevation[i,j])/(sqrt2))   # nw-se
maxgrad[i,j] = np.amax(grad)         # maximum gradient

# for south west corner
i=nrows-1
j=0
grad[0] = abs((elevation[i-1,j]-elevation[i,j]))             # north-south
grad[1] = abs((elevation[i-1,j+1]-elevation[i,j])/(sqrt2))   # ne-sw
grad[2] = abs((elevation[i,j+1]-elevation[i,j]))             # east-west
grad[3] = 0                                                  # nw-se
maxgrad[i,j] = np.amax(grad)         # maximum gradient


# Plot elevation
matplotlib.pyplot.imshow(elevation)
matplotlib.pyplot.title("ski area elevation")
matplotlib.pyplot.colorbar(label='elevation (m)',shrink=0.75)
matplotlib.pyplot.show()

# Plot maximum gradient
matplotlib.pyplot.imshow(maxgrad)
matplotlib.pyplot.title("ski area gradient")
matplotlib.pyplot.colorbar(label='maximum gradient',shrink=0.75)
matplotlib.pyplot.show()

# write gradient to a space separated text file
# maxgrad is output as a float with 4 decimal places
outfile=open("gradient.txt","w")
for i in range(nrows):
    for j in range(ncols):
        print(format(maxgrad[i,j],'2.4f'), end= ' ', file=outfile)
    print(file=outfile) # new row
outfile.close()



