import uuid

from flask import Flask, request, jsonify

from src.render.image import render_rects
from src.schedule.schedule import gen_rand_schedule, gen_schedule, gen_schedule_multi
from src.upload import gcloud_storage

app = Flask(__name__)


@app.route('/api/v1/nba_schedules', methods=['POST'])
def schedules_nba_v1():
    data = request.get_json()
    date = data["date"]

    schedules = gen_schedule_multi(date)

    if len(schedules) == 0:
        return f"No games today: {date}"

    url_acc = []

    for schedule in schedules:
        schedule_img = render_rects(schedule, (1080, 1080))

        if schedule_img is not None:
            url = gcloud_storage.upload_img(schedule_img, uuid.uuid4().hex)
            url_acc.append(url)

    return jsonify(url_acc)


@app.route('/nba/schedules', methods=['POST'])
def schedules_nba():
    data = request.get_json()
    date = data["date"]

    schedule = gen_schedule(date)
    schedule_img = render_rects(schedule, (1080, 1080))

    if schedule_img is not None:
        return gcloud_storage.upload_img(schedule_img, date)
    else:
        return f"No games today: {date}"


@app.route('/schedules', methods=['POST'])
def schedules_random():
    data = request.get_json()
    date = data["date"]

    schedule = gen_rand_schedule(date)
    schedule_img = render_rects(schedule, (1080, 1080))
    return gcloud_storage.upload_img(schedule_img, date)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


