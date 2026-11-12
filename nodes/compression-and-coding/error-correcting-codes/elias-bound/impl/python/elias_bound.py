# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-bound/. The authors are listed in prov/BBQKPZ.jsonl.

"""The Elias-Bassalygo bound, finite and asymptotic, and the Johnson-type count of
codewords in a ball that its proof uses. Fractions keep the finite bound exact."""

from fractions import Fraction
from math import comb, log, sqrt


def volume(q: int, n: int, r: int) -> int:
    """V_q(n, r): the number of words within distance r of a fixed word."""
    return sum(comb(n, i) * (q - 1) ** i for i in range(min(r, n) + 1))


def ball_list_bound(q: int, n: int, d: int, r: int) -> Fraction | None:
    """theta n d / (r^2 - 2 theta n r + theta n d): the most codewords of a code with
    minimum distance d that fit in a ball of radius r <= theta n. None when the
    denominator is not positive (the radius is at or above the Johnson radius)."""
    theta = Fraction(q - 1, q)
    if r > theta * n:
        return None
    den = r * r - 2 * theta * n * r + theta * n * d
    if den <= 0:
        return None
    return theta * n * d / den


def elias_bound(q: int, n: int, d: int) -> tuple[int, int]:
    """min over r of floor(ball_list_bound(r) * q^n / V_q(n, r)): an upper bound on
    A_q(n, d) for every code, linear or not. Returns (bound, best radius)."""
    best: Fraction | None = None
    best_r = 0
    for r in range(n + 1):
        k = ball_list_bound(q, n, d, r)
        if k is None:
            continue
        v = k * Fraction(q ** n, volume(q, n, r))
        if best is None or v < best:
            best, best_r = v, r
    assert best is not None  # r = 0 always gives q^n
    return int(best), best_r


def hamming_bound(q: int, n: int, d: int) -> int:
    return q ** n // volume(q, n, (d - 1) // 2)


def count_in_ball(words: list[tuple[int, ...]], center: tuple[int, ...], r: int) -> int:
    return sum(1 for w in words if sum(a != b for a, b in zip(w, center)) <= r)


def entropy_q(x: float, q: int) -> float:
    if x <= 0:
        return 0.0
    return x * log(q - 1, q) - x * log(x, q) - (1 - x) * log(1 - x, q)


def johnson_radius(delta: float, q: int = 2) -> float:
    """J_q(delta) = theta (1 - sqrt(1 - delta / theta)), the smaller root of
    x^2 - 2 theta x + theta delta = 0."""
    theta = 1 - 1 / q
    if delta >= theta:
        return theta
    return theta * (1 - sqrt(1 - delta / theta))


def elias_rate(delta: float, q: int = 2) -> float:
    """Asymptotic Elias-Bassalygo bound: R <= 1 - h_q(J_q(delta))."""
    return max(0.0, 1 - entropy_q(johnson_radius(delta, q), q))


def hamming_rate(delta: float, q: int = 2) -> float:
    return max(0.0, 1 - entropy_q(delta / 2, q))


def plotkin_rate(delta: float, q: int = 2) -> float:
    return max(0.0, 1 - delta / (1 - 1 / q))
