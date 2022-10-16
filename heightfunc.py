"""Sammlung der Höhenfunktionen für die Punkte"""
import numpy as np
import plates


def get_height_func(x, plate1: plates.Plate, plate2: plates.Plate,
                    shared_border: tuple[np.ndarray[int | float, int | float], np.ndarray[int | float, int | float]]) -> float:
    """Teilt den Interaktionen zwischen zwei Platten eine Relieffunktion zu und setzt dann den Wert x dafür ein.
    :param x: Der Wert, der in die Formel eingesetzt wird.
    :param plate1: Eine der oben erwähnten Platten. Es wird angenommen, dass der Wert, von welchem der x-Wert stammt, in dieser Platte enthalten ist.
    :param plate2: Die zweite der oben erwähnten Platten.
    :param shared_border: Definiert die Grenze, welche plate1 von plate2 separiert."""

    u1, u2 = get_drift_vector_relations(plate1, plate2, shared_border)
    T = get_T_value(u1, u2) * .05
    if is_div(plate1, plate2, u1, u2):
        if plate1.PType == "K":
            return K_div_K(T, x)
        else:
            return O_div_O(T, x)

    else:
        if plate1.PType != plate2.PType:
            if plate1.PType == "K":
                return K_kon_O(T, -x)+1
            else:
                return K_kon_O(T, x)

        else:
            if plate1.PType == "K":
                return K_kon_K(T, x)
            else:
                return O_kon_O(T, x)


def get_drift_vector_relations(plate1: plates.Plate, plate2: plates.Plate,
                               shared_border: tuple[np.ndarray[int | float, int | float],
                                                    np.ndarray[int | float, int | float]]) -> tuple[np.ndarray[int | float, int | float], np.ndarray[int | float, int | float]]:
    """Berechnet, wie die Driftvektoren der Platten :param plate1 und :param plate2 relativ zueinander stehen.
    :param shared_border: definiert die Grenze, die plate1 und plate2 teilen."""

    s = shared_border[0] - shared_border[1]
    v1 = plate1.drift_vector
    v2 = plate2.drift_vector

    u1 = s * (v1.dot(s))/np.linalg.norm(s)
    u2 = s * (v2.dot(s)) / np.linalg.norm(s)

    return u1, u2


def get_T_value(rel_vec_1: np.ndarray[int | float, int | float], rel_vec_2: np.ndarray[int | float, int | float]) -> float | int:
    """Gibt den T-wert zurück zweier Platten
    :param rel_vec_1: Relativ-Vektor von Platte 1 auf Platte 2 bezogen
    :param rel_vec_2: Relativ-Vektor von Platte 2 auf Platte 1 bezogen"""
    return np.linalg.norm(rel_vec_1) + np.linalg.norm(rel_vec_2)


def is_div(plate1: plates.Plate, plate2: plates.Plate, rel_vec_1: np.ndarray[int | float, int | float], rel_vec_2: np.ndarray[int | float, int | float]) -> bool:
    """bestimmt, ob plate1 und plate2 divergieren oder konvergieren. Falls sie divergieren, gibt die Funktion True zurück."""
    if np.linalg.norm(rel_vec_1) > np.linalg.norm(rel_vec_2):
        u = rel_vec_1
        if u.dot(np.array(plate2.Plate_point - plate1.Plate_point)) > 0:
            return True
        else:
            return False
    else:
        u = rel_vec_2
        if u.dot(plate1.Plate_point - plate2.Plate_point) > 0:
            return True
        else:
            return False


def get_rayvector_components(start_point: np.ndarray[int | float, int | float],
                             border_point: np.ndarray[int | float, int | float], edge: tuple[np.ndarray[int | float, int | float], np.ndarray[int | float, int | float]]) -> tuple[int | float, int | float]:
    """get the weight and distance component of a ray vector.
    :param start_point: The Starting point of the ray
    :param border_point: The point where the ray crosses the plate boundary
    :param edge: the edge line where the ray crosses the plate boundary"""

    E1, E2 = edge
    raw = border_point-start_point
    d = E1-E2

    # rotate by 90°
    u = np.array([-d[1], d[0]])

    if raw.dot(u) < 0:
        u = -u

    # normalize vector

    u = u/np.linalg.norm(u)
    distance = raw.dot(u)
    phi = np.arccos(np.linalg.norm(distance) / np.linalg.norm(raw))
    weight = phi
    return distance, weight


def K_div_K(T: int | float, x: int | float) -> float:
    """Relieffunktion kontinental-kontinental divergent"""
    return 1 / (1 + np.exp(4 * (-x + 4 * T)/T)) + np.exp(-25*x**2)/10


def K_kon_K(T: int | float, x: int | float) -> float:
    """Relieffunktion kontinental-kontinental konvergent"""
    return np.exp(-2*x**2)*np.log(T+1)+1


def O_div_O(T: int | float, x: int | float) -> float:
    """Relieffunktion ozeanisch-ozeanisch divergent"""
    return np.exp(-x**2)/10


def O_kon_O(T: int | float, x: int | float) -> float:
    """Relieffunktion ozeanisch-ozeanisch konvergent"""
    return K_kon_K(T, x) - 1


def K_kon_O(T: int | float, x: int | float) -> float:
    """Relieffunktion kontinental-ozeanisch konvergent"""
    s1 = 1.4
    s2 = 2.5
    return T * (np.exp(s1*(x+1)**2) - np.exp(-s2*abs(x)))
