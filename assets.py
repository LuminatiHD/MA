from scipy.spatial import Voronoi


class Map():
    def __init__(self, size:tuple[int, int]):
        self.__vals = tuple(tuple(Pixel((x, y)) for x in range(size[0])) for y in range(size[1]))
        self.__size = size
        self.__xlen = size[0]
        self.__ylen = size[1]

    def __repr__(self):
        return self.__class__.__name__ + f"({self.__size})"

    def __getitem__(self, pos:slice | int):
        if type(pos) == int:
            # if only a start value is given (pos is an int), that means that
            # we will only return the corresponding row
            return self.__vals[pos]
        elif pos.start is None:
            # in the same way, if there is no start value, we just want the column
            return tuple(p[pos.stop] for p in self.__vals)
        else:
            # if both the start and stop value are given [x:y], then we will just return a point
            return self.__vals[pos.stop][pos.start]

    def getvals(self):
        return self.__vals

    def blob(self, xy:tuple[int, int], radius:int | float = 1):
        if xy > self.__size:
            raise TypeError("blob coordinates are outside the map space")
        x_rel, y_rel = xy
        for row in self.__vals[max(y_rel-radius, 0):min(y_rel + radius, self.__ylen)]:
            # the max() and min() set a boundary for the loop, in order to avoid over/underflow
            for pixel in row[max(x_rel-radius, 0):min(x_rel + radius, self.__xlen)]:
                if (pixel.x-x_rel)**2 + (pixel.y-y_rel)**2 < radius**2:
                    pixel.changeval(128)


class Pixel():
    def __init__(self, xy:tuple[int, int], val:float | int=0):
        self.val = val
        self.__pos = xy
        self.x, self.y = xy

    def __repr__(self):
        return "P" + f"({self.__pos}, v={self.val})"

    def changeval(self, newval:float | int):
        """change the value of the pixel to a given parameter"""
        self.val = newval
