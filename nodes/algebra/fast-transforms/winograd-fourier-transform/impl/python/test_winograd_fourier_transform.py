# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winograd-fourier-transform/. The authors are listed in prov/XCA95E.jsonl.

import cmath
import itertools
import math
import random

import pytest

from winograd_fourier_transform import MODULES, counts, wfta

# (prime, generator, usable module lengths)
FIELDS = [
    (998244353, 3, (2, 4, 7, 8)),  # p - 1 = 2^23 * 7 * 17
    (2521, 17, (2, 3, 4, 5, 7, 8)),  # p - 1 = 2520 = 8 * 9 * 5 * 7
    (97, 5, (2, 3, 4, 8)),
    (17, 3, (2, 4, 8)),
]


def dft_mod(x, w, p):
    n = len(x)
    pw = [pow(w, e, p) for e in range(n)]
    return [sum(x[j] * pw[j * k % n] for j in range(n)) % p for k in range(n)]


def dft_c(x, sign=-1):
    n = len(x)
    pw = [cmath.exp(sign * 2j * math.pi * e / n) for e in range(n)]
    return [sum(x[j] * pw[j * k % n] for j in range(n)) for k in range(n)]


def coprime_orders(lengths, limit):
    out = []
    for r in range(1, len(lengths) + 1):
        for combo in itertools.combinations(lengths, r):
            if all(math.gcd(a, b) == 1 for a, b in itertools.combinations(combo, 2)) and math.prod(combo) <= limit:
                out.append(combo)
    return out


def test_modules_against_direct_dft():
    rng = random.Random(1)
    for p, g, lengths in FIELDS:
        for q in lengths:
            w = pow(g, (p - 1) // q, p)
            for _ in range(40):
                x = [rng.randrange(p) for _ in range(q)]
                assert wfta(x, (q,), w=w, p=p) == dft_mod(x, w, p)


def test_nested_all_orders_mod_p():
    rng = random.Random(2)
    for p, g, lengths in FIELDS:
        for combo in coprime_orders(lengths, 210):
            for order in itertools.permutations(combo):
                n = math.prod(order)
                w = pow(g, (p - 1) // n, p)
                x = [rng.randrange(p) for _ in range(n)]
                assert wfta(x, order, w=w, p=p) == dft_mod(x, w, p)


def test_length_840_mod_2521():
    rng = random.Random(3)
    w = pow(17, 3, 2521)  # order 840
    for order in [(8, 3, 5, 7), (7, 5, 3, 8)]:
        x = [rng.randrange(2521) for _ in range(840)]
        X = wfta(x, order, w=w, p=2521)
        assert X == dft_mod(x, w, 2521)
        assert wfta(X, order, w=w, p=2521, inverse=True) == x


class Count:
    """Integers mod p that count additions (with subtractions) and multiplications."""

    p = 2521
    adds = 0
    mults = 0

    def __init__(self, v):
        self.v = v % Count.p

    def _val(self, o):
        return o.v if isinstance(o, Count) else o

    def __add__(self, o):
        Count.adds += 1
        return Count(self.v + self._val(o))

    __radd__ = __add__

    def __sub__(self, o):
        Count.adds += 1
        return Count(self.v - self._val(o))

    def __mul__(self, o):
        Count.mults += 1
        return Count(self.v * self._val(o))

    __rmul__ = __mul__

    def __mod__(self, m):
        return self


def test_exact_operation_counts():
    rng = random.Random(4)
    table = {2: (2, 0), 3: (6, 2), 4: (8, 1), 5: (17, 5), 7: (36, 8), 8: (26, 4)}
    for q, expect in table.items():
        assert counts((q,)) == expect
    orders = [o for c in coprime_orders((2, 3, 4, 5, 7, 8), 120) for o in itertools.permutations(c)]
    for order in orders + [(8, 3, 5, 7), (5, 7, 3, 4)]:
        n = math.prod(order)
        w = pow(17, 2520 // n, 2521)
        x = [Count(rng.randrange(2521)) for _ in range(n)]
        Count.adds = Count.mults = 0
        X = wfta(x, order, w=w, p=2521)
        assert (Count.adds, Count.mults) == counts(order)
        assert [v.v for v in X] == dft_mod([v.v for v in x], w, 2521)
    # the multiplications are prod(m_i) minus the products of ones
    assert counts((8, 3, 5, 7)) == (12450, 1292)


def test_complex_against_direct_dft():
    rng = random.Random(5)
    for combo in coprime_orders((2, 3, 4, 5, 7, 8), 840):
        order = combo
        n = math.prod(order)
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        ref = dft_c(x)
        X = wfta(x, order)
        scale = math.sqrt(sum(abs(v) ** 2 for v in x))
        tol = 16 * 2.2e-16 * math.log2(2 * n) * scale * math.sqrt(n)
        assert max(abs(a - b) for a, b in zip(X, ref)) <= tol
        y = wfta(X, order, inverse=True)
        assert max(abs(a - b) for a, b in zip(x, y)) <= tol


def test_complex_inverse_matches_reference():
    rng = random.Random(6)
    x = [complex(rng.random(), rng.random()) for _ in range(105)]
    ref = [v / 105 for v in dft_c(x, sign=+1)]
    got = wfta(x, (3, 5, 7), inverse=True)
    assert max(abs(a - b) for a, b in zip(got, ref)) < 1e-13


def test_edge_cases():
    assert wfta([5], ()) == [5]
    assert wfta([3, 1], (2,), w=16, p=17) == [4, 2]
    w = pow(17, 2520 // 60, 2521)
    assert wfta([0] * 60, (4, 3, 5), w=w, p=2521) == [0] * 60
    assert wfta([1] + [0] * 59, (4, 3, 5), w=w, p=2521) == [1] * 60
    assert wfta([7] * 60, (4, 3, 5), w=w, p=2521) == [420] + [0] * 59
    X = wfta([1.0] + [0.0] * 104, (3, 5, 7))
    assert max(abs(v - 1) for v in X) < 1e-14
    X = wfta([2.0] * 56, (8, 7))
    assert abs(X[0] - 112) < 1e-12 and max(abs(v) for v in X[1:]) < 1e-12


def test_bad_arguments():
    with pytest.raises(ValueError):
        wfta([0] * 8, (2, 4))
    with pytest.raises(ValueError):
        wfta([0] * 9, (9,))
    with pytest.raises(ValueError):
        wfta([0] * 5, (2, 3))
    with pytest.raises(ValueError):
        wfta([0] * 6, (2, 3), w=2, p=7)  # 2 has order 3 modulo 7


def test_worked_example_mod_7():
    assert wfta([3, 1, 4, 1, 5, 2], (2, 3), w=3, p=7) == [2, 1, 5, 1, 5, 4]
    assert dft_mod([3, 1, 4, 1, 5, 2], 3, 7) == [2, 1, 5, 1, 5, 4]
    assert set(MODULES) == {2, 3, 4, 5, 7, 8}
