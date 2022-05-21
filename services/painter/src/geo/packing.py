from src.Direction import Direction
from src.geo.geo import get_min_bounding_box_rects, sizes_to_rects


def center_rects_y(rects):
    from src.geo.Rect import Rect

    bb = get_min_bounding_box_rects(rects)

    acc = []

    for i, rect in enumerate(rects):
        y = bb.y + bb.height / 2 - rect.height / 2

        if rect.direction == Direction.HORIZONTAL:
            packed_children = pack_rects_x(rect.children, rect.x, y)
        elif rect.direction == Direction.VERTICAL:
            packed_children = pack_rects_y(rect.children, rect.x, y)

        acc.append(Rect(rect.x, y, rect.width, rect.height,
                        packed_children, rect.direction, rect.image, rect.text, rect.text_size))

    return acc


def center_rects_x(rects):
    from src.geo.Rect import Rect

    bb = get_min_bounding_box_rects(rects)

    acc = []

    for i, rect in enumerate(rects):
        x = bb.x + bb.width / 2 - rect.width / 2

        if rect.direction == Direction.HORIZONTAL:
            packed_children = pack_rects_x(rect.children, x, rect.y)
        elif rect.direction == Direction.VERTICAL:
            packed_children = pack_rects_y(rect.children, x, rect.y)

        acc.append(Rect(x, rect.y, rect.width, rect.height,
                        packed_children, rect.direction, rect.image, rect.text, rect.text_size))

    return acc


def arrange_rects_x(rects, origin_x=None, origin_y=None):
    from src.geo.Rect import Rect # Circular dependency, why?

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

        acc.append(Rect(x, origin_y, rect.width, rect.height,
                        arranged_children, rect.direction, rect.image, rect.text, rect.text_size))

    return acc


def arrange_rects_y(rects, origin_x=None, origin_y=None):
    from src.geo.Rect import Rect

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

        # TODO: A way to not keep updating this every time a new property is added
        acc.append(Rect(origin_x, y, rect.width, rect.height,
                        arranged_children, rect.direction, rect.image, rect.text, rect.text_size))

    return acc


def pack_rects_x(rects, origin_x=None, origin_y=None):
    if len(rects) > 0 and type(rects[0]) == tuple:
        rects = sizes_to_rects(rects)

    if type(rects) == list and len(rects) == 0:
        return []

    arranged = arrange_rects_x(rects, origin_x, origin_y)
    centered = center_rects_y(arranged)

    return centered


def pack_rects_y(rects, origin_x=None, origin_y=None):
    if len(rects) > 0 and type(rects[0]) == tuple:
        rects = sizes_to_rects(rects)

    if type(rects) == list and len(rects) == 0:
        return []

    arranged = arrange_rects_y(rects, origin_x, origin_y)
    centered = center_rects_x(arranged)

    return centered


def pack_rects(rects, origin_x=None, origin_y=None, direction=Direction.HORIZONTAL):
    if direction == Direction.HORIZONTAL:
        return pack_rects_x(rects, origin_x, origin_y)
    elif direction == Direction.VERTICAL:
        return pack_rects_y(rects, origin_x, origin_y)