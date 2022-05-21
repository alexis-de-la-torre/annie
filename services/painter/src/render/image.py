import os

from PIL import Image, ImageFont, ImageDraw
from src.geo.rect_util import flatten_rects


def render_rects(rects, canvas_size=(600, 600)):
    if type(canvas_size) is not tuple:
        canvas_size = (canvas_size, canvas_size)

    rects = flatten_rects(rects)

    canvas = Image.new('RGBA', canvas_size, "#852127")

    default_img = "../img/bucks.png"

    script_dir = os.path.dirname(os.path.abspath(__file__))

    font_path = os.path.join(script_dir, '..', '..', 'fonts', 'Roboto-Black.ttf')

    for rect in rects:
        if rect.image is not None:
            img_canvas = Image.new('RGBA', canvas_size)

            path = os.path.join(script_dir, '..', '..', 'img', f"{rect.image}.png")

            img = Image.open(path if rect.image is not None else default_img) \
                .convert('RGBA')
            img = img.resize((int(rect.width), int(rect.height)))

            img_canvas.alpha_composite(img, (int(rect.x), int(rect.y)))

            canvas.alpha_composite(img_canvas)

        if rect.text is not None:
            txt = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
            fnt = ImageFont.truetype(font_path, rect.text_size)
            d = ImageDraw.Draw(txt)
            d.text((int(rect.x), int(rect.y)), rect.text, font=fnt, fill=(255, 255, 255, 255))
            canvas.alpha_composite(txt)

    return canvas.convert("RGB")
