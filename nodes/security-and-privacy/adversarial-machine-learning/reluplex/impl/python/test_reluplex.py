# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reluplex/. The authors are listed in prov/J93TRS.jsonl.

"""Tests of Reluplex on seeded synthetic ReLU networks with rational weights only."""

import itertools
import random
from fractions import Fraction as Fr

import mlkit as m
from reluplex import Query, encode, exists_output_at_least, reluplex, verify_robust

# The network of the worked example: two inputs, two hidden ReLUs, two logits.
EXAMPLE = [([[Fr(2), Fr(-1)], [Fr(1), Fr(-2)]], [Fr(0), Fr(1, 2)]), ([[Fr(1), Fr(-1)], [Fr(-2), Fr(2)]], [Fr(1), Fr(0)])]


def forward(layers, x):
    a = list(x)
    for k, (w, b) in enumerate(layers):
        a = [sum((wi * ai for wi, ai in zip(row, a)), Fr(0)) + bi for row, bi in zip(w, b)]
        if k < len(layers) - 1:
            a = [max(v, Fr(0)) for v in a]
    return a


def exact_max(layers, lower, upper, row):
    """Exact max of row . z(x) over a 2-dimensional box, in rational arithmetic.

    The oracle enumerates every activation pattern. On the region of one pattern the
    network is affine, so the maximum over the region is at a vertex; each vertex is
    the meet of two constraint lines, solved by Cramer's rule.
    """
    d = 2
    sizes = [len(w) for w, _ in layers[:-1]]
    best = None
    for pat in itertools.product([0, 1], repeat=sum(sizes)):
        cons = [([Fr(1), Fr(0)], -lower[0]), ([Fr(-1), Fr(0)], upper[0]), ([Fr(0), Fr(1)], -lower[1]), ([Fr(0), Fr(-1)], upper[1])]
        a = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]
        c = [Fr(0), Fr(0)]
        p = 0
        for k, (w, b) in enumerate(layers):
            a2 = [[sum((w[i][t] * a[t][j] for t in range(len(a))), Fr(0)) for j in range(d)] for i in range(len(w))]
            c2 = [sum((w[i][t] * c[t] for t in range(len(c))), Fr(0)) + b[i] for i in range(len(w))]
            if k < len(layers) - 1:
                for i in range(len(w)):
                    if pat[p]:
                        cons.append((a2[i], c2[i]))
                    else:
                        cons.append(([-v for v in a2[i]], -c2[i]))
                        a2[i], c2[i] = [Fr(0)] * d, Fr(0)
                    p += 1
            a, c = a2, c2
        g = [sum((row[i] * a[i][j] for i in range(len(row))), Fr(0)) for j in range(d)]
        g0 = sum((row[i] * c[i] for i in range(len(row))), Fr(0))
        for (r1, c1), (r2, c2v) in itertools.combinations(cons, 2):
            det = r1[0] * r2[1] - r1[1] * r2[0]
            if det == 0:
                continue
            x0 = (-c1 * r2[1] + r1[1] * c2v) / det
            x1 = (-r1[0] * c2v + c1 * r2[0]) / det
            if all(r[0] * x0 + r[1] * x1 + cc >= 0 for r, cc in cons):
                v = g[0] * x0 + g[1] * x1 + g0
                best = v if best is None else max(best, v)
    return best


def rational_net(rng: random.Random, sizes: list[int]) -> list:
    """A seeded network from mlkit, with each weight rounded to a multiple of 1/8."""
    if len(sizes) == 3:
        net = m.tiny_relu_net(rng, sizes[0], sizes[1], sizes[2])
        raw = [(net["W1"], net["b1"]), (net["W2"], net["b2"])]
    else:
        raw = [([[rng.uniform(-2, 2) for _ in range(a)] for _ in range(b)], [rng.uniform(-1, 1) for _ in range(b)])
               for a, b in zip(sizes, sizes[1:])]
    return [([[Fr(round(v * 8), 8) for v in r] for r in w], [Fr(round(v * 8), 8) for v in b]) for w, b in raw]


def test_example_is_robust_at_one_quarter():
    x = [Fr(1, 2), Fr(1, 2)]
    assert forward(EXAMPLE, x) == [Fr(3, 2), Fr(-1)]
    assert verify_robust(EXAMPLE, x, 0, Fr(1, 4)) is None
    lower, upper = [Fr(1, 4)] * 2, [Fr(3, 4)] * 2
    assert exact_max(EXAMPLE, lower, upper, [Fr(-1), Fr(1)]) == Fr(-1)


