import locale
import os

import dateutil.parser
import numpy as np
import requests

from src.Direction import Direction
from src.geo.Rect import Rect
from src.schedule.schedule_util import match_dates, match_dates_v2
from src.util import chunks

teams = ["mavericks",
         "suns",
         "76ers",
         "bucks",
         "celtics",
         "grizzlies",
         "heat",
         "warriors"]


def random_team(exclude=None):
    if exclude is None:
        return np.random.choice(teams)
    else:
        return np.random.choice(list(filter(lambda t: t not in exclude, teams)))


def random_time():
    hour = np.random.choice(range(1, 12))
    minute = np.random.choice(range(0, 60, 15))
    period = np.random.choice(["AM", "PM"])

    if minute == 0:
        minute = "00"

    return f"{hour}:{minute} {period}"


def gen_game_s(team_a, team_b, time, team_a_id=None, team_b_id=None, team_a_logo=None, team_b_logo=None):
    if team_a_logo is None:
        game = Rect(0, 0, direction=Direction.HORIZONTAL)
        game.append([Rect(220, 240, 140, 140, image=team_a)], Direction.HORIZONTAL)
        game.append([gen_margin()], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 120, 100, image="vs")], Direction.HORIZONTAL)
        game.append([gen_margin()], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 140, 140, image=team_b)], Direction.HORIZONTAL)
        game.append([gen_margin(40)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 160, 31, text=time)], Direction.HORIZONTAL)
        return game
    else:
        game = Rect(0, 0, direction=Direction.HORIZONTAL)
        game.append([Rect(220, 240, 140, 140, image_ext=team_a_logo, team_id=team_a_id)], Direction.HORIZONTAL)
        game.append([gen_margin()], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 120, 100, image="vs")], Direction.HORIZONTAL)
        game.append([gen_margin()], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 140, 140, image_ext=team_b_logo, team_id=team_b_id)], Direction.HORIZONTAL)
        game.append([gen_margin(40)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 160, 31, text=time)], Direction.HORIZONTAL)
        return game


def gen_game_m(team_a, team_b, time, team_a_id=None, team_b_id=None, team_a_logo=None, team_b_logo=None):
    if team_a_logo is None:
        game = Rect(0, 0, direction=Direction.HORIZONTAL)
        game.append([Rect(0, 0, 240, 240, image=team_a)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 40, 10)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 100, 80, image="vs"), Rect(0, 0, 140, 31, text=time)], Direction.VERTICAL)
        game.append([Rect(0, 0, 40, 10)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 240, 240, image=team_b)], Direction.HORIZONTAL)
        return game
    else:
        game = Rect(0, 0, direction=Direction.HORIZONTAL)
        game.append([Rect(0, 0, 240, 240, image_ext=team_a_logo, team_id=team_a_id)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 40, 10)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 100, 80, image="vs"), Rect(0, 0, 140, 31, text=time)], Direction.VERTICAL)
        game.append([Rect(0, 0, 40, 10)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 240, 240, image_ext=team_b_logo, team_id=team_b_id)], Direction.HORIZONTAL)
        return game

def gen_game_l(team_a, team_b, time, team_a_id=None, team_b_id=None, team_a_logo=None, team_b_logo=None):
    if team_a_logo is None:
        game = Rect(0, 0, direction=Direction.HORIZONTAL)
        game.append([Rect(0, 0, 280, 280, image=team_a)], Direction.HORIZONTAL)
        game.append([gen_margin(60)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 140, 120, image="vs"), gen_margin(), Rect(0, 0, 180, 100, text=time, text_size=50)],
                    Direction.VERTICAL)
        game.append([gen_margin(60)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 280, 280, image=team_b)], Direction.HORIZONTAL)
        return game
    else:
        game = Rect(0, 0, direction=Direction.HORIZONTAL)
        game.append([Rect(0, 0, 280, 280, image_ext=team_a_logo, team_id=team_a_id)], Direction.HORIZONTAL)
        game.append([gen_margin(60)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 140, 120, image="vs"), gen_margin(), Rect(0, 0, 180, 100, text=time, text_size=50)],
                    Direction.VERTICAL)
        game.append([gen_margin(60)], Direction.HORIZONTAL)
        game.append([Rect(0, 0, 280, 280, image_ext=team_b_logo, team_id=team_b_id)], Direction.HORIZONTAL)
        return game


def gen_schedule_s(qty, date):
    title = Rect()
    title.append([Rect(0, 0, 160, 100, image="mlb"),
               gen_margin(40),
               Rect(0, 0, 500, 50, text=date)])

    schedule = Rect(direction=Direction.VERTICAL)
    schedule.append([Rect(0, 0, 1080, 80)], direction=Direction.HORIZONTAL)
    schedule.append(title)
    schedule.append([gen_margin(80)], direction=Direction.HORIZONTAL)
    schedule.append(gen_games(qty), direction=Direction.VERTICAL)

    return schedule


def gen_schedule_l(qty, date):
    title = Rect()
    title.append([Rect(0, 0, 160, 100, image="mlb"),
               gen_margin(40),
               Rect(0, 0, 500, 50, text=date)])

    schedule = Rect(direction=Direction.VERTICAL)
    schedule.append([Rect(0, 0, 1080, 180)], direction=Direction.HORIZONTAL)
    schedule.append(title)
    schedule.append([gen_margin(220)], direction=Direction.HORIZONTAL)
    schedule.append(gen_games(qty), direction=Direction.VERTICAL)

    return schedule


