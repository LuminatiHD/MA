from __future__ import annotations
# in order to allow class function argument specifiers to be its parent class

from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point
from typing import Iterable, Literal
import numpy as np
import copy
import random as rand


def getborderpointbyvector(p: np.ndarray[int | float, int | float],
                           v: np.ndarray[int | float, int | float],
                           polygon: Polygon, threshold: float = 0.01) -> tuple[np.ndarray[int | float, int | float], np.ndarray[int | float, int | float], np.ndarray[int | float, int | float]]:
    # wenn der Punkt am Rand des Polygons ist, verschiebt man den etwas zur Mitte des Polygons.
    if polygon.touches(Point(p)):
        dvector = np.array(polygon.centroid)
        p = p+threshold*2*(dvector / np.linalg.norm(dvector))

    for i in range(len(polygon.exterior.coords)):
        E1 = polygon.exterior.coords[i - 1]
        E2 = polygon.exterior.coords[i]
        Q = getPointOnLinesegment(p, v, np.array(E1), np.array(E2))
        if Q is not None:
            if np.array(Q-p).dot(v) >= 0:
                return Q, np.array(E1), np.array(E2)


def approaching_polygon_border(p: np.ndarray[int | float, int | float],
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
    """
    delta = 1
    s = 0
    v=v/np.linalg.norm(v)

    # Teil 1: der Vektor wird so lange verlängert, bis er ausserhalb des Polygons liegt.
    new_s = s + delta
    new_p = p+v*new_s
    while (polygon.contains(Point(new_p)) or polygon.touches(Point(new_p))):
        new_s = s+delta
        new_p = p+v*new_s

        if not polygon.contains(Point(new_p)):
            break
        else:
            s = new_s
    # Teil 2: der Vektor wird dem Resultat angenähert
    while delta>threshold:
        delta/=2

        new_s = s+delta
        new_p = p+v*new_s
        if polygon.contains(Point(new_p)) or polygon.touches(Point(new_p)):
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

    numerator = ((P1[0]-R1[0])*(P1[1]-P2[1])-(P1[0]-P2[0])*(P1[1]-R1[1]))
    divisor = ((P1[0]-P2[0])*(R1[1]-R2[1])-(R1[0]-R2[0])*(P1[1]-P2[1]))
    if divisor == 0:
        return None
    u = numerator / divisor
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
    :param options: oben genannte Optionen, alles Vektoren
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


def organic_border(start_P:np.ndarray, end_P:np.ndarray, polygon:Polygon) -> tuple[tuple[int|float, int|float], ...]:
    """WIP:
    gibt ein Pfad in der form eines tuples von Punkten zurück, der etwas interessanter/organischer aussieht als
    start_P nach end_P
    :param polygon: wird gebraucht, um zu verhindern, dass die Grenze eine der Ecken des Polygons überschneiden könnte."""

    return tuple(start_P), tuple(end_P)


def normalize_vector(v:np.ndarray[int|float, int|float,]) -> np.ndarray[float|float]:
    """normalisiert einen gegebenen Vektor (ausgegebener Vektor zeigt in die gleiche Richtung wie der Ursprüngliche, aber hat eine Länge von 1"""
    len_v = np.linalg.norm(v)
    if len_v == 0:
        return v
    return v/len_v