def test_example_radius_is_5_over_12():
    x = [Fr(1, 2), Fr(1, 2)]
    assert verify_robust(EXAMPLE, x, 0, Fr(5, 12) - Fr(1, 1000)) is None
    cex = verify_robust(EXAMPLE, x, 0, Fr(5, 12))
    assert cex is not None
    z = forward(EXAMPLE, cex)
    assert z[1] >= z[0]
    assert all(abs(a - Fr(1, 2)) <= Fr(5, 12) for a in cex)


def test_plain_linear_program():
    # x1 + x2 >= 3 with 0 <= x1, x2 <= 1 has no solution; >= 2 has one.
    for t, sat in ((Fr(3), False), (Fr(2), True)):
        q = Query(3)
        q.lo[0] = q.hi[0] = q.val[0] = Fr(1)
        for j in (1, 2):
            q.lo[j], q.hi[j] = Fr(0), Fr(1)
        s = q.add_basic({1: Fr(1), 2: Fr(1)}, t, None)
        sol = reluplex(q)
        assert (sol is not None) == sat
        if sol is not None:
            assert sol[s] == sol[1] + sol[2] >= t


def test_single_relu_pair():
    # f = max(0, b) with b = x - 1/2, x in [0, 1]: f >= 1/2 holds only at x = 1.
    for t, sat in ((Fr(1, 2), True), (Fr(1, 2) + Fr(1, 64), False)):
        layers = [([[Fr(1)]], [Fr(-1, 2)]), ([[Fr(1)]], [Fr(0)])]
        q, inputs = encode(layers, [Fr(0)], [Fr(1)], [Fr(1)], t)
        sol = reluplex(q, tau=1)
        assert (sol is not None) == sat
        if sat:
            assert sol[inputs[0]] == 1


def check_solution(layers, lower, upper, row, t, sol):
    assert all(a <= v <= b for a, v, b in zip(lower, sol, upper))
    z = forward(layers, sol)
    assert sum((r * v for r, v in zip(row, z)), Fr(0)) >= t


def test_against_exhaustive_enumeration():
    rng = random.Random(2017)
    sat_count = 0
    for case in range(500):
        if case % 4 == 3:
            sizes = [2, 2, 1, 2]
        else:
            sizes = [2, rng.randint(1, 3), 2]
        layers = rational_net(rng, sizes)
        lo0 = [Fr(rng.randint(0, 6), 8) for _ in range(2)]
        lower = lo0
        upper = [a + Fr(rng.randint(0, 3), 8) for a in lo0]
        row = [Fr(1), Fr(-1)]
        best = exact_max(layers, lower, upper, row)
        t = best + rng.choice([Fr(-1, 4), Fr(-1, 16), Fr(0), Fr(0), Fr(1, 16), Fr(1, 4)])
        sol = exists_output_at_least(layers, lower, upper, row, t, tau=rng.choice([1, 2, 5]))
        assert (sol is not None) == (best >= t)
        if sol is not None:
            sat_count += 1
            check_solution(layers, lower, upper, row, t, sol)
    assert 150 < sat_count < 450


def test_assignment_meets_the_pairs():
    rng = random.Random(3)
    for _ in range(100):
        layers = rational_net(rng, [2, 3, 2])
        lower, upper = [Fr(0), Fr(0)], [Fr(1), Fr(1)]
        best = exact_max(layers, lower, upper, [Fr(1), Fr(0)])
        q, inputs = encode(layers, lower, upper, [Fr(1), Fr(0)], best)
        sol = reluplex(q)
        assert sol is not None
        for b, f in q.pairs:
            assert sol[f] == max(Fr(0), sol[b])
        for i, r in q.basic.items():
            assert sol[i] == sum((c * sol[j] for j, c in r.items()), Fr(0))


def test_verify_robust_agrees_with_enumeration():
    rng = random.Random(19)
    for _ in range(60):
        layers = rational_net(rng, [2, 3, 2])
        x = [Fr(rng.randint(2, 6), 8), Fr(rng.randint(2, 6), 8)]
        z = forward(layers, x)
        if z[0] == z[1]:
            continue
        y = 0 if z[0] > z[1] else 1
        eps = Fr(rng.randint(0, 2), 8)
        lower = [max(a - eps, Fr(0)) for a in x]
        upper = [min(a + eps, Fr(1)) for a in x]
        row = [Fr(-1), Fr(1)] if y == 0 else [Fr(1), Fr(-1)]
        robust = exact_max(layers, lower, upper, row) < 0
        assert (verify_robust(layers, x, y, eps) is None) == robust
