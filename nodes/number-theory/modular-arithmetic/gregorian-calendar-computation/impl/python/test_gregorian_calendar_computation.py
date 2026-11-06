# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gregorian-calendar-computation/. The authors are listed in prov/3NM0VD.jsonl.

import datetime
import random

from gregorian_calendar_computation import (
    day_of_week,
    fixed_from_gregorian,
    gregorian_from_fixed,
    gregorian_leap_year,
    gregorian_year_from_fixed,
)

MONTH_LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def naive_leap(y: int) -> bool:
    if y % 400 == 0:
        return True
    if y % 100 == 0:
        return False
    return y % 4 == 0


def month_length(y: int, m: int) -> int:
    return 29 if m == 2 and naive_leap(y) else MONTH_LENGTHS[m - 1]


def naive_fixed(y: int, m: int, d: int) -> int:
    """Count days one year and one month at a time from R.D. 1 = 1 January of year 1."""
    days = 0
    if y >= 1:
        for yy in range(1, y):
            days += 366 if naive_leap(yy) else 365
    else:
        for yy in range(y, 1):
            days -= 366 if naive_leap(yy) else 365
    for mm in range(1, m):
        days += month_length(y, mm)
    return days + d


def next_day(y: int, m: int, d: int) -> tuple[int, int, int]:
    if d < month_length(y, m):
        return y, m, d + 1
    if m < 12:
        return y, m + 1, 1
    return y + 1, 1, 1


def random_date(rng: random.Random, lo: int, hi: int) -> tuple[int, int, int]:
    y = rng.randint(lo, hi)
    m = rng.randint(1, 12)
    return y, m, rng.randint(1, month_length(y, m))


def test_examples() -> None:
    assert fixed_from_gregorian(1, 1, 1) == 1
    assert fixed_from_gregorian(0, 12, 31) == 0
    assert fixed_from_gregorian(2000, 1, 1) == 730120
    assert fixed_from_gregorian(2000, 12, 31) == 730485
    assert gregorian_from_fixed(730485) == (2000, 12, 31)
    assert fixed_from_gregorian(2026, 11, 6) == 739926
    assert gregorian_from_fixed(739926) == (2026, 11, 6)
    assert day_of_week(739926) == 5
    assert day_of_week(1) == 1
    assert fixed_from_gregorian(1970, 1, 1) == 719163
    assert day_of_week(fixed_from_gregorian(1582, 10, 15)) == 5


def test_leap_years() -> None:
    for y in range(-2000, 3000):
        assert gregorian_leap_year(y) == naive_leap(y)
    assert gregorian_leap_year(2000) and gregorian_leap_year(2024) and gregorian_leap_year(0)
    assert not gregorian_leap_year(1900) and not gregorian_leap_year(2100) and not gregorian_leap_year(2023)
    assert gregorian_leap_year(-4) and not gregorian_leap_year(-100) and gregorian_leap_year(-400)


def test_cycle_boundaries() -> None:
    for y in (-801, -800, -401, -400, -101, -100, -1, 0, 1, 99, 100, 101, 399, 400, 401, 1600, 1900, 2000, 2100):
        for m, d in ((1, 1), (2, 28), (3, 1), (12, 31)):
            r = fixed_from_gregorian(y, m, d)
            assert r == naive_fixed(y, m, d)
            assert gregorian_from_fixed(r) == (y, m, d)
            assert gregorian_year_from_fixed(r) == y
        if naive_leap(y):
            r = fixed_from_gregorian(y, 2, 29)
            assert r == naive_fixed(y, 2, 29)
            assert gregorian_from_fixed(r) == (y, 2, 29)


def test_random_against_naive_count() -> None:
    rng = random.Random(2026)
    for _ in range(1500):
        y, m, d = random_date(rng, -6000, 6000)
        r = naive_fixed(y, m, d)
        assert fixed_from_gregorian(y, m, d) == r
        assert gregorian_from_fixed(r) == (y, m, d)


def test_random_against_datetime() -> None:
    rng = random.Random(5)
    for _ in range(3000):
        y, m, d = random_date(rng, 1, 9999)
        date = datetime.date(y, m, d)
        r = fixed_from_gregorian(y, m, d)
        assert r == date.toordinal()
        assert gregorian_from_fixed(r) == (y, m, d)
        assert day_of_week(r) == (date.weekday() + 1) % 7
    for r in [1, 2, 3652059] + [rng.randint(1, 3652059) for _ in range(2000)]:
        date = datetime.date.fromordinal(r)
        assert gregorian_from_fixed(r) == (date.year, date.month, date.day)


def test_consecutive_days() -> None:
    rng = random.Random(9)
    for start in [-146100, -36530, -1500, -5, 730000] + [rng.randint(-(10**8), 10**8) for _ in range(20)]:
        date = gregorian_from_fixed(start)
        for r in range(start, start + 1000):
            assert gregorian_from_fixed(r) == date
            assert fixed_from_gregorian(*date) == r
            date = next_day(*date)


def test_huge_years() -> None:
    rng = random.Random(1)
    for _ in range(500):
        k = rng.randint(-(10**300), 10**300)
        y, m, d = random_date(rng, -800, 800)
        r = fixed_from_gregorian(y + 400 * k, m, d)
        assert r == naive_fixed(y, m, d) + 146097 * k
        assert gregorian_from_fixed(r) == (y + 400 * k, m, d)
        assert day_of_week(r) == day_of_week(naive_fixed(y, m, d))
        big = rng.randint(-(10**450), 10**450)
        assert fixed_from_gregorian(*gregorian_from_fixed(big)) == big
