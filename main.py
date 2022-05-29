import assets
from scipy.spatial import Voronoi
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import opensimplex
from opensimplex import OpenSimplex

map = assets.Map((200, 200))
map.blob((50, 25), 20)


A = np.zeros([200, 200])
for y in range(0, 200):
    for x in range(0, 200):
        value = map[x:y].val
        color = int((value + 1) * 128)
        A[x, y] = color

plt.imshow(A)
plt.show()