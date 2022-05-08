from src.Direction import Direction
from src.geo.geo import get_min_bounding_box_rects
from src.geo.packing import pack_rects


class Rect:
    def __init__(self, x=0, y=0, w=0, h=0, children=None, direction=Direction.HORIZONTAL, image=None):

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.children = [] if children is None else children
        self.direction = direction
        self.image = image

    def append(self, rects, direction=Direction.HORIZONTAL):
        if type(rects) == list and len(rects) == 0:
            return
        if type(rects) == Rect:
            rects = rects.children

        packed = pack_rects(rects, direction=direction)
        bbw = get_min_bounding_box_rects(packed)
        rect = Rect(bbw.x, bbw.y, bbw.width, bbw.height, packed, direction)

        aa = self.children + [rect]

        bb = pack_rects(aa, direction=self.direction)

        self.children = bb

        self.recalculate_bb()

    def recalculate_bb(self):
        bb = get_min_bounding_box_rects(self.children)

        self.x = bb.x
        self.y = bb.y
        self.width = bb.width
        self.height = bb.height

    # def __str__(self):
    #     return '▩(x={:.2f} y={:.2f} w={:.2f} h={:.2f}, c({})={})'\
    #         .format(self.x, self.y, self.width, self.height, len(self.children), self.children)

    def __str__(self):
        return 'Rect({0}, {1}, {2}, {3}, {4})' \
            .format(self.x, self.y, self.width, self.height, self.children)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x \
               and self.y == other.y \
               and self.width == other.width \
               and self.height == other.height \
               and self.children == other.children
