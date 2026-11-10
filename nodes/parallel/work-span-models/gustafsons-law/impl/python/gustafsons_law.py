# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gustafsons-law/. The authors are listed in prov/0Z9QC0.jsonl.

"""Gustafson's law (scaled speedup) and its conversion to Amdahl's law, exactly.

s is the serial fraction of the run on p processors: of the parallel
running time, a part s runs on one processor and a part 1 - s keeps all p
processors busy. Amdahl's law uses instead the parallel fraction f of the
run on one processor. Pass Fraction or int values to get exact results.
"""

from fractions import Fraction
from typing import Union

Num = Union[int, Fraction]


def _check(x: Num, p: int) -> None:
    if not 0 <= x <= 1:
        raise ValueError("the fraction must be in [0, 1]")
    if p < 1:
        raise ValueError("p must be at least 1")


def scaled_speedup(s: Num, p: int) -> Fraction:
    """Gustafson's scaled speedup s + p (1 - s) = p - (p - 1) s."""
    _check(s, p)
    return Fraction(s) + p * (1 - Fraction(s))


def scaled_efficiency(s: Num, p: int) -> Fraction:
    """The efficiency of the scaled run: s / p + (1 - s)."""
    return scaled_speedup(s, p) / p


def amdahl_speedup(f: Num, p: int) -> Fraction:
    """Amdahl's bound 1 / ((1 - f) + f / p) for the parallel fraction f."""
    _check(f, p)
    return 1 / ((1 - Fraction(f)) + Fraction(f) / p)


def to_amdahl_parallel_fraction(s: Num, p: int) -> Fraction:
    """The parallel fraction f of the one-processor run of the same job.

    The one-processor time is s + p (1 - s), and its parallel part is p (1 - s).
    """
    _check(s, p)
    return p * (1 - Fraction(s)) / scaled_speedup(s, p)


def from_amdahl_parallel_fraction(f: Num, p: int) -> Fraction:
    """The serial fraction s of the p-processor run, given the parallel fraction f."""
    _check(f, p)
    serial, parallel = 1 - Fraction(f), Fraction(f) / p
    return serial / (serial + parallel)
