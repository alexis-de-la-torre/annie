import numpy as np
from matplotlib import pyplot as plt


def render_points(points, color=None):
    point_width = 10

    x = []
    y = []

    for point in points:
        px, py = point
        x.append(px)
        y.append(py)

    if color is None:
        plt.scatter(x, y, s=point_width)
    else:
        plt.scatter(x, y, s=point_width, c=color)

    return None


def render_poly(vertices, color=None, render_vertices=False):
    x = []
    y = []

    for point in vertices:
        px, py = point
        x.append(px)
        y.append(py)

    x.append(vertices[0][0])
    y.append(vertices[0][1])

    if color is None:
        plt.plot(x, y)
    else:
        plt.plot(x, y, c=color)

    if render_vertices:
        render_points(vertices, color)


def render_rects(rects, color=None, render_vertices=False):
    if type(rects) != list:
        rects = [rects]

    for rect in rects:
        render_poly([(rect.x, rect.y),
                     (rect.x + rect.width, rect.y),
                     (rect.x + rect.width, rect.y + rect.height),
                     (rect.x, rect.y + rect.height)],
                    color,
                    render_vertices)


def show():
    plt.grid(True)

    # plt.xlim(0, 1500)
    # plt.ylim(0, 1500)
    # plt.xlim(0, 900)
    # plt.ylim(0, 900)
    # plt.xlim(0, 1200)
    # plt.ylim(0, 1200)
    plt.xlim(0, 600)
    plt.ylim(0, 600)
    # plt.xlim(0, 400)
    # plt.ylim(0, 400)

    plt.gca().set_aspect("equal")
    plt.gca().invert_yaxis()

    plt.show()