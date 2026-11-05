# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-partitioning-greedy/. The authors are listed in prov/48TJ7A.jsonl.
import itertools
import random

from interval_partitioning_greedy import interval_partitioning_greedy


def meet(a, b, kind):
    if kind == "closed":
        return max(a[0], b[0]) <= min(a[1], b[1])
    return max(a[0], b[0]) < min(a[1], b[1])


def chromatic(intervals, kind):
    """Smallest number of colors for the interval graph, by trying all colorings."""
    n = len(intervals)
    if n == 0:
        return 0
    for k in range(1, n + 1):
        for colors in itertools.product(range(k), repeat=n):
            if all(
                colors[i] != colors[j] or not meet(intervals[i], intervals[j], kind)
                for i in range(n)
                for j in range(i + 1, n)
            ):
                return k
    raise AssertionError("unreachable")


def check(intervals, kind, oracle=True):
    k, res = interval_partitioning_greedy(intervals, kind)
    assert len(res) == len(intervals)
    assert all(1 <= c <= k for c in res)
    assert len(set(res)) == k
    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            if res[i] == res[j]:
                assert not meet(intervals[i], intervals[j], kind)
    if oracle:
        assert k == chromatic(intervals, kind)
    return k, res


EXAMPLE = [(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (8, 9), (7, 10)]


def test_example():
    assert check(EXAMPLE, "closed") == (3, [1, 2, 3, 1, 3, 3, 2])
    assert check(EXAMPLE, "half-open") == (2, [1, 2, 1, 1, 2, 1, 2])
    assert check(EXAMPLE, "open")[0] == 2


def test_touching_cases():
    assert check([(1, 3), (3, 5)], "closed")[0] == 2
    assert check([(1, 3), (3, 5)], "half-open") == (1, [1, 1])
    assert check([(1, 3), (3, 5)], "open") == (1, [1, 1])
    # equal starts
    assert check([(2, 4), (2, 3), (3, 6)], "half-open")[0] == 2
    # point intervals, closed
    assert check([(4, 4), (4, 4), (1, 4)], "closed")[0] == 3
    assert check([(4, 4), (5, 5)], "closed")[0] == 1


def test_edge_cases():
    assert interval_partitioning_greedy([]) == (0, [])
    assert check([(0, 1)], "half-open") == (1, [1])
    assert check([(0, 10)] * 4, "half-open")[0] == 4
    assert check([(i, i + 1) for i in range(6)], "half-open")[0] == 1
    assert check([(i, i + 1) for i in range(6)], "closed")[0] == 2


def test_random_against_brute_force():
    rng = random.Random(487)
    for trial in range(600):
        kind = ("closed", "half-open", "open")[trial % 3]
        n = rng.randint(0, 6)
        ivs = []
        for _ in range(n):
            a = rng.randint(0, 8)
            b = rng.randint(a + (0 if kind == "closed" else 1), 9)
            ivs.append((a, b))
        check(ivs, kind)


def test_random_large_against_depth():
    rng = random.Random(4877)
    for trial in range(200):
        kind = ("closed", "half-open")[trial % 2]
        ivs = []
        for _ in range(rng.randint(1, 60)):
            a = rng.randint(0, 40)
            ivs.append((a, rng.randint(a + (0 if kind == "closed" else 1), 41)))
        k, _ = check(ivs, kind, oracle=False)
        pts = [h / 2 for h in range(0, 84)]
        depth = max(
            sum(1 for a, b in ivs if (a <= x <= b if kind == "closed" else a <= x < b)) for x in pts
        )
        assert k == depth