def gen_schedule(date_str):
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    date = dateutil.parser.parse(date_str)
    date_formated = date.strftime("%A %d de %B").upper()\

    mapache_host = os.environ['MAPACHE_HOST']
    mapache_port = os.environ['MAPACHE_PORT']

    mapache_addr = f"http://{mapache_host}:{mapache_port}/crawl.json?spider_name=espn-nba&start_requests=true"

    res = requests.get(mapache_addr).json()

    mapache_schedules = res['items']

    title = Rect()
    title.append([Rect(0, 0, 160, 100, image="mlb"),
                  gen_margin(40),
                  # Rect(0, 0, 500, 50, text=mapache_schedules[0]['date'])])
                  Rect(0, 0, 500, 50, text=date_formated)])

    schedule = Rect(direction=Direction.VERTICAL)
    schedule.append([Rect(0, 0, 1080, 80)], direction=Direction.HORIZONTAL)
    schedule.append(title)
    schedule.append([gen_margin(80)], direction=Direction.HORIZONTAL)

    index_matched = None



    # isMatch = match_dates(date_str, mapache_schedules[0]['date'])
    matched_index = match_dates(date_str, mapache_schedules)

    if matched_index is not None:
        acc = []

        team_a = mapache_schedules[matched_index]['team-a'].lower().replace(' ', '-')
        team_b = mapache_schedules[matched_index]['team-b'].lower().replace(' ', '-')
        team_a_id = mapache_schedules[matched_index]['team-a-id']
        team_b_id = mapache_schedules[matched_index]['team-b-id']
        team_a_logo = mapache_schedules[matched_index]['team-a-logo'].lower().replace(' ', '-')
        team_b_logo = mapache_schedules[matched_index]['team-b-logo'].lower().replace(' ', '-')

        acc.append(gen_game_l(team_a,
                              team_b,
                              mapache_schedules[matched_index]['time'],
                              team_a_id=team_a_id,
                              team_b_id=team_b_id,
                              team_a_logo=team_a_logo,
                              team_b_logo=team_b_logo,))

        schedule.append(acc, direction=Direction.VERTICAL)

        return schedule

    else:
        return []


def gen_schedule_multi(date_str):
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    date = dateutil.parser.parse(date_str)
    date_formated = date.strftime("%A %d de %B").upper()\

    mapache_host = os.environ['MAPACHE_HOST']
    mapache_port = os.environ['MAPACHE_PORT']

    mapache_addr = f"http://{mapache_host}:{mapache_port}/crawl.json?spider_name=espn-mlb&start_requests=true"

    res = requests.get(mapache_addr).json()

    mapache_schedules = res['items']

    filtered = list(filter(lambda sch: match_dates_v2(date_str, sch['date']), mapache_schedules))

    chunked = list(chunks(filtered, 5))

    schedule_acc = []

    for chunk in chunked:
        title = Rect()
        title.append([Rect(0, 0, 160, 100, image="mlb"),
                      gen_margin(40),
                      # Rect(0, 0, 500, 50, text=mapache_schedules[0]['date'])])
                      Rect(0, 0, 500, 50, text=date_formated)])

        schedule = Rect(direction=Direction.VERTICAL)
        schedule.append([Rect(0, 0, 1080, 80)], direction=Direction.HORIZONTAL)
        schedule.append(title)
        schedule.append([gen_margin(80)], direction=Direction.HORIZONTAL)

        acc = []

        chunk_length = len(chunk)

        for game in chunk:
            team_a = game['team-a'].lower().replace(' ', '-')
            team_b = game['team-b'].lower().replace(' ', '-')
            team_a_id = game['team-a-id']
            team_b_id = game['team-b-id']
            team_a_logo = game['team-a-logo'].lower().replace(' ', '-')
            team_b_logo = game['team-b-logo'].lower().replace(' ', '-')

            if chunk_length == 1:
                acc.append(gen_game_l(team_a,
                                      team_b,
                                      game['time'],
                                      team_a_id=team_a_id,
                                      team_b_id=team_b_id,
                                      team_a_logo=team_a_logo,
                                      team_b_logo=team_b_logo, ))
            elif chunk_length <= 3:
                acc.append(gen_game_m(team_a,
                                      team_b,
                                      game['time'],
                                      team_a_id=team_a_id,
                                      team_b_id=team_b_id,
                                      team_a_logo=team_a_logo,
                                      team_b_logo=team_b_logo, ))
            else:
                acc.append(gen_game_s(team_a,
                                      team_b,
                                      game['time'],
                                      team_a_id=team_a_id,
                                      team_b_id=team_b_id,
                                      team_a_logo=team_a_logo,
                                      team_b_logo=team_b_logo, ))

        schedule.append(acc, direction=Direction.VERTICAL)

        schedule_acc.append(schedule)

    return schedule_acc


def gen_rand_schedule(date, qty=None):
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    if qty is None:
        qty = np.random.choice(range(1, 5))

    date = dateutil.parser.parse(date)
    date = date.strftime("%A %d de %B %H:%M").upper()

    if qty == 1:
        return gen_schedule_l(qty, date)
    elif qty <= 3:
        return gen_schedule_s(qty, date)
    else:
        return gen_schedule_s(qty, date)


def gen_margin(size=20):
    return Rect(0, 0, size, size)


def gen_games(qty):
    acc = []

    for i in range(qty):
        team_a = random_team()
        team_b = random_team([team_a])
        time = random_time()

        if qty == 1:
            acc.append(gen_game_l(team_a, team_b, time))
        elif qty <= 3:
            acc.append(gen_game_m(team_a, team_b, time))
        else:
            acc.append(gen_game_s(team_a, team_b, time))

        acc.append(gen_margin())

    return acc
