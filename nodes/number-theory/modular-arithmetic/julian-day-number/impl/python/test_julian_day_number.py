# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/julian-day-number/. The authors are listed in prov/EDDN3S.jsonl.

import datetime
import random

from julian_day_number import (
    gregorian_from_jdn,
    jdn_from_gregorian,
    jdn_from_julian,
    julian_from_jdn,
    weekday,
)

MONTH_LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def gregorian_leap(y: int) -> bool:
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def julian_leap(y: int) -> bool:
    return y % 4 == 0


def month_length(y: int, m: int, leap) -> int:
    if m == 2 and leap(y):
        return 29
    return MONTH_LENGTHS[m - 1]


def naive_jdn(y: int, m: int, d: int, leap, anchor_jdn: int) -> int:
    """Count days one year and one month at a time from 1 January 2000 of the calendar."""
    days = 0
    if y >= 2000:
        for yy in range(2000, y):
            days += 366 if leap(yy) else 365
    else:
        for yy in range(y, 2000):
            days -= 366 if leap(yy) else 365
    for mm in range(1, m):
        days += month_length(y, mm, leap)
    return anchor_jdn + days + d - 1


def naive_gregorian(y: int, m: int, d: int) -> int:
    return naive_jdn(y, m, d, gregorian_leap, 2451545)


def naive_julian(y: int, m: int, d: int) -> int:
    # 1 January 2000 in the Julian calendar is 14 January 2000 in the Gregorian calendar.
    return naive_jdn(y, m, d, julian_leap, 2451545 + 13)


def next_day(y: int, m: int, d: int, leap) -> tuple[int, int, int]:
    if d < month_length(y, m, leap):
        return y, m, d + 1
    if m < 12:
        return y, m + 1, 1
    return y + 1, 1, 1


def random_date(rng: random.Random, lo: int, hi: int, leap) -> tuple[int, int, int]:
    y = rng.randint(lo, hi)
    m = rng.randint(1, 12)
    d = rng.randint(1, month_length(y, m, leap))
    return y, m, d


def test_examples() -> None:
    assert jdn_from_gregorian(2000, 1, 1) == 2451545
    assert gregorian_from_jdn(2451545) == (2000, 1, 1)
    assert jdn_from_gregorian(-4713, 11, 24) == 0
    assert jdn_from_julian(-4712, 1, 1) == 0
    assert gregorian_from_jdn(0) == (-4713, 11, 24)
    assert julian_from_jdn(0) == (-4712, 1, 1)
    assert jdn_from_julian(1582, 10, 4) == 2299160
    assert jdn_from_gregorian(1582, 10, 15) == 2299161
    assert jdn_from_gregorian(1970, 1, 1) == 2440588
    assert jdn_from_gregorian(1858, 11, 17) == 2400001
    assert jdn_from_gregorian(-4800, 3, 1) == -32044
    assert weekday(2451545) == 6
    assert weekday(2299160) == 4 and weekday(2299161) == 5
    assert weekday(jdn_from_gregorian(1969, 7, 20)) == 0


def test_edges() -> None:
    assert jdn_from_gregorian(2000, 3, 1) - jdn_from_gregorian(2000, 2, 28) == 2
    assert jdn_from_gregorian(1900, 3, 1) - jdn_from_gregorian(1900, 2, 28) == 1
    assert jdn_from_gregorian(2100, 3, 1) - jdn_from_gregorian(2100, 2, 28) == 1
    assert jdn_from_gregorian(0, 3, 1) - jdn_from_gregorian(0, 2, 28) == 2
    assert jdn_from_gregorian(-100, 3, 1) - jdn_from_gregorian(-100, 2, 28) == 1
    assert jdn_from_gregorian(-400, 3, 1) - jdn_from_gregorian(-400, 2, 28) == 2
    assert jdn_from_julian(1900, 3, 1) - jdn_from_julian(1900, 2, 28) == 2
    assert jdn_from_gregorian(2001, 1, 1) - jdn_from_gregorian(2000, 12, 31) == 1
    for j in (-1, 0, 1, -32045, -32044, -32043, 10**6, -(10**6)):
        assert jdn_from_gregorian(*gregorian_from_jdn(j)) == j
        assert jdn_from_julian(*julian_from_jdn(j)) == j
    for y, m, d in ((2000, 2, 29), (1900, 2, 28), (0, 2, 29), (-1, 12, 31), (-4800, 2, 29), (-4801, 1, 1)):
        assert jdn_from_gregorian(y, m, d) == naive_gregorian(y, m, d)
        assert gregorian_from_jdn(jdn_from_gregorian(y, m, d)) == (y, m, d)


def test_random_against_naive_count() -> None:
    rng = random.Random(20261106)
    for _ in range(1500):
        y, m, d = random_date(rng, -7000, 7000, gregorian_leap)
        j = naive_gregorian(y, m, d)
        assert jdn_from_gregorian(y, m, d) == j
        assert gregorian_from_jdn(j) == (y, m, d)
        y, m, d = random_date(rng, -7000, 7000, julian_leap)
        j = naive_julian(y, m, d)
        assert jdn_from_julian(y, m, d) == j
        assert julian_from_jdn(j) == (y, m, d)


def test_random_against_datetime() -> None:
    rng = random.Random(7)
    offset = 1721425  # date(1, 1, 1).toordinal() == 1 and its Julian day number is 1721426
    for _ in range(3000):
        y, m, d = random_date(rng, 1, 9999, gregorian_leap)
        date = datetime.date(y, m, d)
        j = jdn_from_gregorian(y, m, d)
        assert j == date.toordinal() + offset
        assert weekday(j) == (date.weekday() + 1) % 7


def test_consecutive_days() -> None:
    rng = random.Random(11)
    for start in [-40000, -32050, -1, 2299150, 2451500] + [rng.randint(-(10**7), 10**7) for _ in range(20)]:
        date = gregorian_from_jdn(start)
        jdate = julian_from_jdn(start)
        for j in range(start, start + 800):
            assert gregorian_from_jdn(j) == date
            assert julian_from_jdn(j) == jdate
            assert jdn_from_gregorian(*date) == j
            date = next_day(*date, gregorian_leap)
            jdate = next_day(*jdate, julian_leap)


def test_huge_years() -> None:
    rng = random.Random(3)
    for _ in range(500):
        k = rng.randint(-(10**300), 10**300)
        y, m, d = random_date(rng, -800, 800, gregorian_leap)
        base = naive_gregorian(y, m, d)
        j = jdn_from_gregorian(y + 400 * k, m, d)
        assert j == base + 146097 * k
        assert gregorian_from_jdn(j) == (y + 400 * k, m, d)
        y, m, d = random_date(rng, -800, 800, julian_leap)
        base = naive_julian(y, m, d)
        j = jdn_from_julian(y + 4 * k, m, d)
        assert j == base + 1461 * k
        assert julian_from_jdn(j) == (y + 4 * k, m, d)
        big = rng.randint(-(10**400), 10**400)
        assert jdn_from_gregorian(*gregorian_from_jdn(big)) == big
        assert jdn_from_julian(*julian_from_jdn(big)) == big
