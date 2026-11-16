# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-conditional-modes/. The authors are listed in prov/ZDD3HA.jsonl.

import itertools
import random

from iterated_conditional_modes import (
    energy,
    icm,
    is_icm_local_minimum,
    local_costs,
    neighbor_lists,
)


def grid_pairs(w, h, rng):
    out = []
    for v in range(h):
        for u in range(w):
            if u + 1 < w:
                out.append((v * w + u, v * w + u + 1, rng.randint(1, 3)))
            if v + 1 < h:
                out.append((v * w + u, (v + 1) * w + u, rng.randint(1, 3)))
    return out


def random_instance(rng):
    w, h, L = rng.randint(1, 4), rng.randint(1, 3), rng.randint(2, 4)
    while L ** (w * h) > 4096:
        h -= 1
    n = w * h
    D = [[rng.randint(-5, 9) for _ in range(L)] for _ in range(n)]
    V = [[rng.randint(0, 6) for _ in range(L)] for _ in range(L)]  # any matrix
    return D, grid_pairs(w, h, rng), V


def test_local_costs_match_energy_differences():
    rng = random.Random(1)
    for _ in range(100):
        D, pairs, V = random_instance(rng)
        n, L = len(D), len(V)
        f = [rng.randrange(L) for _ in range(n)]
        nbrs = neighbor_lists(n, pairs)
        p = rng.randrange(n)
        c = local_costs(D, V, nbrs, f, p)
        for l in range(L):
            g = list(f)
            g[p] = l
            assert energy(D, pairs, V, g) - energy(D, pairs, V, f) == c[l] - c[f[p]]


def test_result_is_a_local_minimum_and_energy_does_not_rise():
    rng = random.Random(2)
    for _ in range(120):
        D, pairs, V = random_instance(rng)
        n, L = len(D), len(V)
        f0 = [rng.randrange(L) for _ in range(n)]
        e0 = energy(D, pairs, V, f0)
        prev = e0
        for sweeps in range(1, 8):
            g, _ = icm(D, pairs, V, f0, max_sweeps=sweeps)
            e = energy(D, pairs, V, g)
            assert e <= prev
            prev = e
        f, _ = icm(D, pairs, V, f0)
        assert is_icm_local_minimum(D, pairs, V, f)
        opt = min(energy(D, pairs, V, g) for g in itertools.product(range(L), repeat=n))
        assert opt <= energy(D, pairs, V, f) <= e0


def test_no_pair_terms_gives_the_exact_minimum():
    rng = random.Random(3)
    for _ in range(50):
        n, L = rng.randint(1, 8), rng.randint(2, 5)
        D = [[rng.randint(0, 9) for _ in range(L)] for _ in range(n)]
        V = [[0] * L for _ in range(L)]
        f, sweeps = icm(D, [], V, [0] * n)
        assert energy(D, [], V, f) == sum(min(row) for row in D)
        assert sweeps <= 2


def test_worked_example_and_order_dependence():
    y = [0, 1, 0, 0, 1, 1, 0, 1, 1, 1]
    D = [[0 if l == v else 2 for l in (0, 1)] for v in y]
    pairs = [(i, i + 1, 1) for i in range(len(y) - 1)]
    V = [[0, 3], [3, 0]]
    assert energy(D, pairs, V, y) == 15
    f, sweeps = icm(D, pairs, V)
    assert f == [1, 1, 0, 0, 1, 1, 1, 1, 1, 1] and sweeps == 2
    assert energy(D, pairs, V, f) == 10
    g, _ = icm(D, pairs, V, order=list(range(9, -1, -1)))
    assert g == [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    assert energy(D, pairs, V, g) == 7
    best = min(energy(D, pairs, V, h) for h in itertools.product((0, 1), repeat=10))
    assert best == 7
