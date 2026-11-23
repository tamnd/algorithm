# SPDX-License-Identifier: MIT
# Shared helper of the security and privacy pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Checkers for differential privacy on small finite examples.

A dataset is a tuple of records from a finite universe. A pmf is a dict from
outputs to probabilities; the probabilities may be fractions.Fraction (exact)
or float. A mechanism pmf is a function from a dataset to the pmf of the
output of the mechanism on that dataset.

This module holds the neighbor relations, the privacy loss, the hockey-stick
and Renyi divergences, the pure and approximate DP checks over a list of
neighbor pairs, an empirical pmf, the Hoeffding margin for Monte Carlo
checks, and a grid check of a log density ratio. It holds no mechanism, no
noise sampler and no accountant: those belong to the pages that define them.

Natural logarithms are used throughout, as in the DP literature.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Callable, Hashable, Iterable, Mapping, Sequence, Union

Number = Union[int, float, Fraction]
Pmf = Mapping[Hashable, Number]
Dataset = tuple
Pair = tuple[Dataset, Dataset]


def neighbors_add_remove(dataset: Sequence[Hashable], universe: Iterable[Hashable]) -> list[Dataset]:
    """All datasets at add/remove distance 1 from dataset.

    A neighbor removes one record, or appends one record from the universe.
    Datasets are treated as multisets: a removal keeps the order of the other
    records, and equal results are listed once. Cost: O(n (n + |universe|)).
    """
    x = tuple(dataset)
    out: list[Dataset] = []
    seen: set[Dataset] = set()
    for i in range(len(x)):
        y = x[:i] + x[i + 1:]
        key = tuple(sorted(y, key=repr))
        if key not in seen:
            seen.add(key)
            out.append(y)
    for v in universe:
        y = x + (v,)
        key = tuple(sorted(y, key=repr))
        if key not in seen:
            seen.add(key)
            out.append(y)
    return out


def neighbors_replace(dataset: Sequence[Hashable], universe: Iterable[Hashable]) -> list[Dataset]:
    """All datasets of the same size that differ from dataset in one record.

    The record at index i is replaced by a different value of the universe.
    Equal multisets are listed once. Cost: O(n^2 |universe|).
    """
    x = tuple(dataset)
    values = list(universe)
    out: list[Dataset] = []
    seen: set[Dataset] = set()
    for i in range(len(x)):
        for v in values:
            if v == x[i]:
                continue
            y = x[:i] + (v,) + x[i + 1:]
            key = tuple(sorted(y, key=repr))
            if key not in seen:
                seen.add(key)
                out.append(y)
    return out


def _ratio(a: Number, b: Number) -> Number:
    if isinstance(a, (int, Fraction)) and isinstance(b, (int, Fraction)):
        return Fraction(a) / Fraction(b)
    return float(a) / float(b)


def privacy_loss(p: Pmf, q: Pmf) -> dict[Hashable, float]:
    """The privacy loss ln(p(y) / q(y)) at each output y with p(y) > 0 or q(y) > 0.

    The value is +inf where q(y) = 0 < p(y) and -inf where p(y) = 0 < q(y).
    Outputs with p(y) = q(y) = 0 are left out. Cost: O(|support|).
    """
    out: dict[Hashable, float] = {}
    for y in set(p) | set(q):
        a, b = p.get(y, 0), q.get(y, 0)
        if a == 0 and b == 0:
            continue
        if b == 0:
            out[y] = math.inf
        elif a == 0:
            out[y] = -math.inf
        else:
            out[y] = math.log(_ratio(a, b))
    return out


def max_privacy_loss(p: Pmf, q: Pmf) -> float:
    """The largest privacy loss ln(p(y) / q(y)) over the outputs y with p(y) > 0.

    Returns -inf when p has no output of positive probability. Cost: O(|support|).
    """
    best = -math.inf
    for y, v in privacy_loss(p, q).items():
        if p.get(y, 0) > 0 and v > best:
            best = v
    return best


