import pytest

from src.render.image import render_rects
from src.schedule.schedule import gen_rand_schedule

from src.upload import gcloud_storage


@pytest.mark.skip()
def test_upload_img():
    date = "2021-05-31"

    schedule = gen_rand_schedule(date)
    schedule_img = render_rects(schedule, (1080, 1080))
    gcloud_storage.upload_img(schedule_img, date)