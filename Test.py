from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import matplotlib.pyplot as plt
from random import randint, seed
from shapely.geometry import Polygon, Point
import random as rand
from world import World

rand.seed(3)

A = World((50, 50))
fig, ax = plt.subplots(1, 1)
points = [(A.size[0]/2, A.size[1]/2)] + [tuple((rand.uniform(0, A.size[0]), rand.uniform(0, A.size[1]))) for i in range(20)]
for i in range(5):
    point = np.array(points[i+1])
    A.split(point)

Map = A.render_world()

plt.imshow(Map)

for plate in A.plates:
    plate_poly = plt.Polygon(plate.vertices, fill=False)
    ax.add_patch(plate_poly)
    x, y = plate.Plate_point
    dx, dy = plate.drift_vector
    # plt.arrow(x, y, dx * 5, dy * 5, width=.8, edgecolor=None, linewidth=None)

data = dict()
for plate in A.plates:
    data[points.index(tuple(plate.Plate_point))] = {"Point": plate.Plate_point,
                                             "PType": plate.PType,
                                             "vector": plate.drift_vector,
                                             "verts": plate.vertices}

print("\n", list(list(i) for i in Map))
plt.show()

