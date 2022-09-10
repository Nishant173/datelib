from typing import Tuple

from datelib.constants import (
    DAY_NUMBER_TO_NAME_MAPPER,
    NUM_DAYS_IN_WEEK,
    YEARS_HAVING_JANUARY_1ST_AS_SATURDAY,
)
from datelib.utils import (
    argmin,
    is_leap_year,
)


def _get_reference_date_details(year: int) -> Tuple[int, int, str]:
    """
    Gets reference date which is closest to the given `year` (to speed up day-of-week calculation).
    Returns tuple of (reference_year, reference_dow_number, reference_dow_name)
    """
    year_differences = [abs(year - year_) for year_ in YEARS_HAVING_JANUARY_1ST_AS_SATURDAY]
    reference_year = YEARS_HAVING_JANUARY_1ST_AS_SATURDAY[argmin(year_differences)]
    assert is_leap_year(reference_year), f"Invalid configuration. The `reference_year` needs to be a leap year, but got year {reference_year}"
    return (reference_year, 6, DAY_NUMBER_TO_NAME_MAPPER[6])


def _get_day_of_week_on_january_1st(year: int) -> Tuple[int, str]:
    """Returns tuple of (dow_number, dow_name) of the day on January 1st of the given `year`"""
    reference_year, reference_dow_number, reference_dow_name = _get_reference_date_details(year=year)
    if year == reference_year:
        return (reference_dow_number, reference_dow_name)
    is_year_ahead_of_reference = (year > reference_year)
    num_years_between = int(abs(year - reference_year))
    num_leap_years_between = 0
    step_size = 4 if is_year_ahead_of_reference else -4
    if is_year_ahead_of_reference:
        for year_ in range(reference_year, year + 1, step_size):
            if is_leap_year(year_) and year_ != year:
                num_leap_years_between += 1
        num_days_away = (num_years_between + num_leap_years_between) % NUM_DAYS_IN_WEEK
    else:
        for year_ in range(reference_year, year - 1, step_size):
            if is_leap_year(year_) and year_ != reference_year:
                num_leap_years_between += 1
        num_days_away = NUM_DAYS_IN_WEEK - ((num_years_between + num_leap_years_between) % NUM_DAYS_IN_WEEK)
    dow_number = (reference_dow_number + num_days_away) % NUM_DAYS_IN_WEEK
    dow_number = NUM_DAYS_IN_WEEK if dow_number == 0 else dow_number
    dow_name = DAY_NUMBER_TO_NAME_MAPPER[dow_number]
    return (dow_number, dow_name)


def get_day_of_week(*, year: int, month: int, day: int) -> str:
    jan1st_dow_number, _ = _get_day_of_week_on_january_1st(year=year)
    _MONTH_TO_FIRST_SAME_DAY_MAPPER = {
        1: 1,
        2: 5,
        3: 5,
        4: 2,
        5: 7,
        6: 4,
        7: 2,
        8: 6,
        9: 3,
        10: 1,
        11: 5,
        12: 3,
    }
    num_days_away = (day - _MONTH_TO_FIRST_SAME_DAY_MAPPER[month]) % NUM_DAYS_IN_WEEK
    num_days_away = num_days_away + NUM_DAYS_IN_WEEK if num_days_away < 0 else num_days_away
    days_difference = jan1st_dow_number + num_days_away
    if is_leap_year(year) and month > 2:
        days_difference += 1
    dow_number = days_difference % NUM_DAYS_IN_WEEK
    dow_number = NUM_DAYS_IN_WEEK if dow_number == 0 else dow_number
    day_of_week = DAY_NUMBER_TO_NAME_MAPPER[dow_number]
    return day_of_week