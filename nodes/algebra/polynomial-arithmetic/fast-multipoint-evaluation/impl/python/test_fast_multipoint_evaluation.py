# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-multipoint-evaluation/. The authors are listed in prov/VW4WSE.jsonl.

import random
from fractions import Fraction

import pytest

from fast_multipoint_evaluation import (
    evaluate,
    evaluate_horner,
    schoolbook_mul,
    subproduct_tree,
)


class ModP:
    """An element of Z/pZ, enough for the tests."""

    def __init__(self, v: int, p: int) -> None:
        self.p = p
        self.v = v % p

    def _c(self, o):
        return o.v if isinstance(o, ModP) else o

    def __add__(self, o):
        return ModP(self.v + self._c(o), self.p)

    __radd__ = __add__

    def __sub__(self, o):
        return ModP(self.v - self._c(o), self.p)

    def __rsub__(self, o):
        return ModP(self._c(o) - self.v, self.p)

    def __mul__(self, o):
        return ModP(self.v * self._c(o), self.p)

    __rmul__ = __mul__

    def __neg__(self):
        return ModP(-self.v, self.p)

    def __truediv__(self, o):
        d = self._c(o) % self.p
        if d == 0:
            raise ZeroDivisionError
        return ModP(self.v * pow(d, -1, self.p), self.p)

    def __rtruediv__(self, o):
        return ModP(o, self.p) / self

    def __eq__(self, o):
        return self.v == self._c(o) % self.p

    def __hash__(self):
        return hash(self.v)

    def __repr__(self):
        return f"{self.v} mod {self.p}"


# Independent oracle: the sum of c_k u^k with plain integer powers.


def oracle(f, points, p=None):
    out = []
    for u in points:
        if p:
            out.append(sum(c * pow(u, k, p) for k, c in enumerate(f)) % p)
        else:
            out.append(sum(c * u**k for k, c in enumerate(f)))
    return out


def ints(v):
    return [x.v if isinstance(x, ModP) else x for x in v]


PRIMES = [2, 3, 7, 998244353]


def test_page_example():
    assert evaluate([1, -2, 0, 1], [0, 1, 2, 3]) == [1, 0, 5, 22]
    levels = subproduct_tree([0, 1, 2, 3])
    assert levels[1] == [[0, -1, 1], [6, -5, 1]]
    assert levels[2] == [[0, -6, 11, -6, 1]]


def test_over_z_random():
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randint(1, 70)
        f = [rng.randint(-50, 50) for _ in range(rng.randint(0, n))]
        pts = [rng.randint(-30, 30) for _ in range(n)]
        assert evaluate(f, pts) == oracle(f, pts)


@pytest.mark.parametrize("p", PRIMES)
def test_mod_p_random(p):
    rng = random.Random(p)
    for _ in range(60):
        n = rng.randint(1, 60)
        f = [rng.randrange(p) for _ in range(rng.randint(0, n))]
        pts = [rng.randrange(p) for _ in range(n)]
        got = evaluate([ModP(c, p) for c in f], [ModP(u, p) for u in pts])
        assert ints(got) == oracle(f, pts, p)


def test_fraction_points():
    rng = random.Random(4)
    for _ in range(40):
        n = rng.randint(1, 30)
        f = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n)]
        pts = [Fraction(rng.randint(-9, 9), rng.randint(1, 7)) for _ in range(n)]
        assert evaluate(f, pts) == oracle(f, pts)


def test_schoolbook_multiplier_and_horner_agree():
    rng = random.Random(8)
    for _ in range(30):
        n = rng.randint(1, 50)
        f = [rng.randint(-9, 9) for _ in range(n)]
        pts = [rng.randint(-9, 9) for _ in range(n)]
        assert evaluate(f, pts, mul=schoolbook_mul) == evaluate_horner(f, pts) == evaluate(f, pts)


def test_large_mod_p():
    p = 998244353
    rng = random.Random(12)
    n = 300
    f = [rng.randrange(p) for _ in range(n)]
    pts = [rng.randrange(p) for _ in range(n)]
    got = evaluate([ModP(c, p) for c in f], [ModP(u, p) for u in pts])
    assert ints(got) == oracle(f, pts, p)


def test_edge_cases():
    assert evaluate([1, 2, 3], []) == []
    # Zero polynomial, with and without stored zeros.
    assert evaluate([], [1, 2, 3]) == [0, 0, 0]
    assert evaluate([0, 0], [5, 6]) == [0, 0]
    # Constants and degree 1.
    assert evaluate([7], [0, 1, -4]) == [7, 7, 7]
    assert evaluate([1, 2], [3]) == [7]
    # Leading zero coefficients are ignored.
    assert evaluate([1, -2, 0, 1, 0, 0], [0, 1, 2, 3]) == [1, 0, 5, 22]
    # Repeated points.
    assert evaluate([1, 1, 1], [2, 2, 2, -1]) == [7, 7, 7, 1]
    # Degree much larger than the number of points, and much smaller.
    rng = random.Random(2)
    f = [rng.randint(-5, 5) for _ in range(300)] + [1]
    pts = [rng.randint(-5, 5) for _ in range(5)]
    assert evaluate(f, pts) == oracle(f, pts)
    pts = [rng.randint(-5, 5) for _ in range(200)]
    assert evaluate([3, 1], pts) == oracle([3, 1], pts)
    # An odd number of points, so a node is carried up without a sibling.
    assert evaluate([0, 0, 1], [1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]
    # Over Z/2: all points, every value.
    two = [ModP(c, 2) for c in [1, 1, 0, 1]]
    assert ints(evaluate(two, [ModP(0, 2), ModP(1, 2)])) == [1, 1]
