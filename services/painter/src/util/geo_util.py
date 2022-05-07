import sys

import numpy as np
from scipy.spatial import ConvexHull

from src.Direction import Direction
from src.util.util import merge, flatten, gen_rand_sizes

import logging

log = logging.getLogger("geo-util")

def rand_coords(qty):
    low = 50
    high = 450

    x = np.random.uniform(low=low, high=high, size=qty)
    y = np.random.uniform(low=low, high=high, size=qty)

    return x, y


def rand_coord():
    x, y = rand_coords(1)
    return x[0], y[0]


def get_min_bounding_box_points(points):
    from src.Rect import Rect

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


def gen_points(qty):
    x, y = rand_coords(qty)
    return merge(x, y)


# https://tutorialedge.net/gamedev/aabb-collision-detection-tutorial/
def collision(rect_a, rects):
    for rect_b in rects:
        if rect_a.x < rect_b.x + rect_b.width and \
                rect_a.x + rect_a.width > rect_b.x and \
                rect_a.y < rect_b.y + rect_b.height and \
                rect_a.y + rect_a.height > rect_b.y:
            return True

    return False


# Generates a qty sized list of randomly positioned rects
def gen_rects(qty, placed_rects=None, tries=0, varied_sizes=False, width=25, height=25, nesting=False):
    from src.Rect import Rect

    if placed_rects is None:
        placed_rects = []

    # Return if enough rects
    if len(placed_rects) == qty:
        return placed_rects

    # cuz we dont like infinity
    if tries >= 100:
        raise Exception("to many retries to generate rects")

    # Generate a bunch of rects

    rects = placed_rects

    origins = gen_points(qty - len(placed_rects))

    for origin in origins:
        x, y = origin

        rand_size = gen_rand_sizes(1)[0]

        if varied_sizes:
            rect = Rect(x, y, rand_size[0], rand_size[1])
        else:
            rect = Rect(x, y, width, height)

        # ignore the ones that collide
        if not collision(rect, rects):
            rects.append(rect)

    # Generate missing rects

    return gen_rects(qty, rects, tries + 1, varied_sizes, width, height)


def rect_to_size(rect):
    return rect.width, rect.height


def rects_to_sizes(rects):
    return list(map(rect_to_size, rects))


def sizes_to_rect(sizes):
    from src.Rect import Rect
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


def center_rects_y(rects, origin_x=None, origin_y=None):
    from src.Rect import Rect

    bb = get_min_bounding_box_rects(rects)

    acc = []

    for i, rect in enumerate(rects):
        y = bb.y + bb.height / 2 - rect.height / 2

        if rect.direction == Direction.HORIZONTAL:
            packed_children = pack_rects_x(rect.children, rect.x, y)
        elif rect.direction == Direction.VERTICAL:
            packed_children = pack_rects_y(rect.children, rect.x, y)

        acc.append(Rect(rect.x, y, rect.width, rect.height, packed_children, rect.direction))

    return acc


def center_rects_x(rects, origin_x, origin_y):
    from src.Rect import Rect

    bb = get_min_bounding_box_rects(rects)

    acc = []

    for i, rect in enumerate(rects):
        x = bb.x + bb.width / 2 - rect.width / 2

        if rect.direction == Direction.HORIZONTAL:
            packed_children = pack_rects_x(rect.children, x, rect.y)
        elif rect.direction == Direction.VERTICAL:
            packed_children = pack_rects_y(rect.children, x, rect.y)

        acc.append(Rect(x, rect.y, rect.width, rect.height, packed_children, rect.direction))

    return acc


def arrange_rects_x(rects, origin_x=None, origin_y=None, align_to_bb= False):
    from src.Rect import Rect # Circular dependency, why?

    if type(rects) == list and len(rects) == 0:
        return []

    if origin_x is None:
        origin_x = rects[0].x

    if origin_y is None:
        origin_y = rects[0].y

    acc = []

    for i, rect in enumerate(rects):
        x = acc[i - 1].x + acc[i - 1].width if i > 0 else origin_x

        if rect.direction == Direction.HORIZONTAL:
            arranged_children = arrange_rects_x(rect.children, x, origin_y)
        elif rect.direction == Direction.VERTICAL:
            arranged_children = arrange_rects_y(rect.children, x, origin_y)

        acc.append(Rect(x, origin_y, rect.width, rect.height, arranged_children, rect.direction))

    return acc


def arrange_rects_y(rects, origin_x=None, origin_y=None):
    from src.Rect import Rect

    if type(rects) == list and len(rects) == 0:
        return []

    if origin_x is None:
        origin_x = rects[0].x

    if origin_y is None:
        origin_y = rects[0].y

    acc = []

    for i, rect in enumerate(rects):
        y = acc[i - 1].y + acc[i - 1].height if i > 0 else origin_y

        if rect.direction == Direction.HORIZONTAL:
            arranged_children = arrange_rects_x(rect.children, origin_x, y)
        elif rect.direction == Direction.VERTICAL:
            arranged_children = arrange_rects_y(rect.children, origin_x, y)

        acc.append(Rect(origin_x, y, rect.width, rect.height, arranged_children, rect.direction))

    return acc


def pack_rects_x(rects, origin_x=None, origin_y=None):
    if len(rects) > 0 and type(rects[0]) == tuple:
        rects = sizes_to_rects(rects)

    if type(rects) == list and len(rects) == 0:
        return []

    arranged = arrange_rects_x(rects, origin_x, origin_y)
    centered = center_rects_y(arranged, origin_x, origin_y)

    return centered


def pack_rects_y(rects, origin_x=None, origin_y=None):
    if len(rects) > 0 and type(rects[0]) == tuple:
        rects = sizes_to_rects(rects)

    if type(rects) == list and len(rects) == 0:
        return []

    arranged = arrange_rects_y(rects, origin_x, origin_y)
    centered = center_rects_x(arranged, origin_x, origin_y)

    return centered


def pack_rects(rects, origin_x=None, origin_y=None, direction=Direction.HORIZONTAL):
    if direction == Direction.HORIZONTAL:
        return pack_rects_x(rects, origin_x, origin_y)
    elif direction == Direction.VERTICAL:
        return pack_rects_y(rects, origin_x, origin_y)