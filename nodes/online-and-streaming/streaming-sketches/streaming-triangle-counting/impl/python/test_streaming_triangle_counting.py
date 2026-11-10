# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/streaming-triangle-counting/. The authors are listed in prov/1HBVC8.jsonl.

import math
import random
from fractions import Fraction

from streaming_triangle_counting import (
    NeighborhoodSampler,
    count_triangles,
    estimate_triangles,
    neighborhood_sizes,
    second_moment,
)

STREAM = [(1, 2), (2, 3), (1, 3), (3, 4), (2, 4), (4, 5)]
SCRIPTS = [(), (True,), (False,), (False, True), (False, False)]


def _step(state, e):
    """All successor states of one estimator after edge e, with exact probabilities."""
    out = {}
    for script in SCRIPTS:
        used = []

        def coin(p, script=script, used=used):
            if len(used) == len(script):
                raise IndexError
            b = script[len(used)]
            used.append(1)
            prob = Fraction(1) if p >= 1 else Fraction(1, round(1 / p))
            coin.w *= prob if b else 1 - prob
            return b

        coin.w = Fraction(1)
        s = NeighborhoodSampler(coin)
        s.i, s.r1, s.r2, s.c, s.found = state
        try:
            s.process(e)
        except IndexError:
            continue
        if len(used) != len(script) or coin.w == 0:
            continue
        out[s.state()] = out.get(s.state(), 0) + coin.w
    return out


def exact_distribution(stream) -> dict:
    """The exact distribution of the estimate of one sampler, by dynamic programming over states."""
    dist = {(0, None, None, 0, False): Fraction(1)}
    for e in stream:
        nxt: dict = {}
        for st, p in dist.items():
            for st2, q in _step(st, e).items():
                nxt[st2] = nxt.get(st2, 0) + p * q
        dist = nxt
    values: dict = {}
    for (i, _, _, c, found), p in dist.items():
        x = i * c if found else 0
        values[x] = values.get(x, 0) + p
    return values


def test_worked_example() -> None:
    assert count_triangles(STREAM) == 2
    assert neighborhood_sizes(STREAM) == [3, 3, 1, 2, 1, 0]
    dist = exact_distribution(STREAM)
    assert dist == {18: Fraction(1, 9), 0: Fraction(8, 9)}
    assert sum(x * p for x, p in dist.items()) == 2
    assert sum(x * x * p for x, p in dist.items()) == 36 == second_moment(STREAM)


def test_unbiased_exactly_on_random_streams() -> None:
    rng = random.Random(13)
    for _ in range(500):
        n = rng.randint(2, 6)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
        rng.shuffle(edges)
        edges = edges[:7]
        dist = exact_distribution(edges)
        assert sum(dist.values()) == 1
        assert sum(x * p for x, p in dist.items()) == count_triangles(edges)
        assert sum(x * x * p for x, p in dist.items()) == second_moment(edges)


def test_edges() -> None:
    rng = random.Random(0)
    assert estimate_triangles([], 5, rng) == 0
    assert estimate_triangles([(1, 2)], 5, rng) == 0
    star = [(0, i) for i in range(1, 9)]
    path = [(i, i + 1) for i in range(10)]
    for g in (star, path):
        assert exact_distribution(g) == {0: 1}  # triangle-free: always 0
    # one triangle: c = 2 for the first edge, so X = 3 * 2 with probability 1 / (3 * 2)
    assert exact_distribution([(1, 2), (2, 3), (3, 1)]) == {6: Fraction(1, 6), 0: Fraction(5, 6)}
    try:
        NeighborhoodSampler(lambda p: True).process((4, 4))
        raise AssertionError("self-loop accepted")
    except ValueError:
        pass


def test_mean_of_seeded_trials() -> None:
    rng = random.Random(7)
    n = 24
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.35]
    rng.shuffle(edges)
    t = count_triangles(edges)
    m2 = second_moment(edges)
    s = 1500
    est = estimate_triangles(edges, s, random.Random(1))
    sd = math.sqrt((m2 - t * t) / s)
    assert t > 50
    assert abs(est - t) <= 4 * sd
    # the bound E[X^2] <= m * C * T with C = max c(e) <= 2 (max degree - 1)
    c = neighborhood_sizes(edges)
    deg: dict = {}
    for u, v in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    assert m2 <= len(edges) * max(c) * t <= len(edges) * 2 * (max(deg.values()) - 1) * t
