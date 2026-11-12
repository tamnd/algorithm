# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/covariance-matrix/. The authors are listed in prov/N5JYXB.jsonl.

import random
from fractions import Fraction as F

from covariance_matrix import RunningCovariance, naive_covariance, two_pass_covariance


def exact_rank(a: list[list[F]]) -> int:
    m = [row[:] for row in a]
    rank, rows, cols = 0, len(m), len(m[0])
    for c in range(cols):
        piv = next((r for r in range(rank, rows) if m[r][c] != 0), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        for r in range(rows):
            if r != rank and m[r][c] != 0:
                f = m[r][c] / m[rank][c]
                m[r] = [m[r][j] - f * m[rank][j] for j in range(cols)]
        rank += 1
    return rank


def rand_points(rng: random.Random, n: int, d: int) -> list[list[F]]:
    return [[F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(d)] for _ in range(n)]


def test_worked_example() -> None:
    pts = [[F(2), F(0)], [F(4), F(2)], [F(6), F(2)], [F(8), F(4)]]
    assert two_pass_covariance(pts) == [[F(20, 3), 4], [4, F(8, 3)]]
    assert two_pass_covariance(pts, ddof=0) == [[5, 3], [3, 2]]
    a, b = RunningCovariance(2), RunningCovariance(2)
    for p in pts[:2]:
        a.add(p)
    for p in pts[2:]:
        b.add(p)
    assert a.m == [[2, 2], [2, 2]] and b.m == [[2, 2], [2, 2]]
    c = a.merge(b)
    assert c.mean == [5, 2] and c.m == [[20, 12], [12, 8]]


def test_welford_and_merge_exact() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n, d = rng.randint(2, 9), rng.randint(1, 4)
        pts = rand_points(rng, n, d)
        direct = two_pass_covariance(pts)
        w = RunningCovariance(d)
        for p in pts:
            w.add(p)
        assert w.covariance() == direct
        assert naive_covariance(pts) == direct
        cut = rng.randint(0, n)
        a, b = RunningCovariance(d), RunningCovariance(d)
        for p in pts[:cut]:
            a.add(p)
        for p in pts[cut:]:
            b.add(p)
        merged = a.merge(b)
        assert merged.n == n
        assert merged.mean == w.mean
        assert merged.covariance() == direct


def test_symmetric_psd_and_rank() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n, d = rng.randint(2, 7), rng.randint(1, 5)
        s = two_pass_covariance(rand_points(rng, n, d))
        assert all(s[a][b] == s[b][a] for a in range(d) for b in range(d))
        for _ in range(5):
            v = [F(rng.randint(-5, 5)) for _ in range(d)]
            q = sum(v[a] * s[a][b] * v[b] for a in range(d) for b in range(d))
            assert q >= 0
        assert exact_rank(s) <= min(d, n - 1)


def test_cancellation_pitfall() -> None:
    pts = [[1e9 + v] for v in (4.0, 7.0, 13.0, 16.0)]
    assert two_pass_covariance(pts)[0][0] == 30.0
    w = RunningCovariance(1)
    for p in pts:
        w.add(p)
    assert abs(w.covariance()[0][0] - 30.0) < 1e-6
    assert abs(naive_covariance(pts)[0][0] - 30.0) > 1.0


def test_edge_cases() -> None:
    one = RunningCovariance(2)
    one.add([F(3), F(4)])
    assert one.m == [[0, 0], [0, 0]]
    assert one.merge(RunningCovariance(2)).m == [[0, 0], [0, 0]]
    assert RunningCovariance(2).merge(one).mean == [3, 4]
    same = [[F(1), F(2)]] * 5
    assert two_pass_covariance(same) == [[0, 0], [0, 0]]
