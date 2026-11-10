# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-lateness-minimization/. The authors are listed in prov/BNQ857.jsonl.

import itertools
import random

from maximum_lateness_minimization import delivery_value, lateness_value, preemptive_edd, schrage


def best_order(p, r, q):
    return min(delivery_value(p, r, q, o) for o in itertools.permutations(range(len(p))))


def best_preemptive(p, r, d):
    """Exact optimum of 1|r_j,pmtn|Lmax for integer data, by a DP over unit time slots."""
    n = len(p)
    horizon = max(r) + sum(p)
    memo = {}

    def f(t, rem):
        # least max lateness of the jobs that are still unfinished at time t
        if not any(rem):
            return None
        key = (t, rem)
        if key in memo:
            return memo[key]
        best = None
        avail = [j for j in range(n) if rem[j] > 0 and r[j] <= t]
        if not avail or t < horizon:
            if not avail:
                best = f(t + 1, rem)
            for j in avail:
                nr = list(rem)
                nr[j] -= 1
                nr = tuple(nr)
                v = f(t + 1, nr)
                if nr[j] == 0:
                    v = t + 1 - d[j] if v is None else max(v, t + 1 - d[j])
                if best is None or v < best:
                    best = v
        memo[key] = best
        return best

    return f(0, tuple(p))


def test_tight_example() -> None:
    # Job 0 is released first and blocks the urgent job 1.
    p, r, q = [4, 1], [0, 1], [0, 4]
    order, start, value = schrage(p, r, q)
    assert order == [0, 1] and value == 9
    assert best_order(p, r, q) == 6
    # With preemption, job 1 cuts in at time 1. Here L_max = 6 - 4 = 2 as in the best order.
    d = [4 - x for x in q]
    pieces, comp, lmax = preemptive_edd(p, r, d)
    assert pieces == [(0, 0, 1), (1, 1, 2), (0, 2, 5)]
    assert lmax == 2 == best_preemptive(p, r, d)


def test_page_example() -> None:
    p = [4, 2, 2, 1, 2]
    r = [0, 1, 1, 2, 3]
    d = [10, 2, 8, 9, 7]
    K = max(d)
    q = [K - x for x in d]
    assert q == [0, 8, 2, 1, 3]
    order, start, value = schrage(p, r, q)
    assert order == [0, 1, 4, 2, 3] and start == [0, 4, 8, 10, 6]
    assert value - K == lateness_value(p, r, d, order) == 4
    assert best_order(p, r, q) - K == 2
    assert lateness_value(p, r, d, [1, 2, 3, 4, 0]) == 2
    pieces, comp, lmax = preemptive_edd(p, r, d)
    assert pieces == [(0, 0, 1), (1, 1, 3), (4, 3, 5), (2, 5, 7), (3, 7, 8), (0, 8, 11)]
    assert lmax == 1 == best_preemptive(p, r, d)


def test_schrage_ratio_against_brute_force() -> None:
    rng = random.Random(41)
    for _ in range(300):
        n = rng.randint(1, 6)
        p = [rng.randint(0, 8) for _ in range(n)]
        r = [rng.randint(0, 15) for _ in range(n)]
        q = [rng.randint(0, 15) for _ in range(n)]
        order, start, value = schrage(p, r, q)
        assert sorted(order) == list(range(n))
        assert all(start[j] >= r[j] for j in range(n))
        assert value == delivery_value(p, r, q, order)
        opt = best_order(p, r, q)
        assert opt <= value <= opt + max(p)
        assert value <= 2 * opt


def test_schrage_exact_without_release_dates() -> None:
    # With all r_j = 0 the rule is EDD in delivery form, which is optimal.
    rng = random.Random(42)
    for _ in range(200):
        n = rng.randint(1, 6)
        p = [rng.randint(0, 8) for _ in range(n)]
        q = [rng.randint(0, 15) for _ in range(n)]
        assert schrage(p, [0] * n, q)[2] == best_order(p, [0] * n, q)


def test_preemptive_edd_against_slot_dp() -> None:
    rng = random.Random(43)
    for _ in range(150):
        n = rng.randint(1, 4)
        p = [rng.randint(1, 3) for _ in range(n)]
        r = [rng.randint(0, 5) for _ in range(n)]
        d = [rng.randint(-2, 14) for _ in range(n)]
        pieces, comp, lmax = preemptive_edd(p, r, d)
        done = [0] * n
        last = 0
        for j, a, b in pieces:
            assert a >= last and a >= r[j] and b > a
            last = b
            done[j] += b - a
        assert done == p
        assert lmax == best_preemptive(p, r, d)
        # never worse than any non-preemptive order
        assert lmax <= min(lateness_value(p, r, d, o) for o in itertools.permutations(range(n)))


def test_edges() -> None:
    assert schrage([], [], []) == ([], [], 0)
    assert preemptive_edd([], [], [])[2] is None
    assert schrage([3], [5], [2]) == ([0], [5], 10)
