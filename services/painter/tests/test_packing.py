from src.Direction import Direction
from src.geo.Rect import Rect
from src.geo.packing import pack_rects_x, pack_rects_y, pack_rects

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


sizes = [(25, 25), (25, 25), (25, 25), (25, 25), (25, 25)]
sizes_varied = [(75, 100), (50, 50), (50, 75), (75, 100), (25, 100)]


def test_pack_rects_a():
    packed_rects = pack_rects_x(sizes, rects[0].x, rects[0].y)

    # # render_rects(rects, "r")
    # render_rects(packed_rects, "g")
    # show()

    # image.render_rects(packed_rects, (600, 600))

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

    # # render_rects(rects, "blue")
    # # render_rects(arranged_rects, "purple")
    # render_rects(packed_rects, "red")
    # # render_rects(min_bounding_box, "green", True)
    # show()

    # image.render_rects(packed_rects, (600, 600))

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

    # # render_rects(rects, "blue")
    # # render_rects(arranged_rects, "purple")
    # render_rects(packed_rects, "red")
    # # render_rects(min_bounding_box, "green", True)
    # show()

    # image.render_rects(packed_rects, (800, 800))

    expected = [Rect(269.5254015709299, 308.35764522666244, 75, 100),
                Rect(282.0254015709299, 408.35764522666244, 50, 50),
                Rect(282.0254015709299, 458.35764522666244, 50, 75),
                Rect(269.5254015709299, 533.3576452266625, 75, 100),
                Rect(294.5254015709299, 633.3576452266625, 25, 100)]

    assert packed_rects == expected


def test_nested_one_level():
    parent = Rect()
    parent.append(rects_varied_a)
    parent.append(rects_varied_b)

    # render_rects(parent.children, "b")
    # render_rects(parent.children[0].children, "r")
    # render_rects(parent.children[1].children, "g")
    # show()
    #
    # image.render_rects(parent, (800, 800))

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


def test_nested_two_levels():
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

    # image.render_rects(parent_a, (1200, 1200), 200)

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
    #
    # image.render_rects(parent, (1200, 1200), 200)

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
    #
    # image.render_rects(rect, grid_size=200)

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

    # image.render_rects(rect, 1200, 200)

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

    # image.render_rects(rect)

    expected = pack_rects_y([Rect(50, 50, 50, 50), Rect(0, 0, 60, 60)])

    assert rect.children[0].children == expected


def test_pack_rects_games():
    game = Rect(0, 0, direction=Direction.HORIZONTAL)
    game.append([Rect(200, 200, 240, 240, image="suns")], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 120, 100, image="vs"), Rect(0, 0, 140, 31, image="time")], Direction.VERTICAL)
    game.append([Rect(0, 0, 240, 240, image="mavericks")], Direction.HORIZONTAL)

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

    # image.render_rects(parent, (1080, 1080))

    expected = Rect(200.0, 200.0, 620.0, 720.0,
                    [Rect(200.0, 200.0, 620.0, 720.0,
                          [Rect(200.0, 200.0, 620.0, 240.0,
                                [Rect(200.0, 200.0, 240, 240.0,
                                      [Rect(200.0, 200.0, 240, 240, [])]),
                                 Rect(440.0, 254.5, 140.0, 131,
                                      [Rect(450.0, 254.5, 120, 100, []),
                                       Rect(440.0, 354.5, 140, 31, [])]),
                                 Rect(580.0, 200.0, 240, 240.0,
                                      [Rect(580.0, 200.0, 240, 240, [])])]),
                           Rect(200.0, 440.0, 620.0, 240.0,
                                [Rect(200.0, 440.0, 240, 240.0,
                                      [Rect(200.0, 440.0, 240, 240, [])]),
                                 Rect(440.0, 494.5, 140.0, 131,
                                      [Rect(450.0, 494.5, 120, 100, []),
                                       Rect(440.0, 594.5, 140, 31, [])]),
                                 Rect(580.0, 440.0, 240, 240.0,
                                      [Rect(580.0, 440.0, 240, 240, [])])]),
                           Rect(200.0, 680.0, 620.0, 240.0,
                                [Rect(200.0, 680.0, 240, 240.0,
                                      [Rect(200.0, 680.0, 240, 240, [])]),
                                 Rect(440.0, 734.5, 140.0, 131,
                                      [Rect(450.0, 734.5, 120, 100, []),
                                       Rect(440.0, 834.5, 140, 31, [])]),
                                 Rect(580.0, 680.0, 240, 240.0,
                                      [Rect(580.0, 680.0, 240, 240, [])])])])])

    assert parent == expected