import numpy as np
import pytest

from src.Direction import Direction
from src.Rect import Rect
from src.render.graph import render_rects, show
from src.util.geo_util import get_min_bounding_box_points, gen_rects, collision, \
    rects_to_points, pack_rects_x, get_min_bounding_box_rects, arrange_rects_x, arrange_rects_y, \
    pack_rects_y, rects_to_sizes, sizes_to_rects, pack_rects

rects = [Rect(269.5254015709299, 308.35764522666244, 25, 25),
         Rect(336.0757465489678, 225.034884505077, 25, 25),
         Rect(291.1053504286575, 406.7092003128319, 25, 25),
         Rect(267.9532731987588, 435.4651042004117, 25, 25),
         Rect(219.46191973556188, 203.37660753031108, 25, 25)]
rects_varied_a = [Rect(269.5254015709299, 308.35764522666244, 75, 100, []),
                  Rect(336.0757465489678, 225.034884505077, 50, 50, []),
                  Rect(267.9532731987588, 435.4651042004117, 50, 75, []),
                  Rect(219.46191973556188, 203.37660753031108, 75, 100, []),
                  Rect(427.86756681983354, 258.73932870002864, 25, 100, [])]
rects_varied_b = [Rect(258.19099182048194, 353.44624972894286, 25, 75, []),
                  Rect(321.5518120475841, 92.36304287511686, 50, 50, []),
                  Rect(338.2530618903667, 239.44016773866298, 50, 100, []),
                  Rect(134.15302442953634, 176.17134036967354, 100, 25, []),
                  Rect(133.55070243793386, 114.5238071539985, 25, 25, [])]
rects_collision = [Rect(280.82901282149317, 367.53190023462395, 50, 50),
                   Rect(263.4649548990691, 389.0988281503088, 50, 50)]
rects_no_collision = [Rect(314.55680991172585, 231.27616337880775, 50, 50),
                      Rect(263.4649548990691, 389.0988281503088, 50, 50)]

points = [(269.5254015709299, 441.4473368931056),
          (336.0757465489678, 369.66342568668944),
          (291.1053504286575, 234.59174490117275),
          (267.9532731987588, 362.2116705145822),
          (219.46191973556188, 97.30977034757329),
          (308.35764522666244, 305.9684085310095),
          (225.034884505077, 107.34131496361856),
          (406.7092003128319, 427.86756681983354),
          (435.4651042004117, 258.73932870002864),
          (203.37660753031108, 215.86477599620943),
          (366.6900152330658, 155.8222448418508),
          (261.55796790116176, 359.69347577368666),
          (277.2178244375729, 232.46013288661942),
          (420.2386553170644, 277.37357954745937),
          (78.41442327915478, 57.51592017454206),
          (84.85171988061629, 297.05419883035086),
          (58.08735897613029, 294.83828908896857),
          (383.0479382191752, 296.77359874990276),
          (361.2627003799402, 427.4992314058497),
          (398.00485929872764, 322.7281196413934)]

sizes = [(25, 25), (25, 25), (25, 25), (25, 25), (25, 25)]
sizes_varied = [(75, 100), (50, 50), (50, 75), (75, 100), (25, 100)]


@pytest.fixture(autouse=True)
def setup():
    np.random.seed(0)


def test_gen_rects():
    np.random.seed(0)

    generated = gen_rects(5)

    # render_rects(generated)
    # show()

    assert generated == rects


def test_collision_a():
    assert collision(rects_collision[0], [rects_collision[1]]) is True


def test_collision_b():
    assert collision(rects_no_collision[0], [rects_no_collision[1]]) is False


def test_rects_to_sizes():
    assert rects_to_sizes(rects_varied_a) == sizes_varied


def test_sizes_to_rect():
    expected = [Rect(0, 0, 75, 100),
                Rect(0, 0, 50, 50),
                Rect(0, 0, 50, 75),
                Rect(0, 0, 75, 100),
                Rect(0, 0, 25, 100)]

    assert sizes_to_rects(sizes_varied) == expected


