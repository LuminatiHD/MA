"""Sammlung der Höhenfunktionen für die Punkte"""
import numpy as np


def K_div_K(self, T, x):
    pass


def K_kon_K(self, T, x):
    # see geogebra file
    b = 3.5

    g = (1 - T) * np.e ** (-abs(x) * b)  # peak mountain
    f = T * np.e ** (-x ** 2)  # flat mountain

    k = 0.7
    h = (k * g - (1 - k) * f) / k

    o = 1.4
    t = np.e ** (4 * T - o) * 2

    return t * (f + h)


def O_div_O(self, T, x):
    pass


def O_kon_O(self, T, x):
    pass


def K_kon_O(self, T, x):
    pass
