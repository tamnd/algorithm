# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/estrin-scheme/. The authors are listed in prov/SDH9BZ.jsonl.

import math
import random
from fractions import Fraction

import pytest

from estrin_scheme import estrin, estrin_stats, horner, horner_stats, levels


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


def oracle(a, x, p=None):
    if p:
        return sum(c * pow(x, k, p) for k, c in enumerate(a)) % p
    return sum(c * x**k for k, c in enumerate(a))


PRIMES = [2, 3, 7, 998244353]


def test_page_example():
    assert levels([1, 2, 3, 4, 5, 6, 7, 8], 2) == [[1, 2, 3, 4, 5, 6, 7, 8], [5, 11, 17, 23], [49, 109], [1793]]
    assert estrin_stats([1, 2, 3, 4, 5, 6, 7, 8], 2) == (1793, 9, 7, 6)
    assert horner_stats([1, 2, 3, 4, 5, 6, 7, 8], 2) == (1793, 7, 7, 14)


def test_over_z_random():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(0, 80)
        a = [rng.randint(-99, 99) for _ in range(n)]
        x = rng.randint(-20, 20)
        assert estrin(a, x) == oracle(a, x) == horner(a, x)


@pytest.mark.parametrize("p", PRIMES)
def test_mod_p_random(p):
    rng = random.Random(p)
    for _ in range(300):
        n = rng.randint(0, 60)
        a = [rng.randrange(p) for _ in range(n)]
        x = rng.randrange(p)
        got = estrin([ModP(c, p) for c in a], ModP(x, p))
        assert got == oracle(a, x, p)


def test_fraction_random():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(0, 30)
        a = [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(n)]
        x = Fraction(rng.randint(-9, 9), rng.randint(1, 9))
        assert estrin(a, x) == oracle(a, x)


def test_operation_counts_and_depth():
    for n in range(0, 130):
        a = list(range(1, n + 2))
        v, muls, adds, depth = estrin_stats(a, 3)
        lg = math.ceil(math.log2(n + 1)) if n >= 1 else 0
        assert v == oracle(a, 3)
        assert adds == n
        assert muls == n + max(lg - 1, 0)
        assert depth <= 2 * lg
        hv, hm, ha, hd = horner_stats(a, 3)
        assert (hv, hm, ha, hd) == (v, n, n, 2 * n)


def test_floats_close_to_horner():
    rng = random.Random(9)
    for _ in range(100):
        a = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 40))]
        x = rng.uniform(-1, 1)
        assert math.isclose(estrin(a, x), horner(a, x), rel_tol=1e-9, abs_tol=1e-12)


def test_edge_cases():
    assert estrin([], 5) == 0
    assert estrin([0, 0, 0], 5) == 0
    assert estrin([7], 5) == 7
    assert estrin([3, 2], 5) == 13
    # Leading zero coefficients do not change the value.
    assert estrin([1, 2, 3, 0, 0], 4) == estrin([1, 2, 3], 4) == 57
    # Point zero and point one.
    assert estrin([4, 5, 6, 7, 8], 0) == 4
    assert estrin([4, 5, 6, 7, 8], 1) == 30
    # Odd lengths, so a coefficient is carried up.
    assert levels([1, 1, 1], 10) == [[1, 1, 1], [11, 1], [111]]
    assert estrin([1] * 7, 10) == 1111111
    # Over Z/2.
    assert estrin([ModP(1, 2)] * 5, ModP(1, 2)) == 1
