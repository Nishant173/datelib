class DayOfWeek:
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class MonthOfYear:
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"


# Do not change the constants
DAY_NUMBER_TO_NAME_MAPPER = {
    1: DayOfWeek.MONDAY,
    2: DayOfWeek.TUESDAY,
    3: DayOfWeek.WEDNESDAY,
    4: DayOfWeek.THURSDAY,
    5: DayOfWeek.FRIDAY,
    6: DayOfWeek.SATURDAY,
    7: DayOfWeek.SUNDAY,
}
MONTH_NUMBER_TO_NAME_MAPPER = {
    1: MonthOfYear.JANUARY,
    2: MonthOfYear.FEBRUARY,
    3: MonthOfYear.MARCH,
    4: MonthOfYear.APRIL,
    5: MonthOfYear.MAY,
    6: MonthOfYear.JUNE,
    7: MonthOfYear.JULY,
    8: MonthOfYear.AUGUST,
    9: MonthOfYear.SEPTEMBER,
    10: MonthOfYear.OCTOBER,
    11: MonthOfYear.NOVEMBER,
    12: MonthOfYear.DECEMBER,
}
NUM_DAYS_IN_WEEK = 7
NUM_MONTHS_IN_YEAR = 12
NUM_DAYS_IN_NON_LEAP_YEAR = 365
NUM_DAYS_IN_LEAP_YEAR = 366
DAY_COUNTS_IN_NON_LEAP_YEAR_BY_MONTH = [
    31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, # must be in order of months 1-12
]
DAY_COUNTS_IN_LEAP_YEAR_BY_MONTH = [
    31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, # must be in order of months 1-12
]
YEARS_HAVING_JANUARY_1ST_AS_SATURDAY = [
    28,
    248,
    524,
    744,
    980,
    1228,
    1448,
    1684,
    1916,
    2000,
    2084,
    2276,
    2400,
    2676,
    2952,
] # Years in A.D. that have January 1st falling on Saturday (as points of reference) - Must also be leap years