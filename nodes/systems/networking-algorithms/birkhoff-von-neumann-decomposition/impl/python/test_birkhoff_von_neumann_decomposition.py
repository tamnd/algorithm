# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birkhoff-von-neumann-decomposition/. The authors are listed in prov/YCNDFQ.jsonl.

import itertools
import random
from fractions import Fraction as F

from birkhoff_von_neumann_decomposition import (
    complete_substochastic,
    decompose,
    frame_schedule,
    is_doubly_stochastic,
    recompose,
)


def random_doubly_stochastic(n: int, k: int, rng: random.Random) -> list[list[F]]:
    weights = [rng.randrange(1, 20) for _ in range(k)]
    total = sum(weights)
    m = [[F(0)] * n for _ in range(n)]
    for w in weights:
        perm = list(range(n))
        rng.shuffle(perm)
        for i, j in enumerate(perm):
            m[i][j] += F(w, total)
    return m


def solve_nonnegative(perms: list[tuple[int, ...]], m: list[list[F]]) -> bool:
    """Is m a convex combination of these permutation matrices? (Gaussian elimination.)"""
    n = len(m)
    k = len(perms)
    rows = []
    for i in range(n):
        for j in range(n):
            rows.append([F(int(p[i] == j)) for p in perms] + [m[i][j]])
    piv_cols = []
    r = 0
    for c in range(k):
        p = next((x for x in range(r, len(rows)) if rows[x][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [x / rows[r][c] for x in rows[r]]
        for x in range(len(rows)):
            if x != r and rows[x][c] != 0:
                f = rows[x][c]
                rows[x] = [a - f * b for a, b in zip(rows[x], rows[r])]
        piv_cols.append(c)
        r += 1
    if any(all(x == 0 for x in row[:k]) and row[k] != 0 for row in rows):
        return False
    assert len(piv_cols) == k  # these permutation matrices are independent
    return all(rows[t][k] >= 0 for t in range(k))


def test_example_from_the_page() -> None:
    m = [[F(1, 2), F(1, 3), F(1, 6)], [F(1, 6), F(1, 2), F(1, 3)], [F(1, 3), F(1, 6), F(1, 2)]]
    terms = decompose(m)
    assert terms == [(F(1, 2), [0, 1, 2]), (F(1, 3), [1, 2, 0]), (F(1, 6), [2, 0, 1])]


def test_random_matrices_recompose_exactly_and_respect_the_bound() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randrange(1, 8)
        m = random_doubly_stochastic(n, rng.randrange(1, 3 * n * n), rng)
        assert is_doubly_stochastic(m)
        terms = decompose(m)
        assert all(w > 0 for w, _ in terms)
        assert sum(w for w, _ in terms) == 1
        assert recompose(terms, n) == m
        assert len(terms) <= (n - 1) ** 2 + 1
        assert all(sorted(p) == list(range(n)) for _, p in terms)


def test_n3_generic_matrix_needs_five_permutations() -> None:
    perms = list(itertools.permutations(range(3)))
    m = [[F(0)] * 3 for _ in range(3)]
    for w, p in zip(range(1, 7), perms):
        for i, j in enumerate(p):
            m[i][j] += F(w, 21)
    assert is_doubly_stochastic(m)
    assert not any(solve_nonnegative(list(s), m) for s in itertools.combinations(perms, 4))
    assert any(solve_nonnegative(list(s), m) for s in itertools.combinations(perms, 5))
    assert len(decompose(m)) == 5


def test_complete_substochastic() -> None:
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randrange(1, 7)
        full = random_doubly_stochastic(n, n * n, rng)
        m = [[x * F(rng.randrange(0, 4), 3) for x in row] for row in full]
        m = [[min(x, F(1)) for x in row] for row in m]
        # Scale down so that row and column sums are at most 1.
        s = max([sum(r) for r in m] + [sum(m[i][j] for i in range(n)) for j in range(n)] + [F(1)])
        m = [[x / s for x in row] for row in m]
        a = complete_substochastic(m)
        assert is_doubly_stochastic(a)
        assert all(a[i][j] >= m[i][j] for i in range(n) for j in range(n))
        changed = sum(1 for i in range(n) for j in range(n) if a[i][j] != m[i][j])
        assert changed <= 2 * n - 1


def test_frame_schedule_serves_every_rate() -> None:
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randrange(1, 6)
        frame = rng.randrange(1, 12)
        k = [[0] * n for _ in range(n)]
        for _ in range(n * frame):
            i, j = rng.randrange(n), rng.randrange(n)
            if sum(k[i]) < frame and sum(k[x][j] for x in range(n)) < frame:
                k[i][j] += 1
        slots = frame_schedule(k, frame)
        assert len(slots) == frame
        for i in range(n):
            for j in range(n):
                assert sum(1 for p in slots if p[i] == j) >= k[i][j]