def test_rects_to_points():
    # render_points(rects_to_points(rects), "b")
    # show()

    expected = [(269.5254015709299, 308.35764522666244),
                (294.5254015709299, 308.35764522666244),
                (294.5254015709299, 333.35764522666244),
                (269.5254015709299, 333.35764522666244),
                (336.0757465489678, 225.034884505077),
                (361.0757465489678, 225.034884505077),
                (361.0757465489678, 250.034884505077),
                (336.0757465489678, 250.034884505077),
                (291.1053504286575, 406.7092003128319),
                (316.1053504286575, 406.7092003128319),
                (316.1053504286575, 431.7092003128319),
                (291.1053504286575, 431.7092003128319),
                (267.9532731987588, 435.4651042004117),
                (292.9532731987588, 435.4651042004117),
                (292.9532731987588, 460.4651042004117),
                (267.9532731987588, 460.4651042004117),
                (219.46191973556188, 203.37660753031108),
                (244.46191973556188, 203.37660753031108),
                (244.46191973556188, 228.37660753031108),
                (219.46191973556188, 228.37660753031108)]

    assert rects_to_points(rects) == expected


def test_min_bounding_box_points():
    # hull = get_convex_hull(points)

    min_bounding_box = get_min_bounding_box_points(points)

    # render_points(points)
    # render_poly(hull, 'purple', True)
    # render_rects(min_bounding_box, 'red', True)
    # show()

    expected = Rect(58.08735897613029, 57.51592017454206, 377.3777452242814, 383.9314167185636)

    assert min_bounding_box == expected


def test_min_bounding_box_rects():
    # points = rects_to_points(rects)
    # hull = get_convex_hull(points)
    min_bounding_box = get_min_bounding_box_rects(rects)

    # render_rects(rects, "blue")
    # render_points(points, "red")
    # render_poly(hull, "purple", True)
    # render_rects(min_bounding_box, "green", True)
    # show()

    expected = Rect(219.46191973556188,
                    203.37660753031108,
                    141.61382681340592,
                    257.08849667010065)

    assert min_bounding_box == expected


def test_pack_rects_a():
    # packed_rects = pack_rects_x(rects)
    packed_rects = pack_rects_x(sizes, rects[0].x, rects[0].y)

    # render_rects(rects, "b")
    # render_rects(packed_rects, "g")
    # show()

    expected = [Rect(269.5254015709299, 308.35764522666244, 25, 25),
                Rect(294.5254015709299, 308.35764522666244, 25, 25),
                Rect(319.5254015709299, 308.35764522666244, 25, 25),
                Rect(344.5254015709299, 308.35764522666244, 25, 25),
                Rect(369.5254015709299, 308.35764522666244, 25, 25)]

    assert packed_rects == expected


def test_pack_rects_b():
    # arranged_rects = arrange_rects_x(rects_varied)
    # min_bounding_box = get_min_bounding_box_rects(arranged_rects)
    # packed_rects = pack_rects_x(rects_varied)
    packed_rects = pack_rects_x(sizes_varied, rects_varied_a[0].x, rects_varied_a[0].y)

    # render_rects(rects, "blue")
    # render_rects(arranged_rects, "purple")
    # render_rects(packed_rects, "red")
    # render_rects(min_bounding_box, "green", True)
    # show()

    expected = [Rect(269.5254015709299, 308.35764522666244, 75, 100),
                Rect(344.5254015709299, 333.35764522666244, 50, 50),
                Rect(394.5254015709299, 320.85764522666244, 50, 75),
                Rect(444.5254015709299, 308.35764522666244, 75, 100),
                Rect(519.52540157093, 308.35764522666244, 25, 100)]

    assert packed_rects == expected


