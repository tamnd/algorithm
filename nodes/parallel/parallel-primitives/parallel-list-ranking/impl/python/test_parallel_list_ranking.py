# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-list-ranking/. The authors are listed in prov/PJYJ60.jsonl.

import math
import random

from parallel_list_ranking import Cost, ceil_log2, random_mate_rank


def random_lists(n: int, k: int, rng: random.Random) -> list[int | None]:
    """A set of at most k disjoint lists on the nodes 0..n-1, in a random order."""
    order = list(range(n))
    rng.shuffle(order)
    cuts = set(rng.sample(range(1, n), min(k - 1, n - 1))) if n > 1 else set()
    nxt: list[int | None] = [None] * n
    for t in range(n - 1):
        if t + 1 not in cuts:
            nxt[order[t]] = order[t + 1]
    return nxt


def walk_rank(nxt: list[int | None]) -> list[int]:
    """Sequential reference: walk each list from its head, then count back."""
    n = len(nxt)
    has_pred = [False] * n
    for j in nxt:
        if j is not None:
            has_pred[j] = True
    rank = [0] * n
    for h in range(n):
        if not has_pred[h]:
            path = []
            v: int | None = h
            while v is not None:
                path.append(v)
                v = nxt[v]
            for d, v in enumerate(reversed(path)):
                rank[v] = d
    return rank


def span_bound(n: int, rounds: int) -> int:
    """The span charged by the code is at most this, for any coin flips (see the page)."""
    lg = ceil_log2(n)
    return 2 * (lg + 1) + rounds * (8 * lg + 6)


def test_example() -> None:
    nxt = [6, 7, 5, 0, None, 1, 2, 4]
    for seed in range(20):
        assert random_mate_rank(nxt, random.Random(seed)) == [6, 2, 4, 7, 0, 3, 5, 1]


def test_edges() -> None:
    rng = random.Random(0)
    assert random_mate_rank([], rng) == []
    assert random_mate_rank([None], rng) == [0]
    assert random_mate_rank([None, None], rng) == [0, 0]
    assert random_mate_rank([1, None], rng) == [1, 0]
    assert random_mate_rank([None, 0], rng) == [0, 1]


def test_random_against_walk() -> None:
    rng = random.Random(1990)
    for _ in range(600):
        n = rng.choice([0, 1, 2, 3, 4, 5, 7, 8, 9, 16, 31, 32, 33, 64, 100])
        nxt = random_lists(n, rng.randint(1, 5), rng)
        expect = walk_rank(nxt)
        for _ in range(3):  # the result must not depend on the coins
            cost = Cost()
            assert random_mate_rank(nxt, rng, cost) == expect
            assert cost.span <= span_bound(n, cost.rounds)


def test_rounds_and_work() -> None:
    # E[rounds] <= log_{4/3} n + 5 = 2.41 log2 n + 5, and E[work] <= 28 n
    rng = random.Random(7)
    c = 1 / math.log2(4 / 3)
    for n in [2, 8, 64, 128, 1000, 4096]:
        trials = 30 if n <= 1000 else 6
        rounds, work = 0, 0
        for _ in range(trials):
            cost = Cost()
            random_mate_rank(random_lists(n, 1, rng), rng, cost)
            rounds += cost.rounds
            work += cost.work
        assert rounds / trials <= c * math.log2(n) + 5
        # the bound 28 n on the mean is almost tight, so the sample mean gets 5 percent slack
        assert work / trials <= 28 * n * 1.05


def test_rounds_high_probability() -> None:
    # Pr[rounds > (k + 1) log_{4/3} n] <= n^{-k}; with k = 2 and n = 256 the chance that
    # one of 200 runs exceeds it is at most 200 / 65536
    rng = random.Random(8)
    n = 256
    limit = 3 * math.log(n, 4 / 3)
    for _ in range(200):
        cost = Cost()
        random_mate_rank(random_lists(n, 1, rng), rng, cost)
        assert cost.rounds <= limit
