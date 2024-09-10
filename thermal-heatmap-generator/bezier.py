import numpy as np
from scipy.special import binom
from typing import Tuple, List

bernstein = lambda n, k, t: binom(n, k) * t**k * (1.0 - t) ** (n - k)


def bezier(points: np.ndarray, num: int = 200) -> np.ndarray:
    """
    Generate a Bezier curve for a set of control points.

    Parameters:
        points (np.ndarray): Control points for the Bezier curve.
        num (int, optional): Number of points to generate along the curve (default is 200).

    Returns:
        np.ndarray: A 2D array representing the curve with shape (num, 2).
    """
    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for i in range(N):
        curve += np.outer(bernstein(N - 1, i, t), points[i])
    return curve


class Segment:
    """
    A class to represent a Bezier curve segment between two points.

    Attributes:
        p1 (np.ndarray): The starting point of the segment.
        p2 (np.ndarray): The ending point of the segment.
        angle1 (float): The angle at the start of the segment.
        angle2 (float): The angle at the end of the segment.
        numpoints (int): Number of points to generate for the curve.
        r (float): Radius factor that determines the control points' distance.
        p (np.ndarray): Control points for the segment.
        curve (np.ndarray): The generated Bezier curve for the segment.
    """

    def __init__(
        self, p1: np.ndarray, p2: np.ndarray, angle1: float, angle2: float, **kw
    ):
        self.p1 = p1
        self.p2 = p2
        self.angle1 = angle1
        self.angle2 = angle2
        self.numpoints = kw.get("numpoints", 100)
        r = kw.get("r", 0.3)
        d = np.sqrt(np.sum((self.p2 - self.p1) ** 2))
        self.r = r * d
        self.p = np.zeros((4, 2))
        self.p[0, :] = self.p1[:]
        self.p[3, :] = self.p2[:]
        self.calc_intermediate_points(self.r)

    def calc_intermediate_points(self, r: float):
        """
        Calculate the intermediate control points for the segment.

        Parameters:
            r (float): Radius factor to calculate the control points.
        """
        self.p[1, :] = self.p1 + np.array(
            [self.r * np.cos(self.angle1), self.r * np.sin(self.angle1)]
        )
        self.p[2, :] = self.p2 + np.array(
            [self.r * np.cos(self.angle2 + np.pi), self.r * np.sin(self.angle2 + np.pi)]
        )
        self.curve = bezier(self.p, self.numpoints)


def get_curve(points: np.ndarray, **kw) -> Tuple[List[Segment], np.ndarray]:
    """
    Generate a Bezier curve that connects multiple points.

    Parameters:
        points (np.ndarray): A 2D array of control points.

    Returns:
        Tuple[List[Segment], np.ndarray]: A list of segments and the full concatenated Bezier curve.
    """
    segments = []
    for i in range(len(points) - 1):
        seg = Segment(
            points[i, :2], points[i + 1, :2], points[i, 2], points[i + 1, 2], **kw
        )
        segments.append(seg)
    curve = np.concatenate([s.curve for s in segments])
    return segments, curve


def ccw_sort(p: np.ndarray) -> np.ndarray:
    """
    Sort points in counter-clockwise order around their centroid.

    Parameters:
        p (np.ndarray): A 2D array of points to sort.

    Returns:
        np.ndarray: The sorted points in counter-clockwise order.
    """
    d = p - np.mean(p, axis=0)
    s = np.arctan2(d[:, 0], d[:, 1])
    return p[np.argsort(s), :]


def get_bezier_curve(
    a: np.ndarray, rad: float = 0.2, edgy: float = 0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate a Bezier curve through a set of points, with adjustable smoothness and control point radius.

    Parameters:
        a (np.ndarray): A 2D array of points through which the curve should pass.
        rad (float, optional): Control point radius factor relative to the distance between adjacent points (default is 0.2).
        edgy (float, optional): A parameter controlling how "edgy" the curve is. 0 is the smoothest (default is 0).

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: The x, y coordinates of the curve and the modified points array.
    """
    p = np.arctan(edgy) / np.pi + 0.5
    a = ccw_sort(a)
    a = np.append(a, np.atleast_2d(a[0, :]), axis=0)
    d = np.diff(a, axis=0)
    ang = np.arctan2(d[:, 1], d[:, 0])
    f = lambda ang: (ang >= 0) * ang + (ang < 0) * (ang + 2 * np.pi)
    ang = f(ang)
    ang1 = ang
    ang2 = np.roll(ang, 1)
    ang = p * ang1 + (1 - p) * ang2 + (np.abs(ang2 - ang1) > np.pi) * np.pi
    ang = np.append(ang, [ang[0]])
    a = np.append(a, np.atleast_2d(ang).T, axis=1)
    s, c = get_curve(a, r=rad)
    x, y = c.T
    return x, y, a


def get_random_points(
    n: int = 5, scale: float = 0.8, mindst: float = None, rec: int = 0
) -> np.ndarray:
    """
    Generate n random points in the unit square, ensuring minimum distance between points.

    Parameters:
        n (int, optional): Number of random points to generate (default is 5).
        scale (float, optional): Scaling factor for the points (default is 0.8).
        mindst (float, optional): Minimum distance between points (default is None).
        rec (int, optional): Recursion counter to prevent infinite loops (default is 0).

    Returns:
        np.ndarray: A 2D array of random points.
    """
    mindst = mindst or 0.7 / n
    a = np.random.rand(n, 2)
    d = np.sqrt(np.sum(np.diff(ccw_sort(a), axis=0) ** 2, axis=1))
    if np.all(d >= mindst) or rec >= 200:
        return a * scale
    else:
        return get_random_points(n=n, scale=scale, mindst=mindst, rec=rec + 1)
