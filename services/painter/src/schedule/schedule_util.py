import locale
import os

import dateutil.parser


def match_dates(date_a_str, dates_b):
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    for i, date_b in enumerate(dates_b):
        date_b = date_b['date'].upper().strip()

        date_a = dateutil.parser.parse(date_a_str)

        if os.name == 'nt':
            date_a_formated = date_a.strftime("%A, %#d de %B, %Y").upper()
        else:
            date_a_formated = date_a.strftime("%A, %-d de %B, %Y").upper()

        if date_a_formated == date_b:
            return i

    return None


def match_dates_v2(date_a_str, date_b):
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    # for i, date_b in enumerate(dates_b):
    date_b = date_b.upper().strip()

    date_a = dateutil.parser.parse(date_a_str)

    if os.name == 'nt':
        date_a_formated = date_a.strftime("%A, %#d de %B, %Y").upper()
    else:
        date_a_formated = date_a.strftime("%A, %-d de %B, %Y").upper()

    return date_a_formated == date_b

    # return None