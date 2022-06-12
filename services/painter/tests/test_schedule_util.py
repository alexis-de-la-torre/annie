from src.schedule.schedule_util import match_dates


def test_match_dates():
    assert match_dates("2022-06-08", 'Miércoles, 8 de Junio, 2022 ') is True
    assert match_dates("2022-06-10", 'Viernes, 10 de Junio, 2022 ') is True
    assert match_dates("2022-06-13", 'Lunes, 13 de Junio, 2022 ') is True
