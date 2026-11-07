# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alphatensor/. The authors are listed in prov/1MB9PX.jsonl.

import random

import pytest

from alphatensor import (
    STRASSEN,
    alphatensor,
    flip_graph_search,
    matmul_tensor,
    multiply_with,
    rank_upper_bound,
    replay,
    verify,
)


def schoolbook(a, b, cols, mod=None):
    n, m = len(a), len(b)
    c = [[0] * cols for _ in range(n)]
    for i in range(n):
        for j in range(cols):
            s = 0
            for k in range(m):
                s += a[i][k] * b[k][j]
            c[i][j] = s % mod if mod is not None else s
    return c


def rand(rng, r, c, lo=-9, hi=9):
    return [[rng.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def standard(n, m, p):
    out = []
    for i in range(n):
        for j in range(m):
            for k in range(p):
                u = [[int((x, y) == (i, j)) for y in range(m)] for x in range(n)]
                v = [[int((x, y) == (j, k)) for y in range(p)] for x in range(m)]
                w = [[int((x, y) == (i, k)) for y in range(p)] for x in range(n)]
                out.append((u, v, w))
    return out


def test_tensor_shape() -> None:
    t = matmul_tensor(2, 3, 4)
    assert len(t) == 6 and len(t[0]) == 12 and len(t[0][0]) == 8
    assert sum(x for plane in t for row in plane for x in row) == 24
    assert matmul_tensor(0, 3, 3) == []


def test_strassen_game_over_z() -> None:
    factors, reward = alphatensor(matmul_tensor(2, 2, 2), replay(STRASSEN), limit=7)
    assert reward == -7 and len(factors) == 7
    assert verify(STRASSEN, 2, 2, 2)
    for mod in (2, 3, 5, 7):
        assert verify(STRASSEN, 2, 2, 2, mod)
        assert alphatensor(matmul_tensor(2, 2, 2), replay(STRASSEN), 7, mod)[1] == -7


def test_standard_scheme_and_limit_penalty() -> None:
    std = standard(2, 2, 2)
    assert alphatensor(matmul_tensor(2, 2, 2), replay(std), 8)[1] == -8
    # Stop after 5 of the 8 moves: 3 rank-one terms remain, and gamma bounds their rank.
    factors, reward = alphatensor(matmul_tensor(2, 2, 2), replay(std), 5)
    assert factors is None and reward == -5 - 3
    # The empty game on <2,2,2>: gamma is the sum of slice ranks, 4 slices of rank 2.
    assert alphatensor(matmul_tensor(2, 2, 2), replay([]), 0) == (None, -8)
    assert rank_upper_bound(matmul_tensor(3, 3, 3)) == 27


def test_bad_moves() -> None:
    bad = [([[3, 0], [0, 0]], [[1, 0], [0, 0]], [[1, 0], [0, 0]])]
    with pytest.raises(ValueError):
        alphatensor(matmul_tensor(2, 2, 2), replay(bad), 1)
    with pytest.raises(ValueError):
        alphatensor(matmul_tensor(2, 2, 2), replay([([[1]], [[1]], [[1]])]), 1)


def test_gf2_only_scheme() -> None:
    """Strassen with every sign dropped is valid over GF(2) but not over Z or Z/3."""
    unsigned = [tuple([[abs(x) for x in row] for row in f] for f in t) for t in STRASSEN]
    assert verify(unsigned, 2, 2, 2, 2)
    assert not verify(unsigned, 2, 2, 2)
    assert not verify(unsigned, 2, 2, 2, 3)
    a, b = [[1, 2], [3, 4]], [[5, 6], [7, 8]]
    assert multiply_with(unsigned, (2, 2, 2), a, b, 2, mod=2) == schoolbook(a, b, 2, 2)
    assert multiply_with(unsigned, (2, 2, 2), a, b, 2) != schoolbook(a, b, 2)


def test_flip_graph_finds_rank_7() -> None:
    for seed in range(4):
        found = flip_graph_search(2, 2, 2, 7, seed)
        assert found is not None and len(found) == 7
        assert verify(found, 2, 2, 2, 2)
        factors, reward = alphatensor(matmul_tensor(2, 2, 2), replay(found), 7, mod=2, coeffs=(0, 1))
        assert reward == -7
    found = flip_graph_search(2, 2, 3, 11, 1)
    assert found is not None and verify(found, 2, 2, 3, 2)
    assert flip_graph_search(2, 2, 2, 6, 0, max_steps=300) is None


def test_multiply_random_over_z() -> None:
    rng = random.Random(1)
    for _ in range(300):
        r, s, c = rng.randint(0, 9), rng.randint(0, 9), rng.randint(0, 9)
        a, b = rand(rng, r, s), rand(rng, s, c)
        assert multiply_with(STRASSEN, (2, 2, 2), a, b, c) == schoolbook(a, b, c)


@pytest.mark.parametrize("mod", [2, 3, 5, 7])
def test_multiply_random_mod(mod: int) -> None:
    rng = random.Random(100 + mod)
    for _ in range(60):
        r, s, c = rng.randint(1, 8), rng.randint(1, 8), rng.randint(1, 8)
        a, b = rand(rng, r, s, 0, mod - 1), rand(rng, s, c, 0, mod - 1)
        assert multiply_with(STRASSEN, (2, 2, 2), a, b, c, mod) == schoolbook(a, b, c, mod)


def test_multiply_gf2_found_scheme() -> None:
    found = flip_graph_search(2, 2, 2, 7, 3)
    rng = random.Random(9)
    for _ in range(100):
        r, s, c = rng.randint(0, 9), rng.randint(0, 9), rng.randint(0, 9)
        a, b = rand(rng, r, s, 0, 1), rand(rng, s, c, 0, 1)
        assert multiply_with(found, (2, 2, 2), a, b, c, 2) == schoolbook(a, b, c, 2)


def test_edge_matrices() -> None:
    assert multiply_with(STRASSEN, (2, 2, 2), [], [], 0) == []
    assert multiply_with(STRASSEN, (2, 2, 2), [[]], [], 3) == [[0, 0, 0]]
    assert multiply_with(STRASSEN, (2, 2, 2), [[4]], [[-5]], 1) == [[-20]]
    n = 7
    eye = [[int(i == j) for j in range(n)] for i in range(n)]
    zero = [[0] * n for _ in range(n)]
    a = rand(random.Random(5), n, n)
    assert multiply_with(STRASSEN, (2, 2, 2), a, eye, n) == a
    assert multiply_with(STRASSEN, (2, 2, 2), eye, a, n) == a
    assert multiply_with(STRASSEN, (2, 2, 2), a, zero, n) == zero
    big = rand(random.Random(6), 17, 17)
    assert multiply_with(STRASSEN, (2, 2, 2), big, big, 17, cutoff=4) == schoolbook(big, big, 17)


def test_rectangular_scheme() -> None:
    std = standard(1, 2, 3)
    assert verify(std, 1, 2, 3)
    rng = random.Random(4)
    for _ in range(40):
        r, s, c = rng.randint(0, 6), rng.randint(0, 6), rng.randint(0, 6)
        a, b = rand(rng, r, s), rand(rng, s, c)
        assert multiply_with(std, (1, 2, 3), a, b, c) == schoolbook(a, b, c)


def test_example_scheme_seed_1() -> None:
    """The scheme printed in the example section."""
    found = flip_graph_search(2, 2, 2, 7, 1)
    assert found == [
        ([[0, 0], [1, 0]], [[1, 0], [0, 0]], [[0, 0], [1, 1]]),
        ([[0, 1], [0, 1]], [[1, 1], [1, 1]], [[1, 0], [0, 0]]),
        ([[1, 1], [0, 0]], [[0, 0], [0, 1]], [[0, 1], [0, 1]]),
        ([[0, 0], [0, 1]], [[0, 0], [1, 0]], [[1, 0], [1, 0]]),
        ([[1, 1], [0, 1]], [[1, 1], [0, 1]], [[1, 0], [0, 1]]),
        ([[1, 1], [1, 1]], [[1, 1], [0, 0]], [[0, 0], [0, 1]]),
        ([[1, 0], [0, 0]], [[0, 1], [0, 1]], [[1, 1], [0, 0]]),
    ]
    assert verify(found, 2, 2, 2, 2) and not verify(found, 2, 2, 2)
