from scipy.spatial import Voronoi, voronoi_plot_2d
import assets
import numpy as np
import matplotlib.pyplot as plt
from random import randint

map = assets.Map((200, 200))
map.blob((50, 25), 20)
V = Voronoi([[randint(0, 200), randint(0, 200)] for i in range(100)])


# for reg in V.regions:
#     print([tuple(V.ridge_points[point]) for point in reg])
#
# fig = voronoi_plot_2d(V)


plt.show()
#
# A = np.zeros([200, 200])
# for y in range(0, 200):
#     for x in range(0, 200):
#         value = map[x:y].val
#         color = int((value + 1) * 128)
#         A[x, y] = color

# plt.imshow(A)
# plt.show()