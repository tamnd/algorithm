# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nuts-and-bolts/. The authors are listed in prov/SA6TXV.jsonl.

"""Randomized matching of nuts and bolts with nut-bolt comparisons only.

The nuts and the bolts are two lists of the same n distinct sizes, in any
order. The algorithm never compares two nuts or two bolts. It works like
randomized quicksort, with an explicit stack instead of recursion, and it
leaves both lists sorted, so nuts[i] matches bolts[i] at the end.
"""

import math
from fractions import Fraction
from typing import Protocol


class Chooser(Protocol):
    def randrange(self, stop: int) -> int: ...


class Counter:
    """A nut-bolt comparison that counts its calls and records the pairs it compares."""

    def __init__(self) -> None:
        self.count = 0
        self.pairs: list[tuple[int, int]] = []

    def __call__(self, nut: int, bolt: int) -> int:
        self.count += 1
        self.pairs.append((nut, bolt))
        return (nut > bolt) - (nut < bolt)


def match(nuts: list[int], bolts: list[int], rng: Chooser, cmp: Counter | None = None) -> int:
    """Sort nuts and bolts in place so that nuts[i] fits bolts[i]; return the number of comparisons."""
    if cmp is None:
        cmp = Counter()
    stack = [(0, len(nuts))]  # @line L1
    while stack:  # @line L2
        lo, hi = stack.pop()  # @line L3
        if hi <= lo:  # @line L4
            continue
        b = bolts[lo + rng.randrange(hi - lo)]  # @line L5
        # Split the nuts around b: hi - lo comparisons.
        small, big, x = [], [], None
        for nut in nuts[lo:hi]:
            c = cmp(nut, b)  # @line L6
            if c < 0:
                small.append(nut)
            elif c > 0:
                big.append(nut)
            else:
                x = nut
        assert x is not None, "no nut fits the bolt"
        q = lo + len(small)
        nuts[lo:hi] = small + [x] + big
        # Split the other bolts around the matching nut x: hi - lo - 1 comparisons.
        small_b, big_b = [], []
        for bolt in bolts[lo:hi]:
            if bolt is b:
                continue
            if cmp(x, bolt) > 0:  # @line L7
                small_b.append(bolt)
            else:
                big_b.append(bolt)
        bolts[lo:hi] = small_b + [b] + big_b  # @line L8
        stack.append((q + 1, hi))  # @line L9
        stack.append((lo, q))
    return cmp.count


def expected_comparisons(n: int) -> Fraction:
    """The exact expected number of comparisons, from the recurrence."""
    c = [Fraction(0)] * (n + 1)
    for m in range(1, n + 1):
        c[m] = (2 * m - 1) + Fraction(2, m) * sum(c[k] for k in range(m))
    return c[n]


def closed_form(n: int) -> Fraction:
    """4 (n + 1) H_n - 7 n."""
    h = sum(Fraction(1, i) for i in range(1, n + 1))
    return 4 * (n + 1) * h - 7 * n


def lower_bound(n: int) -> float:
    """log_3(n!), the decision-tree lower bound on the number of comparisons."""
    return math.lgamma(n + 1) / math.log(3)


class Script:
    """A chooser that replays a list of choices; it is used to enumerate all runs exactly."""

    def __init__(self, choices: list[int]) -> None:
        self.choices = choices
        self.ranges: list[int] = []

    def randrange(self, stop: int) -> int:
        i = len(self.ranges)
        self.ranges.append(stop)
        return self.choices[i] if i < len(self.choices) else 0


def exact_expectation(sizes: list[int], bolts_order: list[int]) -> tuple[Fraction, int, int]:
    """Run the algorithm on every sequence of random choices, weighted by its probability.

    Returns the exact expected number of comparisons, the least and the most.
    """
    total = Fraction(0)
    least, most = 10**9, 0
    choices: list[int] = []
    while True:
        script = Script(choices)
        count = match(list(sizes), list(bolts_order), script)
        weight = Fraction(1)
        for m in script.ranges:
            weight /= m
        total += weight * count
        least, most = min(least, count), max(most, count)
        full = choices + [0] * (len(script.ranges) - len(choices))
        # Advance the choices like an odometer, from the last position.
        i = len(full) - 1
        while i >= 0 and full[i] == script.ranges[i] - 1:
            i -= 1
        if i < 0:
            return total, least, most
        choices = full[:i] + [full[i] + 1]
