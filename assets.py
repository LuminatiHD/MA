from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point
from typing import Iterable, Literal
import numpy as np
import copy


def getborderpointbyvector(p: np.ndarray[int | float, int | float],
                           v: np.ndarray[int | float, int | float],
                           polygon: Polygon, threshold: float = 0.01) -> np.ndarray[int | float, int | float]:
    """
    Berechnet, wie weit man von einem Punkt P in einem polygon PG in Richtung v schreiten kann, ohne über das
    Polygon PG hinauszutreten. Genauer berechnet es einen Punkt R, der auf der Grenze des Polygon PG und von Punkt P aus
    in Richtung v liegt.
    :param p: der Punkt, wovon aus der Vektor sich bewegt
    :param v: Die Richtung, in welcher der Zielpunkt R liegt
    :param polygon: Das Polygon PG an welcher Grenze der Zielpunkt liegt
    :param threshold: wie nahe die Ausgabe am richtigen PUnkt liegen soll
    :return:
    """
    delta = 1
    s = 0

    # Teil 1: der Vektor wird so lange verlängert bis er ausserhalb des Polygons ist.
    new_s = s + delta
    new_p = p+v*new_s
    while polygon.contains(Point(new_p)):
        new_s = s+delta
        new_p = p+v*new_s

        if not polygon.contains(Point(new_p)):
            break
        else:
            s = new_s
    # Teil 2: der Vektor nähert sich dem Resultat
    while delta>threshold:
        delta/=2
        print(delta)
        new_s = s+delta
        new_p = p+v*new_s
        if polygon.contains(Point(new_p)):
            s = new_s
    return new_p


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


class Map():
    def __init__(self, size:tuple[int, int]):
        self.__vals = tuple(tuple(Pixel((x, y)) for x in range(size[0])) for y in range(size[1]))
        self.__size = size
        self.__xlen = size[0]
        self.__ylen = size[1]

    def __repr__(self):
        return self.__class__.__name__ + f"({self.__size})"

    def __getitem__(self, pos:tuple[int, int]) -> Pixel:
        if not 1<len(pos):
            raise TypeError("A point needs 2 coordinate values")
        else:
            # if both the start and stop value are given [x:y], then we will just return a point
            if abs(pos[0]) < 200 and abs(pos[0]) < 200:
                return self.__vals[pos[1]][pos[0]]
            else:
                return Pixel(pos, val=0)

    def getvals(self):
        return self.__vals

    def blob(self, xy:tuple[int, int], radius:int | float = 1):
        # if all(xy[i] > self.__size[i] for i in range(2)):
        #     raise TypeError("blob coordinates are outside the map space")
        x_rel, y_rel = xy
        for row in self.__vals[max(y_rel-radius, 0):min(y_rel + radius, self.__ylen)]:
            # the max() and min() set a boundary for the loop, in order to avoid over/underflow
            for pixel in row[max(x_rel-radius, 0):min(x_rel + radius, self.__xlen)]:
                if (pixel.x-x_rel)**2 + (pixel.y-y_rel)**2 < radius**2:
                    pixel.changeval(64)

    def fill_polygon(self, *args:tuple[int, int], val:int):
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

