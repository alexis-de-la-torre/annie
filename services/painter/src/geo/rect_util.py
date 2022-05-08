from src.geo.Rect import Rect


# https://www.sanfoundry.com/python-program-flatten-nested-list-using-recursion/
def flatten_rects(rects):
    if type(rects) == Rect:
        rects = [rects]

    if not rects:
        return rects

    if len(rects[0].children) > 0:
        return flatten_rects(rects[0].children) + flatten_rects(rects[1:])

    return rects[:1] + flatten_rects(rects[1:])
