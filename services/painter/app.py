from flask import Flask, request

from src.render.image import render_rects
from src.schedule.schedule import gen_schedule
from src.upload import gcloud_storage

app = Flask(__name__)


@app.route('/schedules', methods=['POST'])
def schedules():
    data = request.get_json()
    date = data["date"]

    schedule = gen_schedule(date)
    schedule_img = render_rects(schedule, (1080, 1080))
    return gcloud_storage.upload_img(schedule_img, date)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


