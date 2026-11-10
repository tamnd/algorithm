# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vitter-reservoir-skip/. The authors are listed in prov/2ZA0EM.jsonl.

import itertools
import math
import random
from typing import Iterable, TypeVar

T = TypeVar("T")

_END = object()


def _uniform_open(rng: random.Random) -> float:
    """A uniform real in (0, 1]: never 0, so that its logarithm is finite."""
    return 1.0 - rng.random()


def skip_x(t: int, k: int, rng: random.Random) -> int:
    """Vitter's Algorithm X: the number of items to skip after t processed items.

    Pr[skip >= s] = prod_{j=1..s} (t + j - k) / (t + j). One uniform real is
    used, and the time is O(1 + skip).
    """
    v = rng.random()  # @line L8
    s = 0
    t += 1
    q = (t - k) / t
    while q > v:  # @line L9
        s += 1  # @line L10
        t += 1
        q *= (t - k) / t
    return s  # @line L11


def skip_z(t: int, k: int, w: float, rng: random.Random) -> tuple[int, float]:
    """Vitter's Algorithm Z: the same skip as skip_x, drawn by rejection.

    w is the state W = U^(-1/k) >= 1 left by the previous call (or by the
    start). Returns the skip and the new state. Each round uses O(1)
    uniform reals; the exact test costs O(min(k, skip)) arithmetic steps.
    """
    term = t - k + 1  # @line L12
    while True:  # @line L13
        u = rng.random()  # @line L14
        x = t * (w - 1.0)
        s = math.floor(x)
        tmp = (t + 1) / term
        lhs = math.exp(math.log(((u * tmp * tmp) * (term + s)) / (t + x)) / k) if u > 0 else 0.0  # @line L15
        rhs = (((t + x) / (term + s)) * term) / t  # @line L16
        if lhs <= rhs:  # @line L17
            return s, rhs / lhs if lhs > 0 else math.exp(-math.log(_uniform_open(rng)) / k)
        y = (((u * (t + 1)) / term) * (t + s + 1)) / (t + x)  # @line L18
        if k < s:
            denom = t
            numer_lim = term + s
        else:
            denom = t - k + s
            numer_lim = t + 1
        numer = t + s
        while numer >= numer_lim:
            y = (y * numer) / denom
            denom -= 1
            numer -= 1
        w = math.exp(-math.log(_uniform_open(rng)) / k)  # @line L19
        if math.exp(math.log(y) / k) <= (t + x) / t:  # @line L20
            return s, w


def vitter_reservoir_skip(
    stream: Iterable[T], k: int, rng: random.Random, threshold: float = 22.0
) -> list[T]:
    """Return a uniform random k-subset of a stream (Vitter's Algorithm Z).

    While t <= threshold * k the skip is drawn by Algorithm X, and after
    that by Algorithm Z; threshold = 22 is Vitter's choice. With
    threshold = 0 the method is pure Algorithm Z. If the stream has fewer
    than k items, all of them are returned.

    The output law is that of Algorithm R in exact arithmetic. Cost:
    O(k (1 + log(n / k))) expected time when skipping an item is free, and
    O(k) extra space.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    it = iter(stream)
    reservoir: list[T] = list(itertools.islice(it, k))  # @line L1
    if k == 0 or len(reservoir) < k:
        return reservoir
    t = k
    w = math.exp(-math.log(_uniform_open(rng)) / k)  # @line L2
    while True:  # @line L3
        if t <= threshold * k:  # @line L4
            s = skip_x(t, k, rng)
        else:
            s, w = skip_z(t, k, w, rng)
        x = next(itertools.islice(it, s, None), _END)  # @line L5
        if x is _END:
            return reservoir
        reservoir[rng.randrange(k)] = x  # type: ignore[assignment]  # @line L6
        t += s + 1  # @line L7
