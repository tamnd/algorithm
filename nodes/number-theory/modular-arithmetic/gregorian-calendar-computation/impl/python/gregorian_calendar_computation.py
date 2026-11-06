# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gregorian-calendar-computation/. The authors are listed in prov/3NM0VD.jsonl.

"""Conversions between proleptic Gregorian dates and fixed day numbers (R.D.).

R.D. 1 is 1 January of year 1, a Monday, so R.D. numbers agree with
datetime.date.toordinal for the years 1 to 9999. Years use astronomical
numbering (1 BC is year 0) and may be any Python integer; // and % are the
floor division and the matching non-negative remainder, so the code is valid
for negative years and day numbers. Each function makes a fixed number of
integer operations.
"""


def gregorian_leap_year(year: int) -> bool:
    """True if year is a leap year of the Gregorian calendar."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)  # @line L1


def fixed_from_gregorian(year: int, month: int, day: int) -> int:
    """The fixed day number (R.D.) of a valid proleptic Gregorian date."""
    if month <= 2:  # @line L2
        correction = 0
    elif gregorian_leap_year(year):
        correction = -1
    else:
        correction = -2
    y = year - 1  # @line L3
    return 365 * y + y // 4 - y // 100 + y // 400 + (367 * month - 362) // 12 + correction + day


def gregorian_year_from_fixed(rd: int) -> int:
    """The Gregorian year that contains the day with fixed number rd."""
    d0 = rd - 1  # @line L4
    n400, d1 = divmod(d0, 146097)  # @line L5
    n100, d2 = divmod(d1, 36524)  # @line L6
    n4, d3 = divmod(d2, 1461)  # @line L7
    n1 = d3 // 365  # @line L8
    year = 400 * n400 + 100 * n100 + 4 * n4 + n1  # @line L9
    if n100 != 4 and n1 != 4:  # @line L10
        year += 1
    return year


def gregorian_from_fixed(rd: int) -> tuple[int, int, int]:
    """The proleptic Gregorian date (year, month, day) of the fixed day number rd."""
    year = gregorian_year_from_fixed(rd)
    prior_days = rd - fixed_from_gregorian(year, 1, 1)  # @line L11
    if rd < fixed_from_gregorian(year, 3, 1):  # @line L12
        correction = 0
    elif gregorian_leap_year(year):
        correction = 1
    else:
        correction = 2
    month = (12 * (prior_days + correction) + 373) // 367  # @line L13
    day = rd - fixed_from_gregorian(year, month, 1) + 1  # @line L14
    return year, month, day


def day_of_week(rd: int) -> int:
    """Day of the week of a fixed day number: 0 is Sunday, 1 is Monday, ..., 6 is Saturday."""
    return rd % 7  # @line L15
