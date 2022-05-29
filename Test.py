from scipy.spatial import Voronoi, voronoi_plot_2d
import assets
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from shapely.geometry import Polygon, Point

map = assets.Map((200, 200))
map.blob((50, 25), 20)
V = Voronoi([[randint(0, 200), randint(0, 200)] for i in range(100)], qhull_options="Qc")


for i in range(len(V.points)):
    region_edges = list(V.ridge_points[V.regions[V.point_region[i]]])
    region_points = [(int(i[0]), int(i[1])) for i in region_edges]
    region_points.append((int(V.points[i][0]), int(V.points[i][1])))
    if sum(map[j[0]:j[1]].val for j in region_points if not (j[0] >= 200 or j[1] >= 200))/len(region_points) >= 128/2:
        p = Polygon(region_edges)
        all_x = list(i[0] for i in region_edges)
        all_y = list(i[1] for i in region_edges)
        for x in range(min(all_x), max(all_x)):
            for y in range(min(all_y), max(all_y)):
                if p.contains(other=Point(x, y)):
                    map[x:y].changeval(128)




# for reg in V.regions:
#     print([tuple(V.ridge_points[point]) for point in reg])
#
# fig = voronoi_plot_2d(V)

# print(len(V.point_region), len(set(V.point_region)))

#
A = np.zeros([200, 200])
for y in range(0, 200):
    for x in range(0, 200):
        value = map[x:y].val
        color = int((value + 1) * 128)
        A[x, y] = color
voronoi_plot_2d(V)
plt.imshow(A)
plt.show()