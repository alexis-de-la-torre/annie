from PIL import Image, ImageDraw


def render_rects(rects, canvas_size):
    canvas = Image.new('RGB', canvas_size, "white")

    draw = ImageDraw.Draw(canvas)

    for rect in rects:
        rectangle = (rect.x, rect.y,
                     rect.x + rect.width,
                     rect.y + rect.height)

        draw.rectangle(rectangle)

    canvas.show()
