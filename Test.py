# from scipy.spatial import Voronoi, voronoi_plot_2d
# import assets
# import numpy as np
# import matplotlib.pyplot as plt
# from random import randint
# from shapely.geometry import Polygon, Point
#
# map = assets.Map((200, 200))
# V = Voronoi([[randint(0, 200), randint(0, 200)] for i in range(50)], qhull_options="Qc")
# """the voronoi thing is broken as fuck jesus motherfucking christ good luck"""
# for i in range(len(V.points)):
#     region = tuple(tuple(V.vertices[j]) for j in V.regions[tuple(V.point_region)[i]])
#     point = V.points[i]
#     if not Polygon(region).contains(Point(point)):
#         print("="*40+f"\n{i}")
#         print(region, point)
#         # map.fill_polygon(*region, val=i)
#
# for i in V.vertices:
#     map.blob(tuple(int(j) for j in i), 2)
#
# # for reg in V.regions:
# #     print([tuple(V.ridge_points[point]) for point in reg])
# #
# # fig = voronoi_plot_2d(V)
#
# # print(len(V.point_region), len(set(V.point_region)))
#
# #
# A = np.zeros([200, 200])
# for y in range(0, 200):
#     for x in range(0, 200):
#         value = map[x:y].val
#         color = int((value + 1))
#         A[x, y] = color
#
# voronoi_plot_2d(V)
# plt.imshow(A)
# plt.show()

import numpy as np
points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],

                   [2, 0], [2, 1], [2, 2]])

from scipy.spatial import Voronoi, voronoi_plot_2d

V = Voronoi(points)
import matplotlib.pyplot as plt

fig = voronoi_plot_2d(V)

print(V.point_region, tuple(tuple(tuple(V.vertices[i]) for i in j) for j in V.regions))

plt.show()