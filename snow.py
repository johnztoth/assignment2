"""
Snow.py
Read in the elevation file (snowslope.txt) provided for the exercise.
Calculate maximum gradient at every point, internal points and boundary points.
Plot elevation and maximum gradient.
Write the maximum gradient to an output file.
"""

import matplotlib.pyplot
import numpy as np

# Read snowslope.txt using numpy.loadtext, the file is read into a numpy.array
z = np.loadtxt("snowslope.txt")    # elevation array

nrows = z.shape[0]                 # size of array, number of rows
ncols = z.shape[1]                 # size of array, number of columns

maxgrad = np.zeros_like(z)         # max gradient at each point
grad = np.zeros(8)                 # temporary gradient array
sqrt2 = np.sqrt(2)                 # distance between diagonal cells

# for internal cells calculate absolute gradient in each direction
# assuming first row is furthest north, as shown in the giff image provided
for i in range(1,nrows-1):
    for j in range(1,ncols-1):
        grad[0] = abs((z[i-1,j]-z[i,j]))             # north
        grad[1] = abs((z[i-1,j+1]-z[i,j])/sqrt2)     # northeast        
        grad[2] = abs((z[i,j+1]-z[i,j]))             # east
        grad[3] = abs((z[i+1,j+1]-z[i,j])/sqrt2)     # southeast        
        grad[4] = abs((z[i+1,j]-z[i,j]))             # south
        grad[5] = abs((z[i+1,j-1]-z[i,j])/sqrt2)     # southwest      
        grad[6] = abs((z[i,j-1]-z[i,j]))             # west
        grad[7] = abs((z[i-1,j-1]-z[i,j])/sqrt2)     # northwest 
        maxgrad[i,j] = np.amax(grad)                 # maximum gradient 

# for north boundary cells
i=0
grad = np.zeros(8)
for j in range(1,ncols-1):        
    grad[2] = abs((z[i,j+1]-z[i,j]))             # east
    grad[3] = abs((z[i+1,j+1]-z[i,j])/sqrt2)     # southeast        
    grad[4] = abs((z[i+1,j]-z[i,j]))             # south
    grad[5] = abs((z[i+1,j-1]-z[i,j])/sqrt2)     # southwest      
    grad[6] = abs((z[i,j-1]-z[i,j]))             # west
    maxgrad[i,j] = np.amax(grad)                 # maximum gradient

# for south boundary cells
i=nrows-1
grad = np.zeros(8)
for j in range(1,ncols-1):
    grad[0] = abs((z[i-1,j]-z[i,j]))             # north
    grad[1] = abs((z[i-1,j+1]-z[i,j])/sqrt2)     # northeast        
    grad[2] = abs((z[i,j+1]-z[i,j]))             # east     
    grad[6] = abs((z[i,j-1]-z[i,j]))             # west
    grad[7] = abs((z[i-1,j-1]-z[i,j])/sqrt2)     # northwest 
    maxgrad[i,j] = np.amax(grad)                 # maximum gradient

# for west boundary cells 
j=0
grad = np.zeros(8)
for i in range(1,nrows-1):
    grad[0] = abs((z[i-1,j]-z[i,j]))             # north
    grad[1] = abs((z[i-1,j+1]-z[i,j])/sqrt2)     # northeast        
    grad[2] = abs((z[i,j+1]-z[i,j]))             # east
    grad[3] = abs((z[i+1,j+1]-z[i,j])/sqrt2)     # southeast        
    grad[4] = abs((z[i+1,j]-z[i,j]))             # south
    maxgrad[i,j] = np.amax(grad)                 # maximum gradient
    
# for east boundary cells
j=ncols-1
grad = np.zeros(8)
for i in range(1,nrows-1):
    grad[0] = abs((z[i-1,j]-z[i,j]))             # north        
    grad[4] = abs((z[i+1,j]-z[i,j]))             # south
    grad[5] = abs((z[i+1,j-1]-z[i,j])/sqrt2)     # southwest      
    grad[6] = abs((z[i,j-1]-z[i,j]))             # west
    grad[7] = abs((z[i-1,j-1]-z[i,j])/sqrt2)     # northwest 
    maxgrad[i,j] = np.amax(grad)                 # maximum gradient

# for north west corner cell
i=0
j=0
grad = np.zeros(8)
grad[2] = abs((z[i,j+1]-z[i,j]))             # east
grad[3] = abs((z[i+1,j+1]-z[i,j])/sqrt2)     # southeast        
grad[4] = abs((z[i+1,j]-z[i,j]))             # south
maxgrad[i,j] = np.amax(grad)                 # maximum gradient 

# for north east corner cell
i=0
j=ncols-1
grad = np.zeros(8)
grad[4] = abs((z[i+1,j]-z[i,j]))             # south
grad[5] = abs((z[i+1,j-1]-z[i,j])/sqrt2)     # southwest      
grad[6] = abs((z[i,j-1]-z[i,j]))             # west
maxgrad[i,j] = np.amax(grad)                 # maximum gradient

# for south east corner cell
i=nrows-1
j=ncols-1
grad = np.zeros(8)
grad[0] = abs((z[i-1,j]-z[i,j]))             # north
grad[6] = abs((z[i,j-1]-z[i,j]))             # west
grad[7] = abs((z[i-1,j-1]-z[i,j])/sqrt2)     # northwest 
maxgrad[i,j] = np.amax(grad)                 # maximum gradient

# for south west corner cell
i=nrows-1
j=0
grad = np.zeros(8)
grad[0] = abs((z[i-1,j]-z[i,j]))             # north
grad[1] = abs((z[i-1,j+1]-z[i,j])/sqrt2)     # northeast        
grad[2] = abs((z[i,j+1]-z[i,j]))             # east       
maxgrad[i,j] = np.amax(grad)                 # maximum gradient


# Plot elevation
matplotlib.pyplot.figure(1)
matplotlib.pyplot.imshow(z)
matplotlib.pyplot.title("ski area elevation")
matplotlib.pyplot.colorbar(label='elevation (m)',shrink=0.75)

# Plot maximum gradient
matplotlib.pyplot.figure(2)
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



