"""Map-class und Point-class"""
from __future__ import annotations
import copy
import numpy as np
from shapely.geometry import Polygon, Point
import assets

class Map():
    """Eine Map ist ein 2x2-grid von Punkten, die einen Wert zwischen 0 und 1 besitzen."""
    def __init__(self, size: tuple[int, int]):
        self.__vals = tuple(tuple(Pixel((x, y)) for x in range(size[0])) for y in range(size[1]))
        self.__size = size
        self.__xlen = size[0]
        self.__ylen = size[1]

    def __repr__(self):
        return self.__class__.__name__ + f"({self.__size})"

    def __getitem__(self, pos: tuple[int, int]) -> Pixel:
        if not 1 < len(pos):
            raise TypeError("A point needs 2 coordinate values")
        else:
            # if both the start and stop value are given [x:y], then we will just return a point
            if abs(pos[0]) < 200 and abs(pos[0]) < 200:
                return self.__vals[pos[1]][pos[0]]
            else:
                return Pixel(pos, val=0)

    def __add__(self, arg: int | float | Map) -> Map:
        out = copy.copy(self)
        if type(arg) in (int, float):
            for row in out.__vals:
                for p in row:
                    p.changeval(p.val + arg)

        elif type(arg) == Map:
            if out.__size == arg.__size:
                for i in range(out.__size[1]):
                    for j in range(out.__size[0]):
                        p = out[j, i]
                        p.changeval(p.val + arg[j, i].val)
            else:
                raise AttributeError("The Maps must be of the same size")
        else:
            raise TypeError(f"argument must be int|float or Map, not {arg.__class__.__name__}")

        return out

    def __sub__(self, arg: int | float | Map) -> Map:
        return self.__add__(arg.__neg__())

    def __mul__(self, arg: int | float | Map) -> Map:
        _out = copy.copy(self)
        if type(arg) in (float, int):
            for row in _out.__vals:
                for p in row:
                    p.changeval(p.val * arg)

        elif type(arg) == Map:
            if _out.__size == arg.__size:
                for i in range(_out.__size[1]):
                    for j in range(_out.__size[0]):
                        p = _out[j, i]
                        p.changeval(p.val * arg[j, i].val)
            else:
                raise AttributeError("The Maps must be of the same size")
        else:
            raise TypeError(f"argument must be int|float or Map, not {arg.__class__.__name__}")

        return _out

    def __truediv__(self, arg: int | float | Map) -> Map:
        if type(arg) in (int, float):
            return self.__mul__(1 / arg)
        elif type(arg) == Map:
            return self.__mul__(arg.__invert__())
        else:
            raise TypeError(f"argument must be int|float or Map, not {arg.__class__.__name__}")

    def __neg__(self) -> Map:
        _out = copy.copy(self)
        for row in _out.__vals:
            for p in row:
                p.changeval(-p.val)

        return _out

    def __invert__(self) -> Map:
        _out = copy.copy(self)
        try:
            for row in _out.__vals:
                for p in row:
                    p.changeval(1 / p.val)
            return _out
        except ZeroDivisionError:
            raise ZeroDivisionError("Map must not contain a zero")

    def getvals(self):
        return self.__vals

    def blob(self, xy: tuple[int, int], radius: int | float = 1, height: int | float = 1):
        """creates a circle with its center being xy and with a radius as specified by the parameter radius"""
        x_rel, y_rel = xy
        for row in self.__vals[max(y_rel - radius, 0):min(y_rel + radius, self.__ylen)]:
            for pixel in row[max(x_rel - radius, 0):min(x_rel + radius, self.__xlen)]:
                # loops through all pixels in the bounding box and fills them if they are inside the circle
                # (if x**2+y**2 = r**2)
                # the bounding box only extends to the border of the map, meaning that the x and y values cannot be
                # bigger than the length of the map, and not smaller than 0.
                # This is ensured by the max() and min() operators
                if (pixel.x - x_rel) ** 2 + (pixel.y - y_rel) ** 2 < radius ** 2:  # x**2 + y**2 = r**2
                    pixel.changeval(height)

    def fill_polygon(self, *args: tuple[int, int], val: int):
        """creates a polygon from the points specified, and then fills every point in that
        polygon with the given value."""
        p = Polygon(shell=args)
        x_vals = tuple(int(i[0]) for i in args)
        y_vals = tuple(int(i[1]) for i in args)
        # iterate only over the pixel in the bounding box
        for x in range(max(min(x_vals), 0), min(max(x_vals), self.__xlen)):
            for y in range(max(min(y_vals), 0), min(max(y_vals), self.__ylen)):
                if p.contains(Point(x, y)):
                    self[x, y].val = val

    def size(self):
        return self.__size


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