def test_pack_rects_c():
    # arranged_rects = arrange_rects_y(rects)
    # min_bounding_box = get_min_bounding_box_rects(arranged_rects)
    # packed_rects = pack_rects_y(rects_varied)
    packed_rects = pack_rects_y(sizes_varied, rects_varied_a[0].x, rects_varied_a[0].y)

    # render_rects(rects, "blue")
    # render_rects(arranged_rects, "purple")
    # render_rects(packed_rects, "red")
    # render_rects(min_bounding_box, "green", True)
    # show()

    expected = [Rect(269.5254015709299, 308.35764522666244, 75, 100),
                Rect(282.0254015709299, 408.35764522666244, 50, 50),
                Rect(282.0254015709299, 458.35764522666244, 50, 75),
                Rect(269.5254015709299, 533.3576452266625, 75, 100),
                Rect(294.5254015709299, 633.3576452266625, 25, 100)]

    assert packed_rects == expected


def test_nested_1_level():
    parent = Rect()
    parent.append(rects_varied_a)
    parent.append(rects_varied_b)

    # render_rects(parent.children, "b")
    # render_rects(parent.children[0].children, "r")
    # render_rects(parent.children[1].children, "g")
    # show()

    expected = Rect(269.5254015709299,
                    308.35764522666244,
                    525.0,
                    100.0,
                    [Rect(269.5254015709299,
                          308.35764522666244,
                          275.00000000000006,
                          100.0,
                          [Rect(269.5254015709299, 308.35764522666244, 75, 100, []),
                           Rect(344.5254015709299, 333.35764522666244, 50, 50, []),
                           Rect(394.5254015709299, 320.85764522666244, 50, 75, []),
                           Rect(444.5254015709299, 308.35764522666244, 75, 100, []),
                           Rect(519.52540157093, 308.35764522666244, 25, 100, [])]),
                     Rect(544.52540157093,
                          308.35764522666244,
                          250.0,
                          100.0,
                          [Rect(544.52540157093, 320.85764522666244, 25, 75, []),
                           Rect(569.52540157093, 333.35764522666244, 50, 50, []),
                           Rect(619.52540157093, 308.35764522666244, 50, 100, []),
                           Rect(669.52540157093, 345.85764522666244, 100, 25, []),
                           Rect(769.52540157093, 345.85764522666244, 25, 25, [])])])

    assert parent == expected


def test_nested_2_levels():
    parent_a = Rect(Direction.HORIZONTAL)
    parent_b = Rect(Direction.HORIZONTAL)

    parent_b.append(rects_varied_a)
    parent_b.append(rects_varied_b)

    parent_a.append(parent_b)
    parent_a.append(rects_varied_b)

    # render_rects(parent_a, "lime")
    # render_rects(parent_a.children[0], "orange")
    # render_rects(parent_a.children[0].children[0].children, "silver")
    # render_rects(parent_a.children[0].children[1].children, "firebrick")
    # render_rects(parent_a.children[1], "lightcoral")
    # render_rects(parent_a.children[1].children, "olive")
    # show()

    expected = Rect(269.5254015709299, 308.35764522666244, 775.0, 100.0,
                    [Rect(269.5254015709299, 308.35764522666244, 525.0, 100.0,
                          [Rect(269.5254015709299, 308.35764522666244, 275.00000000000006, 100.0,
                                [Rect(269.5254015709299, 308.35764522666244, 75, 100, []),
                                 Rect(344.5254015709299, 333.35764522666244, 50, 50, []),
                                 Rect(394.5254015709299, 320.85764522666244, 50, 75, []),
                                 Rect(444.5254015709299, 308.35764522666244, 75, 100, []),
                                 Rect(519.52540157093, 308.35764522666244, 25, 100, [])]),
                           Rect(544.52540157093, 308.35764522666244, 250.0, 100.0,
                                [Rect(544.52540157093, 320.85764522666244, 25, 75, []),
                                 Rect(569.52540157093, 333.35764522666244, 50, 50, []),
                                 Rect(619.52540157093, 308.35764522666244, 50, 100, []),
                                 Rect(669.52540157093, 345.85764522666244, 100, 25, []),
                                 Rect(769.52540157093, 345.85764522666244, 25, 25, [])])]),
                     Rect(794.52540157093, 308.35764522666244, 250.0, 100.0,
                          [Rect(794.52540157093, 320.85764522666244, 25, 75, []),
                           Rect(819.52540157093, 333.35764522666244, 50, 50, []),
                           Rect(869.52540157093, 308.35764522666244, 50, 100, []),
                           Rect(919.52540157093, 345.85764522666244, 100, 25, []),
                           Rect(1019.52540157093, 345.85764522666244, 25, 25, [])])])

    assert parent_a == expected


