# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allpairs/. The authors are listed in prov/0NZTCD.jsonl.

import random

from allpairs import all_pairs, dot

EXAMPLE = [
    {0: 0.6, 1: 0.8},
    {0: 0.8, 2: 0.6},
    {0: 0.36, 1: 0.48, 3: 0.8},
    {2: 0.6, 3: 0.8},
]


def brute(vs, t):
    return sorted((j, i) for i in range(len(vs)) for j in range(i) if dot(vs[i], vs[j]) >= t)


def test_example() -> None:
    got = all_pairs(EXAMPLE, 0.55)
    assert [(a, b) for a, b, _ in got] == [(0, 2), (2, 3)]
    assert abs(got[0][2] - 0.6) < 1e-12 and abs(got[1][2] - 0.64) < 1e-12


def test_rejects_zero_threshold() -> None:
    try:
        all_pairs(EXAMPLE, 0)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_random_integer_vectors() -> None:
    rng = random.Random(4242)
    for _ in range(600):
        n, d = rng.randint(0, 25), rng.randint(1, 12)
        vs = []
        for _ in range(n):
            vs.append({i: rng.randint(1, 5) for i in range(d) if rng.random() < rng.choice((0.15, 0.4, 0.8))})
        t = rng.randint(1, 40)
        got = all_pairs(vs, t)
        assert sorted((a, b) for a, b, _ in got) == brute(vs, t)
        assert all(s == dot(vs[a], vs[b]) for a, b, s in got)


def test_random_sets_cosine() -> None:
    rng = random.Random(77)
    for _ in range(100):
        sets = [frozenset(rng.sample(range(15), rng.randint(1, 6))) for _ in range(30)]
        vs = [{i: 1 / len(s) ** 0.5 for i in s} for s in sets]
        t = rng.choice((0.3, 0.5, 0.7, 0.9))
        got = {(a, b) for a, b, _ in all_pairs(vs, t)}
        for i in range(30):
            for j in range(i):
                c = len(sets[i] & sets[j]) / (len(sets[i]) * len(sets[j])) ** 0.5
                if abs(c - t) > 1e-9:
                    assert ((j, i) in got) == (c >= t)
