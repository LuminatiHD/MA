"""Test-cases"""
import unittest
from shapely.geometry import Polygon
import numpy as np

import assets
import plates
import heightfunc


class TestAssets(unittest.TestCase):
    def setUp(self) -> None:
        self.Polygon = Polygon([[0, 0], [0, 10], [10, 10], [10, 0]])

    def test_getborderpointbyvector(self):
        self.assertEqual(tuple(assets.getborderpointbyvector(np.array([5, 5]), np.array([1, 0]), self.Polygon)[0]), (10, 5))
        self.assertEqual(tuple(assets.getborderpointbyvector(np.array([5, 5]), np.array([1, 1]), self.Polygon)[0]), (10, 10))
        self.assertFalse(tuple(assets.getborderpointbyvector(np.array([0, 5]), np.array([1, 0]), self.Polygon)[0]) == (0, 5))

    def test_getPointOnLinesegment(self):
        self.assertEqual(tuple(assets.getPointOnLinesegment(np.array([0, 0]), np.array([1, 0]), np.array([2, 1]), np.array([2, -1]))), (2, 0))
        self.assertEqual(tuple(assets.getPointOnLinesegment(np.array([0, 0]), np.array([1, 0]), np.array([2, 1]), np.array([2, 0]))), (2, 0))
        self.assertEqual(assets.getPointOnLinesegment(np.array([0, 0]), np.array([1, 0]), np.array([2, 2]), np.array([2, 1])), None)
        self.assertEqual(assets.getPointOnLinesegment(np.array([0, 0]), np.array([1, 0]), np.array([1, 2]), np.array([2, 2])), None)

    def test_normalize_vector(self):
        self.assertEqual(tuple(assets.normalize_vector(np.array([2, 0]))), (1, 0))
        self.assertEqual(round(np.linalg.norm(assets.normalize_vector(np.array([1, 1])))), 1)
        self.assertEqual(tuple(assets.normalize_vector(np.array([0, 0]))), (0, 0))


class TestPlates(unittest.TestCase):
    def setUp(self) -> None:
        self.plate = plates.Plate(np.array([0, 10]), [(0, 0), (0, 10), (10, 10), (10, 0)], "K", np.array([0, 0]))

    def test_split(self):
        split_plates = self.plate.split(np.array([0, 0]), t=1)
        self.assertEqual(split_plates[0].vertices, ((0, 0), (10, 0), (10.0, 5.0), (0.0, 5.0)))
        self.assertEqual(split_plates[1].vertices, ((10, 10), (0, 10), (0.0, 5.0), (10.0, 5.0)))
        self.assertEqual(round(np.linalg.norm(split_plates[0].drift_vector)), 1)
        self.assertEqual(tuple(split_plates[0].drift_vector + split_plates[1].drift_vector), (0, 0))
        self.assertFalse(tuple(split_plates[0].Plate_point) == tuple(split_plates[1].Plate_point))
        self.assertEqual(split_plates[0].PType, self.plate.PType)
        self.assertEqual(split_plates[0].PType, split_plates[1].PType)


class Test_Heightfunc(unittest.TestCase):
    def setUp(self):
        self.plate1, self.plate2 = plates.Plate(np.array([5, 6]), [(0, 0), (0, 10), (10, 10), (10, 0)], "K", np.array([0, 0])).split(np.array([5, 4]), t=1)

    def test_relativ_vectors(self):
        u1, u2 = heightfunc.get_drift_vector_relations(self.plate1, self.plate2, (np.array([0, 5]), np.array([10, 5])))
        self.assertTrue(u1.dot(u2)<0)
        self.assertGreater(np.linalg.norm(u1), 0)
        self.assertGreater(np.linalg.norm(u2), 0)

    def test_is_div(self):
        u1, u2 = heightfunc.get_drift_vector_relations(self.plate1, self.plate2, (np.array([0, 5]), np.array([10, 5])))
        self.assertTrue(heightfunc.is_div(self.plate1, self.plate2, u1, u2))
        self.assertFalse(heightfunc.is_div(self.plate1, self.plate2, u2, u1))
