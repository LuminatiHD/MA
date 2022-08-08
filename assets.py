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


def getPointOnLinesegment(P: np.ndarray[int | float, int | float],
                          v: np.ndarray[int | float, int | float],
                          R1: np.ndarray[int | float, int | float],
                          R2: np.ndarray[int | float, int | float]) -> np.ndarray[int | float, int | float] | None:
    """Gibt an, ob und wo ein Strahl S von Punkt P aus Richtung v eine Linie R1-R2 überschneidet. Überschneidet es nicht,
    gibt die Funktion None zurück.
    Specifics werden erklärt in https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
    :param P: Ursprungspunkt des Strahls S
    :param v: Richtung des Strahls S
    :param R1, R2: definiert die Linie R1-R2"""

    P1 = P
    P2 = P+v

    u = ((P1[0]-R1[0])*(P1[1]-P2[1])-(P1[0]-P2[0])*(P1[1]-R1[1])) / ((P1[0]-P2[0])*(R1[1]-R2[1]) - (R1[0]-R2[0])*(P1[1]-P2[1]))
    # existiert ein Intersection-point Q zwischen R1-R2 und Strahl P Richtung v, dann ist dieser Punkt Q = R1+u*(R2-R1).
    # falls der Punkt Q zwischen R1 und R2 liegt, dann ist folglich 0<=u<=1.
    # fals demnach u>1 oder u<0, dann liegt Q nicht auf dem Liniensegment R1-R2
    if not 0<=u<=1:
        return None
    else:
        return R1 + u*(R2-R1)


def direction_preference(options:Iterable[np.ndarray[int | float, int | float]],
                         ideal:np.ndarray[int | float, int | float]) -> np.ndarray[int | float, int | float]:
    """Nimmt von Optionen Vektor opt_1 und opt_2 diese, die am ehesten dem Vektor v gleicht/in die gleiche Richtung zeigt.
    :param opt_1, opt_2: oben genannte Optionen, beides Vektoren
    :param ideal: Der ideale Vektor V"""


    options_key = dict()
    for opt in options:
        # Optionsvektoren werden normalisiert -> abs(O_1) = 1
        opt_norm = opt/np.linalg.norm(opt)
        options_key[opt_norm] = opt
    # das Skalarprodukt zweier Vektoren a, b ist cos(Winkel(a, b))*|a|*|b|.
    # Wenn jedoch die Wahl zwischen a1 und a2 besteht und |a1|>|a2| kann das das Resultat verfälschen, da a2 näher an v sein kann, aber immer noch a1*v > a2*v.
    # darum müssen die Vektoren a1 und a2 die gleiche Länge haben, damit es fair ist.

    # je näher 2 Vektoren zueinander sind/je mehr sie in die gleiche Richtung zeigen, desto grösser ist ihr Skalarprodukt.
    # die Funktion vergleicht die Skalarprodukte (engl: dot-product) des Idealvektors und den jeweiligen Optionen und nimmt den Vektor, der das grösste hat -> am nähesten am Idealvektor dran ist.
    dot_products = dict()
    for opt in options_key.keys():
        dot_products[ideal.dot(opt)] = opt

    return options_key[dot_products[max(dot_products)]]
    # das dict dot_products speichert die dot_produkte als key und die korrespondierenden Normalvektoren als value.
    # max(dot_products) gibt den höchsten Wert unter den Key des dicts dot_products zurück.
    # dot_products[max] gibt den korrespondierenden Normalvektor zurück. Wir brauchen jedoch den richtigen Vektor, nicht der normalisierte
    # options_key[norm] gibt den originalen, nicht-normalisierter Vektor zurück.

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

