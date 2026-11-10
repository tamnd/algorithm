# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lawler-algorithm/. The authors are listed in prov/TBK2E7.jsonl.

import itertools
import random

import pytest

from lawler_algorithm import lawler_algorithm, objective


def extensions(n, prec):
    for o in itertools.permutations(range(n)):
        pos = {j: i for i, j in enumerate(o)}
        if all(pos[a] < pos[b] for a, b in prec):
            yield o


def brute_force(p, f, prec):
    return min(objective(p, f, o) for o in extensions(len(p), prec))


def lateness(d):
    return lambda t: t - d


def weighted_tardiness(w, d):
    return lambda t: w * max(0, t - d)


def step(levels):
    # nondecreasing step function: levels is a sorted list of (time, value)
    def g(t):
        v = 0
        for x, y in levels:
            if t >= x:
                v = y
        return v
    return g


def random_cost(rng):
    kind = rng.randrange(4)
    if kind == 0:
        return lateness(rng.randint(-3, 20))
    if kind == 1:
        return weighted_tardiness(rng.randint(0, 4), rng.randint(0, 20))
    if kind == 2:
        xs = sorted(rng.sample(range(0, 25), 3))
        ys = sorted(rng.randint(0, 30) for _ in range(3))
        return step(list(zip(xs, ys)))
    a, b = rng.randint(0, 3), rng.randint(-10, 10)
    return lambda t: max(b, a * t - 15)


def random_dag(rng, n):
    perm = list(range(n))
    rng.shuffle(perm)
    return [(perm[i], perm[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]


def test_example() -> None:
    p = [2, 3, 1, 4, 2]
    d = [2, 5, 3, 9, 4]
    w = [3, 1, 2, 1, 2]
    prec = [(0, 1), (2, 1), (1, 3)]
    f = [weighted_tardiness(w[j], d[j]) for j in range(5)]
    order, value = lawler_algorithm(p, f, prec)
    assert order == [0, 2, 4, 1, 3]
    assert value == 3 == brute_force(p, f, prec)
    assert max(objective(p, f, o) for o in extensions(5, prec)) == 16


def test_forward_greedy_fails() -> None:
    # Earliest due date among the available jobs, scheduled from the front.
    p, d, prec = [3, 4, 1], [7, 0, 2], [(0, 1)]
    f = [lateness(x) for x in d]
    assert objective(p, f, [2, 0, 1]) == 8
    assert lawler_algorithm(p, f, prec)[1] == 7 == brute_force(p, f, prec)


def test_edges() -> None:
    assert lawler_algorithm([], []) == ([], 0)
    assert lawler_algorithm([5], [lateness(2)]) == ([0], 3)
    with pytest.raises(ValueError):
        lawler_algorithm([1, 1], [lateness(0), lateness(0)], [(0, 1), (1, 0)])
    with pytest.raises(ValueError):
        lawler_algorithm([1], [])


def test_against_brute_force() -> None:
    rng = random.Random(31)
    for _ in range(250):
        n = rng.randint(1, 7)
        p = [rng.randint(0, 6) for _ in range(n)]
        f = [random_cost(rng) for _ in range(n)]
        prec = random_dag(rng, n)
        order, value = lawler_algorithm(p, f, prec)
        pos = {j: i for i, j in enumerate(order)}
        assert sorted(order) == list(range(n))
        assert all(pos[a] < pos[b] for a, b in prec)
        assert value == objective(p, f, order) == brute_force(p, f, prec)


def test_no_precedence_lateness_matches_edd_value() -> None:
    rng = random.Random(32)
    for _ in range(200):
        n = rng.randint(1, 8)
        p = [rng.randint(1, 6) for _ in range(n)]
        d = [rng.randint(0, 30) for _ in range(n)]
        edd = sorted(range(n), key=lambda j: d[j])
        f = [lateness(x) for x in d]
        assert lawler_algorithm(p, f)[1] == objective(p, f, edd)
