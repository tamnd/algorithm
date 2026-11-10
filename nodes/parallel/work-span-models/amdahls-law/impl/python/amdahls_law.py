# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amdahls-law/. The authors are listed in prov/W8TH5A.jsonl.

"""Amdahl's law with exact rational arithmetic.

f is the parallel fraction: the part of the one-processor running time that
can be split evenly among p processors. The rest, 1 - f, runs on one
processor. Pass Fraction or int values to get exact results.
"""

from fractions import Fraction
from typing import Union

Num = Union[int, Fraction]


def _check(f: Num, p: int) -> None:
    if not 0 <= f <= 1:
        raise ValueError("f must be in [0, 1]")
    if p < 1:
        raise ValueError("p must be at least 1")


def amdahl_time(f: Num, p: int, t1: Num = 1) -> Fraction:
    """The time on p processors: (1 - f) t1 + f t1 / p."""
    _check(f, p)
    return (1 - Fraction(f)) * t1 + Fraction(f) * t1 / p


def amdahl_speedup(f: Num, p: int) -> Fraction:
    """The speedup bound 1 / ((1 - f) + f / p)."""
    return 1 / amdahl_time(f, p)


def amdahl_limit(f: Num) -> Fraction | None:
    """The limit 1 / (1 - f) as p grows; None (no bound) when f = 1."""
    _check(f, 1)
    return None if f == 1 else 1 / (1 - Fraction(f))


def amdahl_efficiency(f: Num, p: int) -> Fraction:
    """The parallel efficiency speedup / p."""
    return amdahl_speedup(f, p) / p


def half_limit_processors(f: Num) -> Fraction:
    """The p at which the speedup is half of the limit: p = f / (1 - f), for 0 < f < 1."""
    if not 0 < f < 1:
        raise ValueError("f must be in (0, 1)")
    return Fraction(f) / (1 - Fraction(f))


def karp_flatt(speedup: Num, p: int) -> Fraction:
    """The serial fraction e = (1/speedup - 1/p) / (1 - 1/p) for a measured speedup, p >= 2."""
    if p < 2:
        raise ValueError("p must be at least 2")
    return (1 / Fraction(speedup) - Fraction(1, p)) / (1 - Fraction(1, p))


def serial_then_parallel_greedy_time(a: int, b: int, p: int) -> int:
    """Steps of a greedy schedule of a chain of a unit nodes followed by b independent unit nodes."""
    return a + -(-b // p)
