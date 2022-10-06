"""Sammlung der Höhenfunktionen für die Punkte"""
import numpy as np
import plates
import assets
from shapely.geometry import Polygon, Point


def get_height_func(x, plate1:plates.Plate):
    """findet heraus, welche Höhenfunktion gebraucht werden muss, um die Interaktion zwischen den Platten plate1 und plate2 zu beschreiben."""
    return np.e**(-x**2)*10
    # return x


def get_drift_vector_relations(plate1: plates.Plate, plate2: plates.Plate) -> tuple[np.ndarray[int | float, int | float], np.ndarray[int | float, int | float]]:
    """Relativ-Vektoren von plate1 und plate2"""
    P1 = plate1.Plate_point
    v1 = plate1.drift_vector

    P2 = plate2.Plate_point
    v2 = plate2.Plate_point

    alignment_vector = P1 - P2  # der Vektor, zu welchem u1 parallel sein muss
    len_u1 = v1.dot(alignment_vector) / np.linalg.norm(alignment_vector)
    u1 = len_u1 * assets.normalize_vector(v1)

    alignment_vector = P2 - P1  # der Vektor, zu welchem u2 parallel sein muss
    len_u2 = v2.dot(alignment_vector) / np.linalg.norm(alignment_vector)
    u2 = len_u2 * assets.normalize_vector(v2)

    return u1, u2


def get_T_value(plate1:plates.Plate, plate2:plates.Plate) -> float|int:
    """Returns the T-value of the two given plates"""
    u1, u2 = get_drift_vector_relations(plate1, plate2)


def is_div(plate1:plates.Plate, plate2:plates.Plate) -> bool:
    """bestimmt, ob plate1 und plate2 divergieren oder konvergieren. Falls sie divergieren, gibt die Funktion True zurück."""
    u1, u2 = get_drift_vector_relations(plate1, plate2)


def get_rayvector_components(start_point: np.ndarray[int|float, int|float], ray:np.ndarray[int|float, int|float],
                             border_point: np.ndarray[int|float, int|float], edge: tuple[np.ndarray[int|float, int|float], np.ndarray[int|float, int|float]],
                             homeplate:plates.Plate) -> tuple[int|float, int|float]:
    """get the weight and distance component of a ray vector.
    :param ray: the ray vector
    :param homeplate: """
    E1, E2 = edge
    raw = border_point-start_point
    d = E1-E2

    # rotate by 90°
    u = np.array([-d[1], d[0]])

    if raw.dot(u) < 0:
        u = -u

    #normalize vector

    u = u/np.linalg.norm(u)
    distance = raw.dot(u)
    phi = np.arccos(np.linalg.norm(distance) / np.linalg.norm(raw))
    weight = np.linalg.norm(raw) * np.sin(phi)
    return distance, weight


def true_midpoint(homeplate, neigh_plate) -> np.ndarray[float, float]:
    return np.array(0, 0)


def smoothmin(a, b, k):
    return -np.log2(np.exp2(-k * a) + np.exp2(-k * b)) / k


def smoothmax(a, b, k):
    return np.log2(np.exp2(k * a) + np.exp2(k * b)) / k


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
    np.exp(-x**2)


def O_kon_O(self, T, x):
    pass


def K_kon_O(self, T, x):
    pass


