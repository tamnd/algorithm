# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pagerank/. The authors are listed in prov/YEWMFK.jsonl.

import random
from fractions import Fraction

from pagerank import pagerank, ranking


def exact(n: int, arcs: list[tuple[int, int]], alpha: Fraction) -> list[Fraction]:
    """Solve pi = pi P exactly from the definition, by Gauss-Jordan elimination."""
    out = [0] * n
    for u, _ in arcs:
        out[u] += 1
    p = [[Fraction(0)] * n for _ in range(n)]
    for u, v in arcs:
        p[u][v] += alpha / out[u]
    for u in range(n):
        for v in range(n):
            p[u][v] += Fraction(1, n) if out[u] == 0 else (1 - alpha) / n
    # equations: sum_u pi_u (P_uv - [u == v]) = 0 for v < n-1, and sum pi = 1
    a = [[p[u][v] - (1 if u == v else 0) for u in range(n)] for v in range(n)]
    a[n - 1] = [Fraction(1)] * n
    b = [Fraction(0)] * n
    b[n - 1] = Fraction(1)
    for c in range(n):
        r = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[r] = a[r], a[c]
        b[c], b[r] = b[r], b[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
                b[r] -= f * b[c]
    return [b[i] / a[i][i] for i in range(n)]


def test_example() -> None:
    arcs = [(0, 1), (0, 2), (1, 2), (2, 0), (3, 2), (3, 4), (4, 3), (4, 5)]
    x = pagerank(6, arcs, 0.85, 1e-12)
    want = [Fraction(29447, 91988), Fraction(31133, 183976), Fraction(62107, 183976)] + [Fraction(3, 52)] * 3
    assert all(abs(a - float(b)) < 1e-10 for a, b in zip(x, want))
    assert ranking(x) == [2, 0, 1, 3, 4, 5]


def test_edges() -> None:
    assert pagerank(1, []) == [1.0]
    assert abs(sum(pagerank(4, [])) - 1) < 1e-12
    assert all(abs(t - 0.25) < 1e-12 for t in pagerank(4, []))
    # a directed cycle is symmetric: all scores equal
    assert all(abs(t - 0.2) < 1e-9 for t in pagerank(5, [(i, (i + 1) % 5) for i in range(5)]))
    # alpha = 0 gives the uniform vector after one round
    assert all(abs(t - 1 / 3) < 1e-12 for t in pagerank(3, [(0, 1), (1, 2)], alpha=0.0))
    # self-loop and repeated arcs
    x = pagerank(2, [(0, 0), (0, 1), (0, 1)], 0.5, 1e-14)
    e = exact(2, [(0, 0), (0, 1), (0, 1)], Fraction(1, 2))
    assert all(abs(a - float(b)) < 1e-12 for a, b in zip(x, e))


def test_dangling_share_is_kept() -> None:
    x = pagerank(3, [(0, 1), (0, 2)], 0.85, 1e-14)
    assert abs(sum(x) - 1) < 1e-12
    assert x[1] == x[2] and x[1] > x[0]


def test_random_against_exact() -> None:
    rng = random.Random(4127)
    for _ in range(500):
        n = rng.randint(1, 7)
        m = rng.randint(0, 3 * n)
        arcs = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        alpha = rng.choice([Fraction(0), Fraction(1, 2), Fraction(17, 20), Fraction(9, 10)])
        eps = 1e-12
        x = pagerank(n, arcs, float(alpha), eps)
        e = exact(n, arcs, alpha)
        assert sum(e) == 1
        err = sum(abs(a - float(b)) for a, b in zip(x, e))
        bound = float(alpha) * eps / (1 - float(alpha)) + 1e-12
        assert err <= bound