def test_pack_rects_nested_vertical():
    parent = Rect(direction=Direction.VERTICAL)
    parent.append(rects_varied_a, Direction.VERTICAL)
    parent.append(rects_varied_b, Direction.VERTICAL)

    # render_rects(parent.children, "g")
    # render_rects(parent.children[0].children, "b")
    # render_rects(parent.children[1].children, "k")
    # show()

    expected = pack_rects(rects_varied_a + rects_varied_b, direction=Direction.VERTICAL)
    flattened = parent.children[0].children + parent.children[1].children

    assert flattened == expected


def test_pack_rects_nested_both():
    rect = Rect(direction=Direction.HORIZONTAL)
    rect.append(rects_varied_a, Direction.HORIZONTAL)
    rect.append(rects_varied_b, Direction.VERTICAL)

    # render_rects(rect.children[0], "r")
    # render_rects(rect.children[1], "g")
    # render_rects(rect.children[0].children, "b")
    # render_rects(rect.children[1].children, "k")
    # show()

    expected = Rect(269.5254015709299, 308.3576452266624, 375.00000000000006, 274.9999999999999,
                    [Rect(269.5254015709299, 395.8576452266624, 275.00000000000006, 100.0,
                          [Rect(269.5254015709299, 395.8576452266624, 75, 100, []),
                           Rect(344.5254015709299, 420.8576452266624, 50, 50, []),
                           Rect(394.5254015709299, 408.3576452266624, 50, 75, []),
                           Rect(444.5254015709299, 395.8576452266624, 75, 100, []),
                           Rect(519.52540157093, 395.8576452266624, 25, 100, [])]),
                     Rect(544.52540157093, 308.3576452266624, 100.0, 274.99999999999994,
                          [Rect(582.02540157093, 308.3576452266624, 25, 75, []),
                           Rect(569.52540157093, 383.3576452266624, 50, 50, []),
                           Rect(569.52540157093, 433.3576452266624, 50, 100, []),
                           Rect(544.52540157093, 533.3576452266624, 100, 25, []),
                           Rect(582.02540157093, 558.3576452266624, 25, 25, [])])])

    assert rect == expected


def test_pack_rects_nested_both_b():
    rect = Rect(direction=Direction.HORIZONTAL)
    rect.append(rects_varied_a, Direction.HORIZONTAL)
    rect.append(rects_varied_b, Direction.VERTICAL)
    rect.append(rects_varied_a, Direction.HORIZONTAL)

    # render_rects(rect.children, "r")
    # render_rects(rect.children[0].children, "g")
    # render_rects(rect.children[1].children, "b")
    # render_rects(rect.children[2].children, "k")
    # show()

    expected = Rect(269.5254015709299, 395.85764522666227, 650.0, 275.0,
                    [Rect(269.5254015709299, 483.35764522666227, 275.00000000000006, 100.0,
                          [Rect(269.5254015709299, 483.35764522666227, 75, 100, []),
                           Rect(344.5254015709299, 508.35764522666227, 50, 50, []),
                           Rect(394.5254015709299, 495.85764522666227, 50, 75, []),
                           Rect(444.5254015709299, 483.35764522666227, 75, 100, []),
                           Rect(519.52540157093, 483.35764522666227, 25, 100, [])]),
                     Rect(544.52540157093, 395.85764522666227, 100.0, 274.99999999999994,
                          [Rect(582.02540157093, 395.85764522666227, 25, 75, []),
                           Rect(569.52540157093, 470.85764522666227, 50, 50, []),
                           Rect(569.52540157093, 520.8576452266623, 50, 100, []),
                           Rect(544.52540157093, 620.8576452266623, 100, 25, []),
                           Rect(582.02540157093, 645.8576452266623, 25, 25, [])]),
                     Rect(644.52540157093, 483.35764522666227, 275.00000000000006, 100.0,
                          [Rect(644.52540157093, 483.35764522666227, 75, 100, []),
                           Rect(719.52540157093, 508.35764522666227, 50, 50, []),
                           Rect(769.52540157093, 495.85764522666227, 50, 75, []),
                           Rect(819.52540157093, 483.35764522666227, 75, 100, []),
                           Rect(894.52540157093, 483.35764522666227, 25, 100, [])])])

    assert rect == expected


