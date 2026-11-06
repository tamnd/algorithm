# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/julian-day-number/. The authors are listed in prov/EDDN3S.jsonl.

"""Julian day numbers for dates of the proleptic Gregorian and Julian calendars.

Years use astronomical numbering: 1 BC is year 0, 2 BC is year -1, and so on.
Months run from 1 (January) to 12 (December). Every year, month and day number
is a Python integer of any size; the operator // is floor division, so the
formulas hold for negative values as well. Each function makes a fixed number
of integer operations.
"""


def jdn_from_gregorian(year: int, month: int, day: int) -> int:
    """Julian day number of a date in the proleptic Gregorian calendar."""
    a = (14 - month) // 12  # @line L1
    y = year + 4800 - a  # @line L2
    m = month + 12 * a - 3  # @line L3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045  # @line L4


def gregorian_from_jdn(jdn: int) -> tuple[int, int, int]:
    """The proleptic Gregorian date (year, month, day) of a Julian day number."""
    a = jdn + 32044  # @line L5
    b = (4 * a + 3) // 146097  # @line L6
    c = a - (146097 * b) // 4  # @line L7
    d = (4 * c + 3) // 1461  # @line L8
    e = c - (1461 * d) // 4  # @line L9
    m = (5 * e + 2) // 153  # @line L10
    day = e - (153 * m + 2) // 5 + 1  # @line L11
    month = m + 3 - 12 * (m // 10)  # @line L12
    year = 100 * b + d - 4800 + m // 10  # @line L13
    return year, month, day  # @line L14


def jdn_from_julian(year: int, month: int, day: int) -> int:
    """Julian day number of a date in the proleptic Julian calendar."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083


def julian_from_jdn(jdn: int) -> tuple[int, int, int]:
    """The proleptic Julian calendar date (year, month, day) of a Julian day number."""
    c = jdn + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + m // 10
    return year, month, day


def weekday(jdn: int) -> int:
    """Day of the week of a Julian day number: 0 is Sunday, ..., 6 is Saturday."""
    return (jdn + 1) % 7
