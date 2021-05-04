"""
Skier.py
    Read the elevation file snowslope.txt provided for the exercise.
    Smooth the elevation file.
    Calculate direction of maximum downhill gradient at every point.
    Drop a skier at a random location and move the skier down the mountain.
    Output the smoothed elevation and the skiers path.
"""

import matplotlib.pyplot
import numpy as np
import random

# Read snowslope.txt using numpy.loadtext, the file is read into a numpy.array
z = np.loadtxt("snowslope.txt")

nrows = z.shape[0]
ncols = z.shape[1]

smooth = np.copy(z)                             # elevation data will be smoothed
direction = np.zeros_like(z, dtype = 'int16')   # direction of maximum gradient
grad = np.zeros(8)                              # temporary gradient array

ds = 1.0 # assume distance between data points is 1 unit in both directions
ds_sqrt = ds*np.sqrt(2) # distance between diagonal cells

# smooth the elevation data to make the ski path less jerky
for i in range(1,nrows-1):
    for j in range(1,ncols-1):
        smooth[i,j]=(z[i,j]+z[i-1,j]+z[i-1,j+1]+z[i,j+1]+z[i+1,j+1] \
                     +z[i+1,j]+z[i+1,j-1]+z[i,j-1]+z[i-1,j-1])/9

# calculate direction of maximum downhill gradient, ignore boundary cells
# 0=north, 1=northeast, 2=east, 3=southest
# 4=south, 5=southwest, 6=west, 7=northwest
for i in range(1,nrows-1):
    for j in range(1,ncols-1):
        grad[0] = (smooth[i-1,j]-smooth[i,j])/ds         # north
        grad[1] = (smooth[i-1,j+1]-smooth[i,j])/ds_sqrt  # northeast        
        grad[2] = (smooth[i,j+1]-smooth[i,j])/ds         # east
        grad[3] = (smooth[i+1,j+1]-smooth[i,j])/ds_sqrt  # southeast        
        grad[4] = (smooth[i+1,j]-smooth[i,j])/ds         # south
        grad[5] = (smooth[i+1,j-1]-smooth[i,j])/ds_sqrt  # southwest      
        grad[6] = (smooth[i,j-1]-smooth[i,j])/ds         # west
        grad[7] = (smooth[i-1,j-1]-smooth[i,j])/ds_sqrt  # northwest        
        max = 0.0
        dir = 0
        for k in range(8):
             if grad[k] <= max:    # negative gradient is downhill
                 max = grad[k]     # maximum downward gradient
                 dir = k           # direction of max downward gradient
        direction[i,j] = dir       

# calculate ski run from random starting point
steps = 10000                       # number of movement steps down the mountain
x=np.zeros(steps, dtype = 'int16')  # skiers x location
y=np.zeros(steps, dtype = 'int16')  # skiers y location

# movement matrix, how the skier moves for each gradient direction
mov = np.empty((8,2), dtype = 'int16')
mov[0,0] = -1       # y movement for north step
mov[0,1] = 0        # x movement for north step
mov[2,0] = 0        # y movement for east step
mov[2,1] = 1        # x movement for east step
mov[4,0] = 1        # y movement for south step
mov[4,1] = 0        # x movement for south step
mov[6,0] = 0        # y movement for west step
mov[6,1] = -1       # x movement for west step
mov[1,0] = -1       # y movement for northeast step
mov[1,1] = 1        # x movement for northeast step
mov[3,0] = 1        # y movement for southeast step
mov[3,1] = 1        # x movement for southeast step
mov[5,0] = 1        # y movement for southwest step
mov[5,1] = -1       # x movement for southwest step
mov[7,0] = -1       # y movement for northwest step
mov[7,1] = -1       # x movement for northwest step

y[0] = random.randint(10,nrows-10)    # starting y position of skier
x[0] = random.randint(10,ncols-10)    # starting x position of skier
y[1] = y[0]
x[1] = x[0]

stepstaken = 2        # keep a record of total steps taken
jump =  3             # how far can the skier jump when he gets stuck in a hole
# ski down the slope
for i in range(2,steps):
    stepstaken +=1
    if x[i-1] <= jump:               # dont ski or jump off edge of model
        break
    if x[i-1] >= ncols-jump-1:
        break
    if y[i-1] <= jump:
        break
    if y[i-1] >= nrows-jump-1:
        break
    q = direction[y[i-1],x[i-1]]  # direction of maximum downhill gradient
    y[i] = y[i-1] + mov[q,0]      # move skier
    x[i] = x[i-1] + mov[q,1]
    if x[i-2] == x[i] or y[i-2] == y[i]:   # skier is stuck in hole, jump out
       x[i] = x[i] + random.randint(-jump,jump)
       y[i] = y[i] + random.randint(-jump,jump)
    
print("steps taken =", stepstaken)
xx=x[0:stepstaken-1]
yy=y[0:stepstaken-1]

# Plot smoothed elevation and skiers path down the mountain
matplotlib.pyplot.imshow(smooth)
matplotlib.pyplot.title("ski area elevation")
matplotlib.pyplot.colorbar(label='smoothed elevation (m)',shrink=0.75)
matplotlib.pyplot.scatter(xx,yy,color="red",s = 1)
matplotlib.pyplot.show()