def test_6741():
    rect = Rect(0, 0, direction=Direction.HORIZONTAL)
    rect.append([Rect(50, 50, 50, 50), Rect(0, 0, 60, 60)], Direction.VERTICAL)

    # render_rects(rect, "r")
    # render_rects(rect.children, "g")
    # render_rects(rect.children[0].children, "b")
    #
    # show()

    expected = pack_rects_y([Rect(50, 50, 50, 50), Rect(0, 0, 60, 60)])

    assert rect.children[0].children == expected


def test_pack_rects_games():
    game = Rect(0, 0, direction=Direction.HORIZONTAL)
    game.append([Rect(50, 50, 80, 80)], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 40, 40), Rect(0, 0, 80, 20)], Direction.VERTICAL)
    game.append([Rect(0, 0, 80, 80)], Direction.HORIZONTAL)

    parent = Rect()
    parent.append([game, game, game], direction=Direction.VERTICAL)


    # render_rects(parent, "r")
    # render_rects(parent.children[0].children, "g")
    # render_rects(parent.children[0].children[0].children[0].children, "b")
    # render_rects(parent.children[0].children[0].children[1].children, "b")
    # render_rects(parent.children[0].children[0].children[2].children, "b")
    #
    # render_rects(parent.children[0].children[1].children[0].children, "orange")
    # render_rects(parent.children[0].children[1].children[1].children, "orange")
    # render_rects(parent.children[0].children[1].children[2].children, "orange")
    #
    # render_rects(parent.children[0].children[2].children[0].children, "salmon")
    # render_rects(parent.children[0].children[2].children[1].children, "salmon")
    # render_rects(parent.children[0].children[2].children[2].children, "salmon")
    #
    # show()

    expected = Rect(50.0, 50.0, 240.0, 240.0,
                    [Rect(50.0, 50.0, 240.0, 240.0,
                          [Rect(50.0, 50.0, 240.0, 80.0,
                                [Rect(50.0, 50.0, 80, 80.0,
                                      [Rect(50.0, 50.0, 80, 80, [])]),
                                 Rect(130.0, 60.0, 80.0, 60,
                                      [Rect(150.0, 60.0, 40, 40, []),
                                       Rect(130.0, 100.0, 80, 20, [])]),
                                 Rect(210.0, 50.0, 80, 80.0,
                                      [Rect(210.0, 50.0, 80, 80, [])])]),
                           Rect(50.0, 130.0, 240.0, 80.0,
                                [Rect(50.0, 130.0, 80, 80.0,
                                      [Rect(50.0, 130.0, 80, 80, [])]),
                                 Rect(130.0, 140.0, 80.0, 60,
                                      [Rect(150.0, 140.0, 40, 40, []),
                                       Rect(130.0, 180.0, 80, 20, [])]),
                                 Rect(210.0, 130.0, 80, 80.0,
                                      [Rect(210.0, 130.0, 80, 80, [])])]),
                           Rect(50.0, 210.0, 240.0, 80.0,
                                [Rect(50.0, 210.0, 80, 80.0,
                                      [Rect(50.0, 210.0, 80, 80, [])]),
                                 Rect(130.0, 220.0, 80.0, 60,
                                      [Rect(150.0, 220.0, 40, 40, []),
                                       Rect(130.0, 260.0, 80, 20, [])]),
                                 Rect(210.0, 210.0, 80, 80.0,
                                      [Rect(210.0, 210.0, 80, 80, [])])])])])

    assert parent == expected
