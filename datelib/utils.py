from typing import Any, Dict, List

from datelib.constants import (
    DAY_COUNTS_IN_LEAP_YEAR_BY_MONTH,
    DAY_COUNTS_IN_NON_LEAP_YEAR_BY_MONTH,
    NUM_DAYS_IN_LEAP_YEAR,
    NUM_DAYS_IN_NON_LEAP_YEAR,
)


def get_type_name(obj: Any, /) -> str:
    return type(obj).__name__


def argmin(iterable: List[Any]) -> int:
    """Returns index of lowest element in the given `iterable`"""
    low_idx, low_item = 0, iterable[0]
    for idx, item in enumerate(iterable[1:]):
        idx += 1
        if item < low_item:
            low_idx, low_item = idx, item
    return low_idx


def is_leap_year(year: int, /) -> bool:
    if year % 4 != 0:
        return False
    if year % 100 != 0:
        return True
    return True if year % 400 == 0 else False


def get_two_digit_0_padding(integer: int) -> str:
    """Returns string of padded one/two digit positive integer"""
    assert 1 <= integer <= 99, "Integer needs to be in range 1-99"
    if 1 <= integer <= 9:
        return f"0{integer}"
    return f"{integer}"


def get_days_count_in_year(year: int, /) -> int:
    return NUM_DAYS_IN_LEAP_YEAR if is_leap_year(year) else NUM_DAYS_IN_NON_LEAP_YEAR


def get_days_count_between_months(*, year: int, start_month: int, end_month: int) -> int:
    assert (1 <= start_month <= 12) and (1 <= end_month <= 12), "Given start/end months must be in range 1-12"
    assert start_month <= end_month, "Parameter `start_month` must be <= `end_month`"
    _is_leap_year = False
    includes_february = 2 in range(start_month, end_month + 1)
    if includes_february:
        _is_leap_year = is_leap_year(year)
    if _is_leap_year:
        return sum(DAY_COUNTS_IN_LEAP_YEAR_BY_MONTH[start_month - 1 : end_month])
    return sum(DAY_COUNTS_IN_NON_LEAP_YEAR_BY_MONTH[start_month - 1 : end_month])


def get_days_in_month(*, year: int, month: int) -> int:
    return get_days_count_between_months(year=year, start_month=month, end_month=month)


def get_days_remaining_in_month(*, year: int, month: int, day: int) -> int:
    return get_days_in_month(year=year, month=month) - day


def get_days_per_month_mapper(year: int) -> Dict[int, int]:
    """
    Returns dictionary having number of days per month (in any given year).
    i.e; keys = month number, and values = number of days in said month.
    NOTE: The keys having month numbers will be in ascending order.
    """
    return {
        1: 31,
        2: 29 if is_leap_year(year) else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }


def get_days_per_month_mapper_for_multiple_years(years: List[int]) -> Dict[int, Dict[int, int]]:
    """
    Returns dictionary having number of days per month (for all the given years).
    NOTE: The keys having years/months will be in ascending order.

    >>> sample_output = {
        2020: {
            1: 31,
            2: 29,
            3: 31,
            4: 30,
            ...
        },
        2021: {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            ...
        },
    }
    """
    BASE_MAPPER = {
        1: 31,
        2: 28, # Will change to 29 for leap years
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    full_mapper = {}
    for year in sorted(years, reverse=False):
        base_mapper_copy = BASE_MAPPER.copy()
        if is_leap_year(year):
            base_mapper_copy[2] = 29
        full_mapper[year] = base_mapper_copy
    return full_mapper