def hockey_stick(p: Pmf, q: Pmf, epsilon: float) -> float:
    """The hockey-stick divergence: the sum over y of max(0, p(y) - e^epsilon q(y)).

    It is sup over sets S of P(S) - e^epsilon Q(S). Cost: O(|support|).
    """
    a = math.exp(epsilon)
    total = 0.0
    for y in set(p) | set(q):
        d = float(p.get(y, 0)) - a * float(q.get(y, 0))
        if d > 0:
            total += d
    return total


def is_pure_dp(mech_pmf: Callable[[Dataset], Pmf], pairs: Iterable[Pair], epsilon: float, tol: float = 1e-12) -> bool:
    """True if max privacy loss <= epsilon + tol for both orders of every pair.

    Precondition: mech_pmf returns the exact output pmf of the mechanism.
    Cost: O(|pairs|) calls of mech_pmf and O(|support|) work per call.
    """
    for x, y in pairs:
        p, q = mech_pmf(x), mech_pmf(y)
        if max_privacy_loss(p, q) > epsilon + tol or max_privacy_loss(q, p) > epsilon + tol:
            return False
    return True


def is_approx_dp(mech_pmf: Callable[[Dataset], Pmf], pairs: Iterable[Pair], epsilon: float, delta: float, tol: float = 1e-12) -> bool:
    """True if the hockey-stick divergence at e^epsilon is <= delta + tol for both orders of every pair.

    Precondition: mech_pmf returns the exact output pmf of the mechanism.
    Cost: O(|pairs|) calls of mech_pmf and O(|support|) work per call.
    """
    for x, y in pairs:
        p, q = mech_pmf(x), mech_pmf(y)
        if hockey_stick(p, q, epsilon) > delta + tol or hockey_stick(q, p, epsilon) > delta + tol:
            return False
    return True


def renyi_divergence(p: Pmf, q: Pmf, alpha: float) -> float:
    """The Renyi divergence of order alpha > 1: ln(sum_y p(y)^alpha q(y)^(1 - alpha)) / (alpha - 1).

    Returns +inf when q(y) = 0 < p(y) for some y. Cost: O(|support|).
    """
    if alpha <= 1:
        raise ValueError("alpha must be greater than 1")
    s = 0.0
    for y in set(p) | set(q):
        a, b = float(p.get(y, 0)), float(q.get(y, 0))
        if a == 0:
            continue
        if b == 0:
            return math.inf
        s += a * (a / b) ** (alpha - 1)
    return math.log(s) / (alpha - 1)


def empirical_pmf(samples: Iterable[Hashable]) -> dict[Hashable, float]:
    """The fraction of the samples equal to each value. Cost: O(number of samples)."""
    counts: dict[Hashable, int] = {}
    n = 0
    for s in samples:
        counts[s] = counts.get(s, 0) + 1
        n += 1
    if n == 0:
        return {}
    return {k: c / n for k, c in counts.items()}


def hoeffding_margin(n: int, beta: float) -> float:
    """The margin t = sqrt(ln(2 / beta) / (2 n)).

    For n independent samples of a [0, 1] variable, the empirical mean is
    within t of the true mean with probability at least 1 - beta (Hoeffding).
    """
    if n <= 0 or not 0 < beta < 1:
        raise ValueError("need n >= 1 and 0 < beta < 1")
    return math.sqrt(math.log(2 / beta) / (2 * n))


def log_ratio_grid(logpdf_x: Callable[[float], float], logpdf_y: Callable[[float], float], grid: Iterable[float]) -> float:
    """The largest |logpdf_x(z) - logpdf_y(z)| over the points z of the grid.

    Use it to check the log density ratio of a continuous mechanism on two
    neighbors. Cost: O(|grid|) calls of each function.
    """
    best = 0.0
    for z in grid:
        d = abs(logpdf_x(z) - logpdf_y(z))
        if d > best:
            best = d
    return best
