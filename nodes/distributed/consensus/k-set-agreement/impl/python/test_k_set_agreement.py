# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-set-agreement/. The authors are listed in prov/16H2HE.jsonl.

from itertools import combinations, product

from k_set_agreement import async_run, flood_min, min_of_first


def views(n: int, f: int):
    """Every choice, for every process, of the n - f senders it hears first (itself included)."""
    per = [[[p] + list(c) for c in combinations([q for q in range(n) if q != p], n - f - 1)] for p in range(n)]
    return product(*per)


def check_async(n: int, f: int, inputs) -> int:
    k = f + 1
    worst = 0
    for values in inputs:
        bound = sorted(values)[f]  # the (f + 1)-th smallest input
        for heard in views(n, f):
            d = [x for x in min_of_first(list(values), [list(h) for h in heard], f) if x is not None]
            assert len(d) == n
            assert all(x in values for x in d)  # validity
            assert all(x <= bound for x in d)  # among the f + 1 smallest inputs
            assert len(set(d)) <= k  # k-agreement
            worst = max(worst, len(set(d)))
    return worst


def test_async_all_views_small() -> None:
    # n = 4, f = 1 and f = 2, all inputs over {0, 1, 2, 3}, every view of every process
    allv = list(product(range(4), repeat=4))
    assert check_async(4, 1, allv) == 2
    assert check_async(4, 2, allv) == 3


def test_async_all_views_n5() -> None:
    # distinct inputs are the worst case; by symmetry the identity assignment covers them
    assert check_async(5, 2, [(0, 1, 2, 3, 4)]) == 3
    assert check_async(5, 3, [(0, 1, 2, 3, 4)]) == 4


def test_async_bound_is_tight_for_f_ge_k() -> None:
    # with f = k = 2 the same algorithm gives f + 1 = 3 values, more than k: it needs f < k
    d = min_of_first([0, 1, 2, 3], [[0, 1], [1, 2], [2, 3], [3, 0]], f=2)
    assert d == [0, 1, 2, 0]


def test_async_runs_with_crashes() -> None:
    n, f = 5, 2
    for seed in range(400):
        crashed = [(seed + i) % n for i in range(seed % (f + 1))]
        crashes = {p: (seed * 7 + p) % n for p in crashed}  # sends before the crash, 0 to 4
        values = [(seed * 31 + 17 * p) % 6 for p in range(n)]
        d = async_run(values, f, seed, crashes)
        for p in range(n):
            if p not in crashes:
                assert d[p] is not None  # termination for correct processes
        dec = [x for x in d if x is not None]
        assert all(x in values for x in dec)
        assert len(set(dec)) <= f + 1
        assert all(x <= sorted(values)[f] for x in dec)


def crash_patterns(n: int, f: int, rounds: int):
    yield {}
    for size in range(1, f + 1):
        for who in combinations(range(n), size):
            opts = []
            for p in who:
                others = [q for q in range(n) if q != p]
                subsets = [frozenset(s) for m in range(len(others) + 1) for s in combinations(others, m)]
                opts.append([(r, s) for r in range(1, rounds + 1) for s in subsets])
            for choice in product(*opts):
                yield dict(zip(who, choice))


def test_flood_min_all_crash_patterns() -> None:
    n, f, k = 5, 2, 2
    count = 0
    for crashes in crash_patterns(n, f, f // k + 1):
        d = flood_min(list(range(n)), f, k, crashes)
        assert len(d) == n - len(crashes)
        assert len(set(d.values())) <= k
        count += 1
    assert count == 1 + 5 * 32 + 10 * 32 * 32


def test_flood_min_one_round_too_few() -> None:
    # floor(f / k) rounds are not enough (CHLT bound): n = 5, f = 2, k = 2, one round
    crashes = {0: (1, frozenset({2})), 1: (1, frozenset({3}))}
    d = flood_min(list(range(5)), 2, 2, crashes, rounds=1)
    assert d == {2: 0, 3: 1, 4: 2}
    bad = sum(len(set(flood_min(list(range(5)), 2, 2, c, rounds=1).values())) > 2
              for c in crash_patterns(5, 2, 1))
    assert bad > 0


def test_flood_min_consensus_case() -> None:
    # k = 1 is consensus and needs f + 1 rounds
    for crashes in crash_patterns(4, 2, 3):
        d = flood_min([3, 1, 2, 0], 2, 1, crashes)
        assert len(set(d.values())) <= 1
