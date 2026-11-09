# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moea-d/. The authors are listed in prov/EZEF0D.jsonl.

import itertools
import math
import random
from fractions import Fraction as Fr

from moea_d import (
    blend_gauss,
    dominates,
    moea_d,
    neighbourhoods,
    simplex_weights,
    tchebycheff,
    update_external,
    update_neighbours,
    weakly_dominates,
    zdt1,
)


def front(images):
    return {y for y in images if not any(dominates(z, y) for z in images)}


def test_example() -> None:
    w = simplex_weights(2, 4)
    assert w == [(0, 1), (Fr(1, 4), Fr(3, 4)), (Fr(1, 2), Fr(1, 2)), (Fr(3, 4), Fr(1, 4)), (1, 0)]
    b = neighbourhoods(w, 3)
    assert b[2] == [2, 1, 3] and b[0] == [0, 1, 2] and b[4] == [4, 3, 2]
    pop = [(k, y) for k, y in enumerate([(1, 10), (2, 9), (5, 5), (8, 2), (10, 1)])]
    z = (1, 1)
    child = ("y", (3, 6))
    assert tchebycheff((3, 6), w[1], z) == Fr(15, 4) and tchebycheff((2, 9), w[1], z) == 6
    assert tchebycheff((3, 6), w[2], z) == Fr(5, 2) and tchebycheff((5, 5), w[2], z) == 2
    assert tchebycheff((3, 6), w[3], z) == Fr(3, 2) and tchebycheff((8, 2), w[3], z) == Fr(21, 4)
    assert sorted(update_neighbours(pop, child, b[2], w, z)) == [1, 3]
    assert [x for x, _ in pop] == [0, "y", 2, "y", 4]
    ext = [(1, 10), (2, 9), (5, 5), (8, 2), (10, 1)]
    update_external(ext, (3, 6))
    assert (3, 6) in ext and len(ext) == 6


def test_simplex_weights_count() -> None:
    for p in range(1, 5):
        for h in range(1, 7):
            w = simplex_weights(p, h)
            assert len(w) == math.comb(h + p - 1, p - 1) == len(set(w))
            assert all(sum(v) == 1 and min(v) >= 0 for v in w)


def test_neighbourhoods_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(1, 12)
        w = [tuple(Fr(rng.randint(0, 5), 5) for _ in range(2)) for _ in range(n)]
        t = rng.randint(1, n)
        b = neighbourhoods(w, t)
        for i in range(n):
            assert len(b[i]) == t == len(set(b[i])) and b[i][0] == i
            d = [sum((a - c) ** 2 for a, c in zip(w[i], w[j])) for j in range(n)]
            inside = max(d[j] for j in b[i])
            assert all(d[j] >= inside for j in range(n) if j not in b[i])


def test_child_replaces_what_it_weakly_dominates() -> None:
    rng = random.Random(2)
    w = simplex_weights(3, 3)
    for _ in range(300):
        pop = [(k, tuple(rng.randint(0, 6) for _ in range(3))) for k in range(len(w))]
        child = ("c", tuple(rng.randint(0, 6) for _ in range(3)))
        z = [min([y[m] for _, y in pop] + [child[1][m]]) for m in range(3)]
        nb = list(range(len(w)))
        old = list(pop)
        update_neighbours(pop, child, nb, w, z)
        for j in nb:
            if weakly_dominates(child[1], old[j][1]):
                assert pop[j] == child


def bits(n):
    return lambda r: tuple(r.randint(0, 1) for _ in range(n))


def uniform_flip(u, v, r):
    return tuple((a if r.random() < 0.5 else b) ^ (1 if r.random() < 1 / len(u) else 0) for a, b in zip(u, v))


def two_knapsacks(x):
    w1 = [3, 1, 4, 1, 5, 9, 2]
    w2 = [2, 7, 1, 8, 2, 8, 1]
    return (-sum(a * b for a, b in zip(x, w1)), -sum((1 - a) * b for a, b in zip(x, w2)))


def test_run_invariants_discrete() -> None:
    for seed in range(3):
        rng = random.Random(seed)
        w = simplex_weights(2, 5)
        seen = set()
        state = {}

        def hook(i, child, z, before, pop):
            if "ext" not in state:
                seen.update(y for _, y in before)
            seen.add(child[1])
            assert len(pop) == len(w)
            assert z == [min(y[m] for y in seen) for m in range(2)]
            for j in range(len(w)):
                if pop[j] is not before[j]:
                    assert pop[j] == child
                    assert tchebycheff(child[1], w[j], z) <= tchebycheff(before[j][1], w[j], z)
            state["ext"] = True

        ext, pop = moea_d(bits(7), two_knapsacks, uniform_flip, w, 3, 6, rng, hook)
        assert set(ext) == front(seen) and len(ext) == len(set(ext))
        assert all(y == two_knapsacks(x) for x, y in pop)


def test_run_invariants_real() -> None:
    rng = random.Random(4)
    w = [tuple(float(v) for v in u) for u in simplex_weights(2, 9)]
    lo, hi = [0.0] * 3, [1.0] * 3
    ext, pop = moea_d(lambda r: tuple(r.random() for _ in range(3)), zdt1, blend_gauss(lo, hi), w, 4, 10, rng)
    assert len(pop) == 10
    assert all(all(0 <= v <= 1 for v in x) and y == zdt1(x) for x, y in pop)
    for a, b in itertools.permutations(ext, 2):
        assert not weakly_dominates(a, b)
