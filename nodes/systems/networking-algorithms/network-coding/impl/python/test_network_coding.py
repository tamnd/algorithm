# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-coding/. The authors are listed in prov/S62752.jsonl.

import random
from fractions import Fraction
from itertools import product

from network_coding import (
    butterfly,
    min_cut,
    multicast,
    random_coefficients,
    random_dag,
    rank,
    reaches,
    routing_max_min,
    solve,
)


def test_solve_over_prime_field():
    rng = random.Random(1)
    q = 101
    for _ in range(50):
        h = rng.randrange(1, 6)
        A = [[rng.randrange(q) for _ in range(h)] for _ in range(h + 2)]
        x = [[rng.randrange(q) for _ in range(3)] for _ in range(h)]
        Y = [[sum(a[k] * x[k][c] for k in range(h)) % q for c in range(3)] for a in A]
        got = solve(A, Y, q)
        if rank(A, q) == h:
            assert got == x
        else:
            assert got is None
    assert rank([[1, 2], [2, 4]], 7) == 1 and rank([[1, 2], [2, 5]], 7) == 2


def xor_code(i, j):
    # Edges: 0 s->a, 1 s->b, 2 a->t1, 3 a->c, 4 b->c, 5 b->t2, 6 c->d, 7 d->t1, 8 d->t2.
    if j == 0:
        return int(i == ("s", 0))
    if j == 1:
        return int(i == ("s", 1))
    return 1


def test_butterfly_xor_delivers_both_bits_to_both_sinks():
    n, edges, s, sinks = butterfly()
    for x1, x2 in product((0, 1), repeat=2):
        g, decoded = multicast(n, edges, s, sinks, [[x1], [x2]], 2, xor_code)
        assert g[6] == [1, 1]
        assert decoded == {5: [[x1], [x2]], 6: [[x1], [x2]]}


def test_butterfly_routing_gets_one_message_per_sink_coding_gets_two():
    n, edges, s, sinks = butterfly()
    assert [min_cut(n, edges, s, t) for t in sinks] == [2, 2]
    assert routing_max_min(n, edges, s, sinks, 2) == 1


def test_butterfly_steiner_tree_packing_is_three_halves():
    n, edges, s, sinks = butterfly()
    sa, sb, at1, ac, bc, bt2, cd, dt1, dt2 = range(9)
    trees = [[sa, at1, ac, cd, dt2], [sb, bt2, bc, cd, dt1], [sa, at1, sb, bt2]]
    half = Fraction(1, 2)
    for t in trees:
        assert reaches(n, [edges[j] for j in t], s, sinks)
    load = [sum(half for t in trees if j in t) for j in range(9)]
    assert max(load) <= 1 and half * len(trees) == Fraction(3, 2)
    # Dual certificate: weights on edges, every edge set that connects s to both sinks weighs >= 1.
    z = [half if j in (sa, sb, cd) else 0 for j in range(9)]
    assert sum(z) == Fraction(3, 2)
    for mask in range(1 << 9):
        sub = [j for j in range(9) if mask >> j & 1]
        if reaches(n, [edges[j] for j in sub], s, sinks):
            assert sum(z[j] for j in sub) >= 1


def test_random_linear_coding_meets_the_ho_bound_on_random_dags():
    q, trials, checked = 101, 150, 0
    for seed in range(25):
        rng = random.Random(seed)
        n = 8
        edges = random_dag(n, 0.5, rng)
        sinks = [n - 2, n - 1]
        h = min(min_cut(n, edges, 0, t) for t in sinks)
        if h == 0:
            continue
        checked += 1
        bound = (1 - Fraction(len(sinks), q)) ** len(edges)
        ok = 0
        for _ in range(trials):
            data = [[rng.randrange(q) for _ in range(4)] for _ in range(h)]
            _, decoded = multicast(n, edges, 0, sinks, data, q, random_coefficients(rng, q))
            if all(decoded[t] is not None for t in sinks):
                ok += 1
                assert all(decoded[t] == data for t in sinks)
        assert Fraction(ok, trials) >= bound
    assert checked >= 15


def test_rate_above_min_cut_cannot_be_decoded():
    rng = random.Random(7)
    n, edges, s, sinks = butterfly()
    for _ in range(50):
        data = [[rng.randrange(13)] for _ in range(3)]
        _, decoded = multicast(n, edges, s, sinks, data, 13, random_coefficients(rng, 13))
        assert decoded == {5: None, 6: None}
