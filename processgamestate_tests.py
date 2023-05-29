from processgamestate import Point
from processgamestate import Polygon
import unittest


XY_BOUNDS = [[-1735, 250], [-2024, 398], [-2806, 742], [-2472, 1233], [-1565, 580]]


class PolygonTestMethods(unittest.TestCase):
    def test_on_the_line(self):
        polygon = Polygon(XY_BOUNDS)

        self.assertTrue(polygon.in_region(Point(-1735, 250)))
        self.assertTrue(polygon.in_region(Point(-2024, 398)))
        self.assertTrue(polygon.in_region(Point(-2806, 742)))
        self.assertTrue(polygon.in_region(Point(-2472, 1233)))
        self.assertTrue(polygon.in_region(Point(-1565, 580)))

    def test_slightly_right(self):
        polygon = Polygon(XY_BOUNDS)

        self.assertFalse(polygon.in_region(Point(-1735+1, 250)))
        self.assertTrue(polygon.in_region(Point(-2024+1, 398)))
        self.assertTrue(polygon.in_region(Point(-2806+1, 742)))
        self.assertFalse(polygon.in_region(Point(-2472+1, 1233)))
        self.assertFalse(polygon.in_region(Point(-1565+1, 580)))

    def test_slightly_left(self):
        polygon = Polygon(XY_BOUNDS)

        self.assertFalse(polygon.in_region(Point(-1735-1, 250)))
        self.assertFalse(polygon.in_region(Point(-2024-1, 398)))
        self.assertFalse(polygon.in_region(Point(-2806-1, 742)))
        self.assertFalse(polygon.in_region(Point(-2472-1, 1233)))
        self.assertTrue(polygon.in_region(Point(-1565-1, 580)))

    def test_slightly_above(self):
        polygon = Polygon(XY_BOUNDS)

        self.assertTrue(polygon.in_region(Point(-1735, 250+1)))
        self.assertTrue(polygon.in_region(Point(-2024, 398+1)))
        self.assertFalse(polygon.in_region(Point(-2806, 742+1)))
        self.assertFalse(polygon.in_region(Point(-2472, 1233+1)))
        self.assertFalse(polygon.in_region(Point(-1565, 580+1)))

    def test_slightly_below(self):
        polygon = Polygon(XY_BOUNDS)

        self.assertFalse(polygon.in_region(Point(-1735, 250-1)))
        self.assertFalse(polygon.in_region(Point(-2024, 398-1)))
        self.assertFalse(polygon.in_region(Point(-2806, 742-1)))
        self.assertTrue(polygon.in_region(Point(-2472, 1233-1)))
        self.assertFalse(polygon.in_region(Point(-1565, 580-1)))

   
if __name__ == '__main__':
    unittest.main()