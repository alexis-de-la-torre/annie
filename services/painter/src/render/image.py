from PIL import Image

from src.geo.rect_util import flatten_rects


def render_rects(rects, canvas_size=(600, 600), grid_size=100):
    if type(canvas_size) is not tuple:
        canvas_size = (canvas_size, canvas_size)

    rects = flatten_rects(rects)

    canvas = Image.new('RGBA', canvas_size, "#852127")

    # Grid

    # draw = ImageDraw.Draw(canvas)
    # y_start = 0
    # y_end = canvas.height
    # step_size = grid_size
    #
    # for x in range(0, canvas.width, step_size):
    #     line = ((x, y_start), (x, y_end))
    #     draw.line(line, fill="grey")
    #
    # x_start = 0
    # x_end = canvas.width
    #
    # for y in range(0, canvas.height, step_size):
    #     line = ((x_start, y), (x_end, y))
    #     draw.line(line, fill="grey")
    #
    # del draw

    #

    default_img = "../img/bucks.png"

    for rect in rects:
        img_canvas = Image.new('RGBA', canvas_size)

        img = Image.open(f"../img/{rect.image}.png" if rect.image is not None else default_img)\
            .convert('RGBA')
        img = img.resize((int(rect.width), int(rect.height)))

        img_canvas.alpha_composite(img, (int(rect.x), int(rect.y)))

        canvas.alpha_composite(img_canvas)

    canvas.show()
