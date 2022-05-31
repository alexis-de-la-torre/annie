import locale

import dateutil.parser
import numpy as np

from src.Direction import Direction
from src.geo.Rect import Rect

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


def gen_game_s(team_a, team_b, time):
    game = Rect(0, 0, direction=Direction.HORIZONTAL)
    game.append([Rect(220, 240, 140, 140, image=team_a)], Direction.HORIZONTAL)
    game.append([gen_margin()], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 120, 100, image="vs")], Direction.HORIZONTAL)
    game.append([gen_margin()], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 140, 140, image=team_b)], Direction.HORIZONTAL)
    game.append([gen_margin(40)], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 160, 31, text=time)], Direction.HORIZONTAL)
    return game


def gen_game_m(team_a, team_b, time):
    game = Rect(0, 0, direction=Direction.HORIZONTAL)
    game.append([Rect(0, 0, 240, 240, image=team_a)], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 40, 10)], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 100, 80, image="vs"), Rect(0, 0, 140, 31, text=time)], Direction.VERTICAL)
    game.append([Rect(0, 0, 40, 10)], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 240, 240, image=team_b)], Direction.HORIZONTAL)
    return game


def gen_game_l(team_a, team_b, time):
    game = Rect(0, 0, direction=Direction.HORIZONTAL)
    game.append([Rect(0, 0, 280, 280, image=team_a)], Direction.HORIZONTAL)
    game.append([gen_margin(60)], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 140, 120, image="vs"), gen_margin(), Rect(0, 0, 180, 100, text=time, text_size=50)], Direction.VERTICAL)
    game.append([gen_margin(60)], Direction.HORIZONTAL)
    game.append([Rect(0, 0, 280, 280, image=team_b)], Direction.HORIZONTAL)
    return game


def gen_schedule_s(qty, date):
    title = Rect()
    title.append([Rect(0, 0, 160, 80, image="nba-logo"),
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
    title.append([Rect(0, 0, 160, 80, image="nba-logo"),
               gen_margin(40),
               Rect(0, 0, 500, 50, text=date)])

    schedule = Rect(direction=Direction.VERTICAL)
    schedule.append([Rect(0, 0, 1080, 180)], direction=Direction.HORIZONTAL)
    schedule.append(title)
    schedule.append([gen_margin(220)], direction=Direction.HORIZONTAL)
    schedule.append(gen_games(qty), direction=Direction.VERTICAL)

    return schedule


def gen_schedule(date):
    # locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

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
