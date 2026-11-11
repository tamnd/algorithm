# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cole-vishkin/. The authors are listed in prov/PCJE4Q.jsonl.

import random

from cole_vishkin import cole_vishkin_ring, cole_vishkin_tree, cv_value, lg_ceil, log_star, steps


def ring(n: int) -> list[int]:
    return [(v + 1) % n for v in range(n)]


def test_step_is_proper_brute_force() -> None:
    # If c != d and d != e, the new colours of the two adjacent nodes differ.
    for c in range(64):
        for d in range(64):
            if c == d:
                continue
            assert cv_value(c, d) < 2 * lg_ceil(64)
            for e in range(64):
                if e != d:
                    assert cv_value(c, d) != cv_value(d, e)


def test_steps_and_log_star() -> None:
    assert [steps(N) for N in (1, 6, 7, 8, 16, 17, 256, 2**16)] == [0, 0, 1, 1, 2, 3, 3, 4]
    assert steps(2**65536) == 5 and log_star(2**65536) == 5
    for N in range(1, 5000):
        assert steps(N) <= log_star(N)
        assert steps(N) >= log_star(N) - 3
    for k in range(1, 300):
        assert steps(2**k) <= steps(2 ** (k + 1))


def test_rings_exact_rounds() -> None:
    rng = random.Random(1)
    sizes = list(range(3, 40)) + [100, 1000, 10000]
    for n in sizes:
        for N in (n, n * n, 2**64):
            ids = rng.sample(range(N), n) if N < 10**7 else [rng.randrange(N) for _ in range(n)]
            if len(set(ids)) < n:
                continue
            history: list[list[int]] = []
            col, rounds = cole_vishkin_ring(ring(n), ids, N, history)
            assert rounds == steps(N) + 3
            assert rounds <= log_star(N) + 3
            assert set(col) <= {0, 1, 2}
            assert all(col[v] != col[(v + 1) % n] for v in range(n))
            for h in history:
                assert all(h[v] != h[(v + 1) % n] for v in range(n))


def test_ring_range_after_each_step() -> None:
    rng = random.Random(2)
    n, N = 500, 2**40
    ids = rng.sample(range(10**6), n)
    ids = [x * (N // 10**6) for x in ids]
    history: list[list[int]] = []
    cole_vishkin_ring(ring(n), ids, N, history)
    b = N
    for h in history[: steps(N)]:
        b = 2 * lg_ceil(b)
        assert max(h) < b
    assert b == 6


def random_forest(n: int, rng: random.Random) -> list[int]:
    return [-1 if v == 0 or rng.random() < 0.01 else rng.randrange(v) for v in range(n)]


def test_trees() -> None:
    rng = random.Random(3)
    for n in (1, 2, 5, 50, 2000):
        shapes = [random_forest(n, rng), [v - 1 for v in range(n)], [-1] + [0] * (n - 1)]
        for parent in shapes:
            for N in (n, n**3 + 7):
                ids = rng.sample(range(N), n)
                col, rounds = cole_vishkin_tree(parent, ids, N)
                assert rounds == steps(N) + 6
                assert set(col) <= {0, 1, 2}
                assert all(parent[v] < 0 or col[v] != col[parent[v]] for v in range(n))
