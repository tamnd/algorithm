# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-characteristic-set-method/. The authors are listed in prov/RYT59J.jsonl.
"""Brute-force tests over Z/7Z, where every point of the affine space can be checked."""

import itertools
import random

from wu_characteristic_set_method import (add, mul, cls, deg, init, prem_chain,
                                          basic_set, charset, decompose, wu_prove,
                                          reduced, is_constant)

P7 = 7


class Mod:
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v % P7

    def _o(self, o):
        return o.v if isinstance(o, Mod) else o

    def __add__(self, o):
        return Mod(self.v + self._o(o))

    __radd__ = __add__

    def __sub__(self, o):
        return Mod(self.v - self._o(o))

    def __rsub__(self, o):
        return Mod(self._o(o) - self.v)

    def __mul__(self, o):
        return Mod(self.v * self._o(o))

    __rmul__ = __mul__

    def __neg__(self):
        return Mod(-self.v)

    def __eq__(self, o):
        return self.v == self._o(o) % P7

    def __ne__(self, o):
        return not self == o

    def __hash__(self):
        return self.v


def ev(p, pt, m=None):
    s = 0
    for e, c in p.items():
        t = c.v if isinstance(c, Mod) else c
        for v, k in zip(pt, e):
            t *= v ** k
        s += t
    return s % m if m else s


def rand_poly(rng, n, terms, maxdeg, mod=True):
    p = {}
    for _ in range(terms):
        e = tuple(rng.randint(0, maxdeg) for _ in range(n))
        if sum(e) > maxdeg + 1:
            continue
        c = rng.randint(1, P7 - 1)
        p = add(p, {e: Mod(c) if mod else rng.choice([-2, -1, 1, 2])})
    return p


def zeros(P, n, m=P7):
    pts = itertools.product(range(m), repeat=n)
    return {pt for pt in pts if all(ev(p, pt, m) == 0 for p in P)}


def quasi_zeros(C, n, m=P7):
    h = [init(b) for b in C]
    return {pt for pt in zeros(C, n, m) if all(ev(g, pt, m) != 0 for g in h)}


def check_ascending(C):
    if is_constant(C):
        return
    for k, b in enumerate(C):
        assert cls(b) >= 0
        if k:
            assert cls(b) > cls(C[k - 1])
        assert reduced(b, C[:k])


def test_charset_properties_mod7():
    rng = random.Random(11)
    n = 3
    for _ in range(60):
        P = [rand_poly(rng, n, rng.randint(1, 3), 2) for _ in range(rng.randint(1, 3))]
        P = [p for p in P if p]
        C, P2 = charset(P)
        check_ascending(C)
        zP = zeros(P, n)
        if is_constant(C):
            assert not zP
            continue
        for p in P:
            assert prem_chain(p, C) == {}
        assert zP <= zeros(C, n)
        assert quasi_zeros(C, n) <= zP


def test_decomposition_mod7():
    rng = random.Random(12)
    n = 3
    sizes = []
    for _ in range(40):
        P = [rand_poly(rng, n, rng.randint(1, 3), 2) for _ in range(rng.randint(1, 3))]
        P = [p for p in P if p]
        D = decompose(P)
        sizes.append(len(D))
        union = set()
        for C in D:
            check_ascending(C)
            union |= quasi_zeros(C, n)
        assert union == zeros(P, n)
    assert max(sizes) >= 2


def test_integers_pointwise():
    rng = random.Random(13)
    n = 3
    for _ in range(30):
        P = [rand_poly(rng, n, rng.randint(1, 3), 2, mod=False) for _ in range(2)]
        P = [p for p in P if p]
        C, _ = charset(P)
        if is_constant(C):
            continue
        for p in P:
            assert prem_chain(p, C) == {}
        for m in (5, 11):
            assert quasi_zeros(C, n, m) <= zeros(P, n, m)
            assert zeros(P, n, m) <= zeros(C, n, m)


def var(n, i, k=1):
    e = [0] * n
    e[i] = k
    return {tuple(e): 1}


def parallelogram():
    # variables u1 < u2 < u3 < x1 < x2 < x3 < x4 (indices 0..6)
    n = 7
    u1, u2, u3, x1, x2, x3, x4 = (var(n, i) for i in range(n))
    H = [add(x2, u3, -1),                                    # C on the line y = u3
         add(mul(add(x1, u1, -1), u3), mul(x2, u2), -1),     # BC parallel to AD
         add(mul(x4, x1), mul(x3, x2), -1),                  # O on AC
         add(mul(x4, add(u2, u1, -1)), mul(u3, add(x3, u1, -1)), -1)]  # O on BD
    return n, H, (u1, u2, u3, x1, x2, x3, x4)


def test_parallelogram_theorem():
    n, H, (u1, u2, u3, x1, x2, x3, x4) = parallelogram()
    ok, r, conds = wu_prove(H, add(mul({(0,) * n: 2}, x3), x1, -1))   # 2 x3 = x1
    assert ok and r == {}
    ok2, _, _ = wu_prove(H, add(mul({(0,) * n: 2}, x4), x2, -1))      # 2 x4 = x2
    assert ok2
    bad, r3, _ = wu_prove(H, add(x3, x4, -1))                          # false claim
    assert not bad and r3
    C, _ = charset(H)
    assert [cls(b) for b in C] == [3, 4, 5, 6]
    assert C[1] == add(x2, u3, -1)
    assert C[0] == add(mul(u3, x1), mul(u3, add(u1, u2)), -1)   # x1 = u1 + u2
    # nondegeneracy conditions: u3, 2 u1 u3^2 and 2 u1 u3^3 (u1 + u2)
    assert conds[0] == u3 and len(conds) == 3


def test_edges():
    n = 2
    one = {(0, 0): 1}
    x, y = var(n, 0), var(n, 1)
    assert charset([])[0] == []
    assert decompose([]) == [[]]
    assert charset([one])[0] == [one]            # the unit ideal
    assert decompose([one]) == []
    assert decompose([x, add(x, one, -1)]) == []  # x = 0 and x = 1
    C, _ = charset([mul(x, y)])                   # a single generator
    assert C == [mul(x, y)]
    D = decompose([mul(x, y)])                    # x y = 0: y = 0 (x != 0) or x = 0
    assert len(D) == 2
    assert charset([{}, x])[0] == [x]             # the zero polynomial is dropped
    assert basic_set([mul(y, y), add(y, x)]) == [add(y, x)]
    ok, r, _ = wu_prove([one], x)
    assert ok
    # many reduction steps: y^6 - x by y^2 - x leaves x^3 - x
    C = [add(mul(y, y), x, -1)]
    assert prem_chain(add(var(n, 1, 6), x, -1), C) == add(var(n, 0, 3), x, -1)
