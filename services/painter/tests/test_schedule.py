from src.render.image import render_rects
from src.schedule.schedule import gen_rand_schedule, gen_schedule, gen_schedule_multi


def test_gen_schedule():
    date = "2022-06-13"

    schedule = gen_schedule(date)
    schedule_img = render_rects(schedule, (1080, 1080))

    if schedule_img is not None:
        schedule_img.save("a.jpg")


def test_gen_schedule_multi():
    date = "2022-06-07"

    schedules = gen_schedule_multi(date)

    for i, schedule in enumerate(schedules):
        img = render_rects(schedule, (1080, 1080))
        img.save(f"{i}.jpg")