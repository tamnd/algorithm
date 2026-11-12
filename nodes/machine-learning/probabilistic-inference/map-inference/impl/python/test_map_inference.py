# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/map-inference/. The authors are listed in prov/VQER59.jsonl.

import random
from fractions import Fraction as F
from itertools import product

import pytest

from map_inference import Factor, marginal_map, mpe, posterior_marginal_decoding, value


def random_bn(rng, n):
    card = [rng.choice([2, 2, 3]) for _ in range(n)]
    factors = []
    for v in range(n):
        pa = tuple(u for u in range(v) if rng.random() < 0.4)[:3]
        t = {}
        for p in product(*(range(card[u]) for u in pa)):
            w = [rng.randint(0, 4) for _ in range(card[v])]
            if sum(w) == 0:
                w[0] = 1
            for x in range(card[v]):
                t[(x,) + p] = F(w[x], sum(w))
        factors.append(Factor((v,) + pa, t))
    return factors, card


def test_page_example_mpe_and_marginal_map_differ():
    # A: P(A=0) = 0.6, P(A=1) = 0.4. B | A=0 uniform on {0, 1, 2}; B | A=1 is 0 surely.
    pa = Factor((0,), {(0,): F(6, 10), (1,): F(4, 10)})
    pb = Factor((1, 0), {(b, a): (F(1, 3) if a == 0 else F(int(b == 0))) for b in range(3) for a in range(2)})
    fs, card = [pa, pb], [2, 3]
    assert mpe(fs, card, {}) == ((1, 0), F(4, 10))
    assert marginal_map(fs, card, [0], {}) == ((0,), F(6, 10))
    assert posterior_marginal_decoding(fs, card, {}) == (0, 0)
    assert value(fs, (0, 0)) == F(2, 10)


def test_random_networks():
    rng = random.Random(8)
    differ = 0
    for _ in range(300):
        n = rng.randint(2, 6)
        fs, card = random_bn(rng, n)
        ev = {v: rng.randrange(card[v]) for v in rng.sample(range(n), rng.randint(0, 2))}
        free = [v for v in range(n) if v not in ev]
        pe = sum(value(fs, x) for x in product(*(range(c) for c in card))
                 if all(x[v] == e for v, e in ev.items()))
        if pe == 0:
            with pytest.raises(ValueError):
                mpe(fs, card, ev)
            continue
        x, w = mpe(fs, card, ev)
        assert all(x[v] == e for v, e in ev.items()) and value(fs, x) == w
        for y in product(*(range(c) for c in card)):
            if all(y[v] == e for v, e in ev.items()):
                assert value(fs, y) <= w
        # Marginal MAP over all the free variables is MPE.
        q, s = marginal_map(fs, card, free, ev)
        assert s == w
        # Over a part M, the maximum sum is at least the MPE value, and at least the
        # sum at the projection of the MPE assignment.
        m = sorted(rng.sample(free, rng.randint(1, len(free)))) if free else []
        if m:
            q, s = marginal_map(fs, card, m, ev)
            proj = tuple(x[v] for v in m)
            s_proj = sum(value(fs, y) for y in product(*(range(c) for c in card))
                         if all(y[v] == e for v, e in ev.items()) and tuple(y[v] for v in m) == proj)
            assert s >= s_proj >= w
            if s > s_proj:
                differ += 1
    assert differ > 0  # the projection of the MPE is often not a marginal MAP


def test_mpe_decides_satisfiability():
    # Cooper's network for a 3-CNF formula, with the output observed true:
    # the MPE value is positive exactly when the formula is satisfiable.
    rng = random.Random(2)
    for _ in range(60):
        n, m = rng.randint(2, 4), rng.randint(1, 8)
        clauses = [[(v, rng.random() < 0.5) for v in rng.sample(range(n), min(3, n))] for _ in range(m)]
        card = [2] * (n + m + 1)
        fs = [Factor((v,), {(0,): F(1, 2), (1,): F(1, 2)}) for v in range(n)]
        for j, cl in enumerate(clauses):
            scope = (n + j,) + tuple(v for v, _ in cl)
            t = {}
            for a in product((0, 1), repeat=len(scope)):
                sat = any(a[1 + t_] == (1 if pos else 0) for t_, (_, pos) in enumerate(cl))
                t[a] = F(int(a[0] == int(sat)))
            fs.append(Factor(scope, t))
        out = n + m
        scope = (out,) + tuple(range(n, n + m))
        fs.append(Factor(scope, {a: F(int(a[0] == int(all(a[1:])))) for a in product((0, 1), repeat=m + 1)}))
        sat = any(all(any(x[v] == (1 if pos else 0) for v, pos in cl) for cl in clauses)
                  for x in product((0, 1), repeat=n))
        if sat:
            x, w = mpe(fs, card, {out: 1})
            assert w == F(1, 2 ** n)
            assert all(any(x[v] == (1 if pos else 0) for v, pos in cl) for cl in clauses)
        else:
            with pytest.raises(ValueError):
                mpe(fs, card, {out: 1})
