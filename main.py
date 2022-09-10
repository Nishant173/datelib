from datetime import datetime, timedelta
from pprint import pprint

from datelib.dates import Date
from datelib.decorators import repeat, timer
from datelib.utils import (
    get_days_count_between_months,
    get_days_in_month,
    get_days_per_month_mapper_for_multiple_years,
    get_days_remaining_in_month,
)



DATE_INPUT = {
    "year": 1898,
    "month": 3,
    "day": 7,
}
NUM_DAYS = 25
NUM_RUNS = 10_000


@timer("StdLib")
@repeat(num_times=NUM_RUNS)
def func_a():
    # dt = datetime(**DATE_INPUT)
    # dt += timedelta(days=NUM_DAYS)
    # return dt
    return datetime(1890, 6, 28) - datetime(1717, 4, 13)


@timer("CustomFunc")
@repeat(num_times=NUM_RUNS)
def func_b():
    # date = Date(**DATE_INPUT)
    # date = date.add(days=NUM_DAYS)
    # return date
    return Date(year=1890, month=6, day=28).difference(
        other=Date(year=1717, month=4, day=13)
    )


# @timer("Hello")
# @repeat(num_times=NUM_RUNS)
# def func_c():
#     date = Date(**DATE_INPUT)
#     return date.days_till_end_of_year


# print(
# #     # f"{dt} (StdLib)",
# #     # f"{date.as_string_prettified()} (Custom)",
# #     # f"{date.days_since_start_of_year}",
# #     # f"{date.days_till_end_of_year}",
#     func_a(),
#     func_b(),
#     # datetime(1890, 6, 28) - datetime(1717, 4, 13),
#     # Date(year=1890, month=6, day=28).difference(
#     #     other=Date(year=1717, month=4, day=13)
#     # ),
#     sep="\n",
# )


# m = get_days_per_month_mapper_for_multiple_years(years=list(range(1999, 2022+1, 1)))
# pprint(m)


# print(
#     get_days_count_between_months(year=2012, start_month=2, end_month=2),
#     get_days_in_month(year=2019, month=3),
#     get_days_remaining_in_month(year=2019, month=3, day=31),
#     func_a(),
#     func_b(),
#     sep="\n",
# )

print(
    Date(year=2014, month=8, day=1).difference(
        Date(year=2018, month=6, day=11)
    ),
    Date(year=2014, month=1, day=1).add(days=360),
    sep="\n",
)