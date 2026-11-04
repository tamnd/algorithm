# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smawk-algorithm/. The authors are listed in prov/V8AHMD.jsonl.

import random

from smawk_algorithm import row_minima


def leftmost_minima(mat):
    return [row.index(min(row)) for row in mat]


def is_totally_monotone(mat):
    n, m = len(mat), len(mat[0])
    for i in range(n):
        for i2 in range(i + 1, n):
            for j in range(m):
                for j2 in range(j + 1, m):
                    if mat[i][j] > mat[i][j2] and not mat[i2][j] > mat[i2][j2]:
                        return False
    return True


def run(mat):
    count = [0]

    def a(i, j):
        count[0] += 1
        return mat[i][j]

    return row_minima(len(mat), len(mat[0]), a), count[0]


def random_monge(rng, n, m):
    # Sums of Monge terms are Monge: column and row offsets, and f(x_i - y_j) with f convex.
    xs = sorted(rng.randint(0, 20) for _ in range(n))
    ys = sorted(rng.randint(0, 20) for _ in range(m))
    u = [rng.randint(0, 9) for _ in range(m)]
    v = [rng.randint(0, 9) for _ in range(n)]
    return [[(xs[i] - ys[j]) ** 2 + u[j] + v[i] for j in range(m)] for i in range(n)]


def test_example() -> None:
    x, y, u = [1, 2, 4, 5, 7], range(7), [9, 4, 6, 0, 7, 3, 5]
    mat = [[(xi - yj) ** 2 + uj for yj, uj in zip(y, u)] for xi in x]
    assert run(mat)[0] == [1, 3, 3, 5, 6]


def test_edges() -> None:
    assert run([[5]])[0] == [0]
    assert run([[3, 1, 2]])[0] == [1]
    assert run([[2], [1], [7]])[0] == [0, 0, 0]
    assert run([[4, 4, 4], [4, 4, 4]])[0] == [0, 0]
    assert row_minima(0, 3, lambda i, j: 0) == []


def test_ties_take_leftmost() -> None:
    mat = [[1, 1, 2], [3, 0, 0], [5, 2, 2]]
    assert is_totally_monotone(mat)
    assert run(mat)[0] == leftmost_minima(mat)


def test_large_values() -> None:
    big = 1 << 62
    mat = [[big, big - 1, big], [big + 1, big, big - 5]]
    assert is_totally_monotone(mat)
    assert run(mat)[0] == [1, 2]


def test_random_monge_against_brute_force() -> None:
    rng = random.Random(1987)
    for _ in range(800):
        n, m = rng.randint(1, 12), rng.randint(1, 12)
        mat = random_monge(rng, n, m)
        got, reads = run(mat)
        assert got == leftmost_minima(mat)
        assert reads <= 4 * m + 12 * n


def test_random_totally_monotone_small_values() -> None:
    rng = random.Random(42)
    done = 0
    while done < 600:
        n, m = rng.randint(1, 4), rng.randint(1, 4)
        mat = [[rng.randint(0, 3) for _ in range(m)] for _ in range(n)]
        if not is_totally_monotone(mat):
            continue
        done += 1
        assert run(mat)[0] == leftmost_minima(mat)


def test_linear_reads_on_large_input() -> None:
    rng = random.Random(7)
    n, m = 300, 2000
    mat = random_monge(rng, n, m)
    got, reads = run(mat)
    assert got == leftmost_minima(mat)
    assert reads <= 4 * m + 12 * n
