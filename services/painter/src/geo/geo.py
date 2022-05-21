import sys

import numpy as np
from scipy.spatial import ConvexHull

from src.util import flatten


def get_min_bounding_box_points(points):
    from src.geo.Rect import Rect

    hull = get_convex_hull(points)

    xmin = sys.maxsize
    xmax = 0
    ymin = sys.maxsize
    ymax = 0

    for point in hull:
        x, y = point

        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y

    return Rect(xmin, ymin, xmax - xmin, ymax - ymin)


def get_min_bounding_box_rects(rects):
    from src.geo.Rect import Rect

    if type(rects) is Rect:
        rects = [rects]

    points = rects_to_points(rects)
    hull = get_convex_hull(points)
    return get_min_bounding_box_points(hull)


def get_convex_hull(points):
    if len(points) == 0:
        return []

    np_points = np.array(points)

    hull = ConvexHull(np_points)

    agg = []

    for vertex in hull.vertices:
        agg.append(points[vertex])

    return agg


# https://tutorialedge.net/gamedev/aabb-collision-detection-tutorial/
def collision(rect_a, rects):
    for rect_b in rects:
        if rect_a.x < rect_b.x + rect_b.width and \
                rect_a.x + rect_a.width > rect_b.x and \
                rect_a.y < rect_b.y + rect_b.height and \
                rect_a.y + rect_a.height > rect_b.y:
            return True

    return False


def rect_to_size(rect):
    return rect.width, rect.height


def rects_to_sizes(rects):
    return list(map(rect_to_size, rects))


def sizes_to_rect(sizes):
    from src.geo.Rect import Rect
    width, height = sizes
    return Rect(0, 0, width, height)


def sizes_to_rects(sizes):
    return list(map(sizes_to_rect, sizes))


def rect_to_points(rect):
   return [
        (rect.x, rect.y),
        (rect.x + rect.width, rect.y),
        (rect.x + rect.width, rect.y + rect.height),
        (rect.x, rect.y + rect.height)
    ]


def rects_to_points(rects):
    return flatten(map(rect_to_points, rects))