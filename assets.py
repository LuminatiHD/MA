"""Enthält alle Funktionen, die für nichts spezifisches gebraucht werden."""
from __future__ import annotations
# in order to allow class function argument specifiers to be its parent class
from shapely.geometry import Polygon, Point
from typing import Iterable
import numpy as np


def getborderpointbyvector(p: np.ndarray[int | float, int | float],
                           v: np.ndarray[int | float, int | float],
                           polygon: Polygon, threshold: float = 0.01) -> tuple[np.ndarray[int | float, int | float],
                                                                               np.ndarray[int | float, int | float],
                                                                               np.ndarray[int | float, int | float]]:
    """Findet den Punkt, wo der Strahl :param p + λ * :param v die Grenze des Polygons :param polygon schneidet.
    :returns: die Funktion gibt drei Punkte zurück. Diese sind der Punkt, wo der Strahl das Polygon schneidet, sowie die zwei Eckpunkte des Polygons zwischen welchen
              dieser Punkt liegt, in dieser Ordnung.
    :param p: definiert den Startpunkt des Strahls.
    :param v: definiert die Richtung des Strahls.
    :param polygon: das wie oben definierte polygon.
    :param threshold: Definiert, wie nahe der zurückgegebene Punkt am richtigen Wert liegen soll.
    (Falls der Startpunkt auf der Grenze des Polygons liegt, verschiebt die Funktion diesen Punkt um diesen Wert zum Polygon hinzu, da es sonst zu Probleme führen könnte). """

    # wenn der Punkt am Rand des Polygons ist, verschiebt man den etwas zur Mitte des Polygons.
    if polygon.touches(Point(p)):
        dvector = np.array(polygon.centroid)
        p = p+threshold*2*(dvector / np.linalg.norm(dvector))

    # Geht durch alle Eckpunktpaare, bis dieses gefunden wurde, zwischen welchen der Grenzpunkt liegt.
    for i in range(len(polygon.exterior.coords)):
        E1 = np.array(polygon.exterior.coords[i - 1])
        E2 = np.array(polygon.exterior.coords[i])

        # falls der Punkt nicht zwischen diesen Punkten liegt, gibt diese Funktion None zurück.
        Q = getPointOnLinesegment(p, v, np.array(E1), np.array(E2))
        if Q is not None:
            if np.array(Q-p).dot(v) >= 0:
                return Q, np.array(E1), np.array(E2)


def getPointOnLinesegment(P: np.ndarray[int | float, int | float],
                          v: np.ndarray[int | float, int | float],
                          R1: np.ndarray[int | float, int | float],
                          R2: np.ndarray[int | float, int | float]) -> np.ndarray[int | float, int | float] | None:
    """Gibt an, ob und wo ein Strahl S von Punkt P aus Richtung v eine Linie R1-R2 überschneidet. Überschneidet der Strahl diese Linie nicht,
    gibt die Funktion None zurück.
    Specifics werden erklärt in https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
    :param P: Ursprungspunkt des Strahls S
    :param v: Richtung des Strahls S
    :param R1:/:param R2: definieren die Linie R1-R2"""

    P1 = P
    P2 = P+v

    numerator = ((P1[0]-R1[0])*(P1[1]-P2[1])-(P1[0]-P2[0])*(P1[1]-R1[1]))
    divisor = ((P1[0]-P2[0])*(R1[1]-R2[1])-(R1[0]-R2[0])*(P1[1]-P2[1]))
    # wenn der Strahl und die Linie parallel sind, ist der divisor = 0.
    if divisor == 0:
        return None
    u = numerator / divisor
    # existiert ein Intersection-point Q zwischen R1-R2 und Strahl P Richtung v, dann ist dieser Punkt Q = R1+u*(R2-R1).
    # falls der Punkt Q zwischen R1 und R2 liegt, dann ist folglich 0<=u<=1.
    # falls demnach u>1 oder u<0, dann liegt Q nicht auf dem Liniensegment R1-R2
    if not 0 <= u <= 1:
        return None
    else:
        return R1 + u*(R2-R1)


def normalize_vector(v: np.ndarray[int | float, int | float]) -> np.ndarray[float | float]:
    """normalisiert einen gegebenen Vektor (ausgegebener Vektor zeigt in die gleiche Richtung wie der Ursprüngliche, aber hat eine Länge von 1"""
    len_v = np.linalg.norm(v)
    if len_v == 0:
        # falls der Vektor die Länge 0 hat, dann handelt es sich um den 0-vektor -> (0, 0)
        return v
    return v/len_v
