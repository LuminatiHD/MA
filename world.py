"""Everything around the World Object"""
from __future__ import annotations

import numpy as np
from typing import Iterable
from shapely.geometry import Polygon, Point
import random as rand
import assets
import heightfunc
from plates import Plate, create_rays
import sys


class World:
    """Der Container für die Platten"""
    def __init__(self, size: tuple[int, int], plates: Iterable[Plate] | None = None):
        self.size = size
        if plates:
            self.plates = list(plates)
        else:
            self.plates = [Plate(point=np.array((size[0]/2, size[1]/2)),
                                 vertices=((0, 0), (0, size[1]), (size[0], size[1]), (size[0], 0)),
                                 PType="K")]

        self.age = 1

    def getPlate(self, point: np.ndarray[int, int]) -> Plate:
        """gibt an, in welcher Platte der angegebene Punkt enthalten ist."""
        selected_plate = None
        # es werden alle plates durchgeloopt bis die Platte gefunden ist, in der der Punkt enthalten ist.
        for plate in self.plates:
            # ".contains" doesn't include points on boundary, but ".touches" returns True for points on the boundary
            if Polygon(plate.vertices).contains(Point(point)) or Polygon(plate.vertices).touches(Point(point)):
                selected_plate = plate
                return selected_plate

        # es kann theoretisch möglich sein, dass der Punkt in keiner Plate enthalten ist
        if not selected_plate:
            raise TypeError("Point is not contained in any Plate")

    def split(self, point: np.ndarray[int | float, int | float] | None = None) -> None:
        """finds the plate that contains :param point, then splits that plate along the perpendicular bisector of the Plate_point and :param point."""
        if point is None:
            point = np.array((rand.uniform(0, self.size[0]), rand.uniform(0, self.size[1])))
            # wurde kein Punkt spezifiziert, generiert das Programm einen zufälligen Punkt

        selected_plate = self.getPlate(point)

        # die alte Platte wird gesplittet. Dies gibt 2 neue Platten zurück.
        new_plates = selected_plate.split(point, self.age)

        # die alte Platte wird durch die neuen Platten ersetzt
        self.plates.remove(selected_plate)
        self.plates.extend(new_plates)

        self.age -= rand.uniform(0, self.age/2)

    def getPointHeight(self, point: np.ndarray[int | float, int | float], resolution: int) -> float:
        """gibt die Höhe eines Punktes zurück.
        :param point: der besagte Punkt
        :param resolution: Mit welcher Genauigkeit die Höhe des Punktes berechnet wird. je höher, desto genauer"""
        homeplate = self.getPlate(point)
        P = point
        values = []
        for ray in create_rays(resolution):
            threshold = 0.001
            Q, E1, E2 = assets.getborderpointbyvector(P, ray, Polygon(homeplate.vertices), threshold)
            if Polygon(homeplate.vertices).exterior.distance(Point(Q)) > threshold:
                print(Q)
            Q += ((ray/np.linalg.norm(ray)) * threshold)
            if not (0 <= Q[0] <= self.size[0] and (0 <= Q[1] <= self.size[1])):
                # falls der Punkt über dem Rand der Platte austritt, "erscheint" er an der anderen Seite wieder.
                neigh_plate = self.getPlate(np.array([Q[0] % self.size[0], Q[1] % self.size[1]]))
            else:
                neigh_plate = self.getPlate(Q)

            distance, weight = heightfunc.get_rayvector_components(P, Q, (E1, E2))
            values.append((heightfunc.get_height_func(abs(distance)*.1, homeplate, neigh_plate, (E1, E2)), np.pi-weight))

        # np.sum() is faster than sum()
        return np.sum((i[0])*i[1] for i in values) / np.sum(i[1] for i in values)

    def render_world(self, res: int = 6) -> np.ndarray:
        """Calculates the height of all points and returns them in a 2D-Array.
        :param res: Accuracy of the height value for each point"""
        A = np.zeros(self.size)
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                h = self.getPointHeight(np.array([x, y]), res)
                A[y, x] = h
                sys.stdout.write("\r" + f"{x}, {y}")
        return A
