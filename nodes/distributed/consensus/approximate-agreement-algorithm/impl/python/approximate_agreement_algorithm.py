# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-agreement-algorithm/. The authors are listed in prov/11RC2B.jsonl.

"""Synchronous Byzantine approximate agreement by the trimmed midpoint.

n processes, at most t of them Byzantine, n > 3t. In each round every process
sends its value to all, drops the t smallest and t largest of the n values it
received and moves to the midpoint of the rest. The spread of the correct
values halves in each round, and the values stay inside the range of the
correct inputs. All arithmetic uses fractions, so the tests check the bounds
exactly.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable, Optional

# A Byzantine strategy: (round, sender, receiver, current correct values) -> value or None (silent)
Strategy = Callable[[int, int, int, dict[int, Fraction]], Optional[Fraction]]


def rounds_needed(delta: Fraction, eps: Fraction) -> int:
    """The smallest R with delta / 2**R <= eps, that is ceil(log2(delta / eps)) for delta > eps."""
    r = 0
    while delta / (2 ** r) > eps:
        r += 1
    return r


def trimmed_midpoint(received: list[Fraction], t: int) -> Fraction:
    vals = sorted(received)[t: len(received) - t]  # @line L4
    return (vals[0] + vals[-1]) / 2  # @line L5


def run(inputs: dict[int, Fraction], n: int, t: int, rounds: int,
        byz: Optional[Strategy] = None) -> list[dict[int, Fraction]]:
    """inputs holds the correct processes; ids outside it are Byzantine. Returns the values after each round."""
    x = dict(inputs)  # @line L1
    history = [dict(x)]
    for r in range(1, rounds + 1):  # @line L2
        new = {}
        for p in x:
            got = []
            for q in range(n):
                v = x[q] if q in x else (byz(r, q, p, x) if byz else None)
                got.append(x[p] if v is None else Fraction(v))  # @line L3
            new[p] = trimmed_midpoint(got, t)
        x = new
        history.append(dict(x))
    return history  # @line L6


def spread(vals: dict[int, Fraction]) -> Fraction:
    return max(vals.values()) - min(vals.values())


# Byzantine strategies used by the tests


def split_attack(r: int, q: int, p: int, x: dict[int, Fraction]) -> Fraction:
    """Send a very low value to processes below the middle and a very high one to the others."""
    lo, hi = min(x.values()), max(x.values())
    return lo - 1000 if x[p] <= (lo + hi) / 2 else hi + 1000


def random_attack(seed: int) -> Strategy:
    rng = random.Random(seed)

    def strat(r: int, q: int, p: int, x: dict[int, Fraction]) -> Optional[Fraction]:
        lo, hi = min(x.values()), max(x.values())
        c = rng.random()
        if c < 0.15:
            return None
        if c < 0.4:
            return lo - rng.randint(0, 50)
        if c < 0.65:
            return hi + rng.randint(0, 50)
        return lo + (hi - lo) * Fraction(rng.randint(0, 8), 8)

    return strat
