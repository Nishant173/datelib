### NOTE - Use setters in Date class, instead of creating new objects multiple times


from __future__ import annotations
from typing import List, Optional, Tuple

from datelib.constants import (
    DayOfWeek,
    MONTH_NUMBER_TO_NAME_MAPPER,
    NUM_MONTHS_IN_YEAR,
)
from datelib.day_of_week import get_day_of_week
from datelib.errors import InvalidDateError
from datelib.utils import (
    get_days_count_between_months,
    get_days_count_in_year,
    get_days_per_month_mapper,
    get_days_per_month_mapper_for_multiple_years,
    get_days_remaining_in_month,
    get_two_digit_0_padding,
    get_type_name,
    is_leap_year,
)


class Date:
    """
    Class for working with dates.

    Methods:
        - as_string()
        - as_string_prettified()
        - copy()
        - is_weekend()
        - is_weekday()
        - is_last_day_of_month()
        - is_last_day_of_year()
        - is_first_day_of_month()
        - is_first_day_of_year()
        - difference()
        - abs_difference()
        - add()
        - subtract()

    Properties (getter):
        - year
        - month
        - day
        - days_since_start_of_year
        - days_till_end_of_year
        - day_of_week

    Properties (setter):
        - year
        - month
        - day
    """
    def __init__(self, *, year: int, month: int, day: int) -> None:
        self._year = year
        self._month = month
        self._day = day
        Date._validate_date(self)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(year={self.year}, month={self.month}, day={self.day})"

    def __eq__(self, other: Date) -> bool:
        return self.year == other.year and self.month == other.month and self.day == other.day

    def __ne__(self, other: Date) -> bool:
        return self.year != other.year or self.month != other.month or self.day != other.day

    def __gt__(self, other: Date) -> bool:
        return any([
            self.year > other.year,
            (
                self.year == other.year and (
                    self.month > other.month or (self.day > other.day)
                )
            ),
        ])

    def __ge__(self, other: Date) -> bool:
        return (self.year >= other.year and self.month >= other.month and self.day >= other.day)

    def __lt__(self, other: Date) -> bool:
        return any([
            self.year < other.year,
            (
                self.year == other.year and (
                    self.month < other.month or (self.day < other.day)
                )
            ),
        ])

    def __le__(self, other: Date) -> bool:
        return (self.year <= other.year and self.month <= other.month and self.day <= other.day)

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month

    @property
    def day(self) -> int:
        return self._day

    @year.setter
    def year(self, year: int) -> None:
        self._year = year
        Date._validate_date(self)

    @month.setter
    def month(self, month: int) -> None:
        self._month = month
        Date._validate_date(self)

    @day.setter
    def day(self, day: int) -> None:
        self._day = day
        Date._validate_date(self)

    def as_string(self) -> str:
        """Returns date-string of format 'yyyy-mm-dd'"""
        return f"{self.year}-{get_two_digit_0_padding(self.month)}-{get_two_digit_0_padding(self.day)}"

    def as_string_prettified(self) -> str:
        return f"{MONTH_NUMBER_TO_NAME_MAPPER[self.month]} {self._get_day_with_suffix()}, {self.year}"

    def copy(self) -> Date:
        """Returns new copy of object"""
        return Date(year=self.year, month=self.month, day=self.day)

    def _get_day_with_suffix(self) -> str:
        if 4 <= self.day <= 20 or 24 <= self.day <= 30:
            return f"{self.day}th"
        if self.day in [1, 21, 31]:
            return f"{self.day}st"
        if self.day in [2, 22]:
            return f"{self.day}nd"
        if self.day in [3, 23]:
            return f"{self.day}rd"
        raise ValueError(self)

    @staticmethod
    def _validate_date(date_obj: Date, /) -> None:
        """Raises an InvalidDateError if given date object is invalid"""
        # Check types
        if not all([
            isinstance(date_obj.year, int),
            isinstance(date_obj.month, int),
            isinstance(date_obj.day, int),
        ]):
            raise InvalidDateError(
                "Expects (year, month, day) to all be of type int, but got types"
                f" ({get_type_name(date_obj.year)}, {get_type_name(date_obj.month)}, {get_type_name(date_obj.day)}) respectively"
            )

        # Check values
        if date_obj.year <= 0:
            raise InvalidDateError(f"Got an invalid year {date_obj.year}")
        if not (1 <= date_obj.month <= 12):
            raise InvalidDateError(f"Got an invalid month {date_obj.month}. Expects month to be in range 1-12")
        if date_obj.month in [1, 3, 5, 7, 8, 10, 12] and not (1 <= date_obj.day <= 31):
            raise InvalidDateError(
                f"Got an invalid day {date_obj.day}. Expects day to be in range 1-31 (for the given month {date_obj.month})"
            )
        if date_obj.month in [4, 6, 9, 11] and not (1 <= date_obj.day <= 30):
            raise InvalidDateError(
                f"Got an invalid day {date_obj.day}. Expects day to be in range 1-30 (for the given month {date_obj.month})"
            )
        if date_obj.month in [2]:
            _is_leap_year = is_leap_year(date_obj.year)
            if (_is_leap_year and not (1 <= date_obj.day <= 29)) or (not _is_leap_year and not (1 <= date_obj.day <= 28)):
                raise InvalidDateError(
                    f"Got an invalid day {date_obj.day} (for the given month {date_obj.month} and year {date_obj.year})."
                    " Expects day to be in range 1-28 (for non leap year) and in range 1-29 (for leap year)"
                )
        return None

    @property
    def days_since_start_of_year(self) -> int:
        """Days since start of the year (including current date)"""
        if self.month == 1:
            return self.day
        return get_days_count_between_months(year=self.year, start_month=1, end_month=self.month - 1) + self.day

    @property
    def days_till_end_of_year(self) -> int:
        """Days till end of the year (excluding current date)"""
        num_days = 0
        for month_number, num_days_in_month in reversed(get_days_per_month_mapper(year=self.year).items()):
            if month_number == self.month:
                num_days += num_days_in_month - self.day
                break
            num_days += num_days_in_month
        return num_days

    def is_weekend(self) -> bool:
        """Returns True if day of week is one of Saturday|Sunday"""
        return self.day_of_week in [DayOfWeek.SATURDAY, DayOfWeek.SUNDAY]

    def is_weekday(self) -> bool:
        """Returns True if day of week is not on a weekend"""
        return not self.is_weekend()

    def is_last_day_of_month(self) -> bool:
        return self.day == get_days_per_month_mapper(year=self.year)[self.month]

    def is_last_day_of_year(self) -> bool:
        return self.month == 12 and self.day == 31

    def is_first_day_of_month(self) -> bool:
        return self.day == 1

    def is_first_day_of_year(self) -> bool:
        return self.month == 1 and self.day == 1

    def _increment_year_and_month(self, year: int, month: int) -> Tuple[int, int]:
        """Increments year/month combo, and returns tuple of (year, month)"""
        if month == 12:
            year, month = year + 1, 1
        else:
            month += 1
        return (year, month)

    def _decrement_year_and_month(self, year: int, month: int) -> Tuple[int, int]:
        """Decrements year/month combo, and returns tuple of (year, month)"""
        if month == 1:
            year, month = year - 1, 12
        else:
            month -= 1
        return (year, month)

    def _subtract_one_day(self) -> Date:
        if self.is_first_day_of_year():
            return Date(year=self.year - 1, month=12, day=31)
        if self.is_first_day_of_month():
            return Date(
                year=self.year,
                month=self.month - 1,
                day=get_days_per_month_mapper(year=self.year)[self.month - 1],
            )
        return Date(year=self.year, month=self.month, day=self.day - 1)

    def _subtract_days(self, days: int) -> Date:
        assert days >= 0, "Cannot subtract negative number of days"
        current_year, current_month = self.year, self.month
        days_per_month_mapper = get_days_per_month_mapper_for_multiple_years(
            years=list(
                range(self.year - (days // 366) - 1, self.year + 1, 1)
            )
        )
        # Handle current year/month
        total_days_in_month = days_per_month_mapper.get(current_year, {}).get(current_month, None) # needs to be an integer
        if days < self.day:
            return Date(year=self.year, month=self.month, day=self.day - days)
        days -= self.day
        current_year, current_month = self._decrement_year_and_month(year=current_year, month=current_month)
        # Handle previous years/months
        while True:
            total_days_in_month = days_per_month_mapper.get(current_year, {}).get(current_month, None) # needs to be an integer
            if days == 0:
                return Date(year=current_year, month=current_month, day=total_days_in_month)
            if days > total_days_in_month:
                days -= total_days_in_month
                current_year, current_month = self._decrement_year_and_month(year=current_year, month=current_month)
            elif days < total_days_in_month:
                break
        return Date(year=current_year, month=current_month, day=total_days_in_month - days)

    def _subtract_months(self, months: int) -> Date:
        assert months >= 0, "Cannot subtract negative number of months"
        years, months = divmod(months, NUM_MONTHS_IN_YEAR)
        date_new = self._subtract_years(years=years)
        month = date_new.month - months
        year = date_new.year
        if month <= 0:
            _mapper = {
                0: 12,
                -1: 11,
                -2: 10,
                -3: 9,
                -4: 8,
                -5: 7,
                -6: 6,
                -7: 5,
                -8: 4,
                -9: 3,
                -10: 2,
                -11: 1,
            }
            month = _mapper[month]
            year = date_new.year - 1
        return Date(year=year, month=month, day=date_new.day)

    def _subtract_years(self, years: int) -> Date:
        assert years >= 0, "Cannot subtract negative number of years"
        if self.month == 2 and self.day == 29:
            if is_leap_year(self.year - years):
                month, day = 2, 29
            else:
                month, day = 2, 28
        else:
            month, day = self.month, self.day
        return Date(year=self.year - years, month=month, day=day)

    def _add_days(self, days: int) -> Date:
        assert days >= 0, "Cannot add negative number of days"
        current_year, current_month = self.year, self.month
        days_per_month_mapper = get_days_per_month_mapper_for_multiple_years(
            years=list(
                range(self.year, self.year + (days // 366) + 2, 1)
            )
        )
        # Handle current year/month
        total_days_in_month = days_per_month_mapper.get(current_year, {}).get(current_month, None) # needs to be an integer
        days_remaining_in_month = total_days_in_month - self.day
        if days <= days_remaining_in_month:
            return Date(year=self.year, month=self.month, day=self.day + days)
        days -= days_remaining_in_month
        current_year, current_month = self._increment_year_and_month(year=current_year, month=current_month)
        # Handle subsequent years/months
        while True:
            total_days_in_month = days_per_month_mapper.get(current_year, {}).get(current_month, None) # needs to be an integer
            if days > total_days_in_month:
                days -= total_days_in_month
                current_year, current_month = self._increment_year_and_month(year=current_year, month=current_month)
            elif days <= total_days_in_month:
                break
        return Date(year=current_year, month=current_month, day=days)

    def _add_months(self, months: int) -> Date:
        assert months >= 0, "Cannot add negative number of months"
        years, months = divmod(months, NUM_MONTHS_IN_YEAR)
        date_new = self._add_years(years=years)
        month = (date_new.month + months) % NUM_MONTHS_IN_YEAR
        month = NUM_MONTHS_IN_YEAR if month == 0 else month
        year = date_new.year + 1 if date_new.month + months > NUM_MONTHS_IN_YEAR else date_new.year
        return Date(year=year, month=month, day=date_new.day)

    def _add_years(self, years: int) -> Date:
        assert years >= 0, "Cannot add negative number of years"
        if self.month == 2 and self.day == 29:
            if is_leap_year(self.year + years):
                month, day = 2, 29
            else:
                month, day = 3, 1
        else:
            month, day = self.month, self.day
        return Date(year=self.year + years, month=month, day=day)

    def _difference_between_dates_in_same_year(self, *, small: Date, big: Date) -> int:
        """Returns the absolute date difference (in days)"""
        assert small < big, "The `small` date needs to be < the `big` date"
        assert small.year == big.year, "The year of both `small` and `big` need to be the same"
        days_difference_abs = 0
        if small.month == big.month:
            days_difference_abs += big.day - small.day
        elif small.month + 1 == big.month:
            days_difference_abs += get_days_remaining_in_month(year=self.year, month=small.month, day=small.day)
            days_difference_abs += big.day
        else:
            days_difference_abs += get_days_remaining_in_month(year=self.year, month=small.month, day=small.day)
            days_difference_abs += get_days_count_between_months(year=self.year, start_month=small.month + 1, end_month=big.month - 1)
            days_difference_abs += big.day
        return days_difference_abs

    def _difference_between_dates_in_different_years(self, *, small: Date, big: Date) -> int:
        """Returns the absolute date difference (in days)"""
        assert small < big, "The `small` date needs to be < the `big` date"
        assert small.year != big.year, "The years of `small` and `big` need to be different"
        days_difference_abs = 0
        _, *years_in_between, _ = self._get_years_between_dates(small=small, big=big)
        days_difference_abs += small.days_till_end_of_year
        days_difference_abs += sum(get_days_count_in_year(year) for year in years_in_between) if years_in_between else 0
        days_difference_abs += big.days_since_start_of_year
        return days_difference_abs

    def _get_years_between_dates(self, *, small: Date, big: Date) -> List[int]:
        assert small < big, "The `small` date needs to be < the `big` date"
        if small.year == big.year:
            return [small.year]
        years = [small.year]
        while True:
            last_year = years[-1]
            if last_year + 1 <= big.year:
                years.append(last_year + 1)
            else:
                break
        return years

    def difference(self, other: Date) -> int:
        """
        Returns the date difference (in days).
        If self > other, difference will be positive.
        If self < other, difference will be negative.
        If self == other, difference will be 0.
        """
        if self == other:
            return 0
        if self < other:
            small, big = self.copy(), other.copy()
        else:
            small, big = other.copy(), self.copy()
        if small.year == big.year:
            days_difference_abs = self._difference_between_dates_in_same_year(small=small, big=big)
        else:
            days_difference_abs = self._difference_between_dates_in_different_years(small=small, big=big)
        return days_difference_abs * -1 if self < other else days_difference_abs

    def abs_difference(self, other: Date) -> int:
        """Returns the absolute date difference (in days)"""
        return abs(self.difference(other=other))

    def add(
            self,
            *,
            years: Optional[int] = 0,
            months: Optional[int] = 0,
            days: Optional[int] = 0,
        ) -> Date:
        return self._add_years(years=years)._add_months(months=months)._add_days(days=days)

    def subtract(
            self,
            *,
            years: Optional[int] = 0,
            months: Optional[int] = 0,
            days: Optional[int] = 0,
        ) -> Date:
        return self._subtract_years(years=years)._subtract_months(months=months)._subtract_days(days=days)

    @property
    def day_of_week(self) -> str:
        return get_day_of_week(year=self.year, month=self.month, day=self.day)

