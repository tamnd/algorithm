# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-probe-lsh/. The authors are listed in prov/9SW2DV.jsonl.

import itertools
import math
import random

from multi_probe_lsh import MultiProbeLSH, perturbations

POINTS = [(1, 1), (4.3, 2.0), (2.5, 4.5), (6, 6), (-2, 5), (9, 1), (0, -3), (3, 0)]
GRID = [([[1, 0], [0, 1]], [0.5, 1.0])]


def score(delta, x_minus, w):
    return sum((xm if dj == -1 else w - xm) ** 2 for dj, xm in zip(delta, x_minus) if dj)


def test_example_sequence() -> None:
    seq = [d for d, _ in perturbations([3.7, 3.5], 4.0)]
    assert seq == [(1, 0), (0, 1), (1, 1), (0, -1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]


def test_example_query() -> None:
    lsh = MultiProbeLSH(POINTS, 2, 1, 4.0, functions=GRID)
    q = (3.2, 2.5)
    assert sorted(lsh.candidates(q, 0)) == [0, 7]
    assert lsh.query(q, 0) == 7
    assert lsh.query(q, 1) == 1
    assert sorted(lsh.candidates(q, 4)) == [0, 1, 2, 3, 6, 7]


def test_edges() -> None:
    assert list(perturbations([], 1.0)) == []
    assert [d for d, _ in perturbations([0.25], 1.0)] == [(-1,), (1,)]
    lsh = MultiProbeLSH([], 3, 2, 1.0)
    assert lsh.query((0.0, 0.0), 5) is None
    one = MultiProbeLSH([(0.0, 0.0)], 2, 1, 1.0, seed=1)
    assert one.query((0.0, 0.0), 0) == 0


def test_perturbations_against_enumeration() -> None:
    rng = random.Random(2007)
    for _ in range(600):
        m = rng.randint(1, 5)
        w = rng.uniform(0.5, 4.0)
        xm = [rng.uniform(0.0, w) for _ in range(m)]
        got = list(perturbations(xm, w))
        scores = [s for _, s in got]
        assert all(a <= b + 1e-12 for a, b in zip(scores, scores[1:]))
        everything = {d for d in itertools.product((-1, 0, 1), repeat=m) if any(d)}
        assert len(got) == len(everything) == len({d for d, _ in got})
        assert {d for d, _ in got} == everything
        for d, s in got:
            assert math.isclose(s, score(d, xm, w), abs_tol=1e-9)


def test_query_against_brute_force() -> None:
    rng = random.Random(950)
    for _ in range(500):
        n = rng.randint(1, 30)
        dim = rng.randint(1, 4)
        pts = [tuple(rng.uniform(-5, 5) for _ in range(dim)) for _ in range(n)]
        m, tables, w = rng.randint(1, 4), rng.randint(1, 3), rng.uniform(0.5, 3.0)
        lsh = MultiProbeLSH(pts, m, tables, w, seed=rng.randrange(10**6))
        q = tuple(rng.uniform(-5, 5) for _ in range(dim))
        probes = rng.randint(0, 3**m)
        keys = lsh.probed_keys(q, probes)
        expected = set()
        for (a, b), ks in zip(lsh.functions, keys):
            assert len(ks) == min(probes, 3**m - 1) + 1 and len(set(ks)) == len(ks)
            for i, p in enumerate(pts):
                if lsh._key(a, b, p)[0] in ks:
                    expected.add(i)
        assert lsh.candidates(q, probes) == expected
        best = lsh.query(q, probes)
        if expected:
            assert math.dist(pts[best], q) == min(math.dist(pts[i], q) for i in expected)
        else:
            assert best is None
        assert lsh.candidates(q, 0) <= expected
        if probes == 3**m - 1:
            for (a, b) in lsh.functions:
                hq = lsh._key(a, b, q)[0]
                for i, p in enumerate(pts):
                    if max(abs(x - y) for x, y in zip(lsh._key(a, b, p)[0], hq)) <= 1:
                        assert i in expected
