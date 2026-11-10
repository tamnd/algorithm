# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-parallelism/. The authors are listed in prov/271465.jsonl.
import random

from dynamic_parallelism import adaptive_fill, cdp_quicksort, launch_cost


def test_quicksort_sorts_and_counts():
    for seed in range(30):
        rng = random.Random(seed)
        n = rng.randrange(0, 600)
        a = [rng.randrange(0, 50 if seed % 3 == 0 else 10 ** 6) for _ in range(n)]
        out, st = cdp_quicksort(a, random.Random(seed + 100), cutoff=rng.choice([1, 8, 32]))
        assert out == sorted(a)
        assert st.launches == sum(st.per_level.values())
        assert st.launches <= 2 * max(n, 1)


def test_quicksort_worked_example():
    rng = random.Random(1)
    a = [rng.randrange(10 ** 6) for _ in range(1000)]
    out, st = cdp_quicksort(a, random.Random(2), 32)
    assert out == sorted(a)
    assert (st.launches, st.max_depth) == (112, 10)
    # sorted input with the first item as pivot: one level per item above the cutoff
    out, st = cdp_quicksort(list(range(200)), random.Random(0), 32, pivot_rule="first")
    assert out == list(range(200))
    assert (st.launches, st.max_depth) == (168, 168)
    assert st.max_depth > 24


def circ(x, y):
    return min(3, (x * x + y * y) // 4096)


def test_adaptive_fill_is_exact_for_monotone_images():
    rng = random.Random(9)
    for _ in range(20):
        a, b, cap = rng.randrange(1, 40), rng.randrange(1, 40), rng.randrange(1, 6)
        f = lambda x, y, a=a, b=b, cap=cap: min(cap, x // a + y // b)
        img, st = adaptive_fill(f, 64, 4, rng.randrange(0, 5))
        assert all(img[y][x] == f(x, y) for y in range(64) for x in range(64))


def test_adaptive_worked_example():
    rows = []
    for depth in (0, 3, 4, 5):
        img, st = adaptive_fill(circ, 128, 4, depth)
        assert all(img[y][x] == circ(x, y) for y in range(128) for x in range(128))
        rows.append((depth, st.launches, st.evaluations))
    assert rows == [(0, 0, 16384), (3, 68, 12260), (4, 188, 11612), (5, 396, 12620)]
    _, st = adaptive_fill(circ, 128, 4, 4)
    assert dict(st.per_level) == {1: 4, 2: 16, 3: 48, 4: 120}
    assert launch_cost(188, 5) == 940
