# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-completion-time-scheduling/. The authors are listed in prov/Y1GCMZ.jsonl.

import itertools
import math
import random

from weighted_completion_time_scheduling import (
    srpt,
    srpt_conversion,
    weighted_sum,
    wspt_list,
    wspt_order,
)


def best_one_machine(p, w, r=None):
    return min(weighted_sum(p, w, o, r) for o in itertools.permutations(range(len(p))))


def best_parallel(p, w, m):
    # each machine runs its jobs in WSPT order, which is optimal for a fixed assignment
    n = len(p)
    rank = {j: i for i, j in enumerate(wspt_order(p, w))}
    best = None
    for assign in itertools.product(range(m), repeat=n):
        s = 0
        for i in range(m):
            jobs = [j for j in range(n) if assign[j] == i]
            s += weighted_sum(p, w, sorted(jobs, key=rank.get))
        if best is None or s < best:
            best = s
    return best


def best_preemptive_total(p, r):
    """Optimum of 1|r_j,pmtn|sum C_j for integer data, by a DP over unit time slots."""
    n = len(p)
    memo = {}

    def f(t, rem):
        if not any(rem):
            return 0
        key = (t, rem)
        if key in memo:
            return memo[key]
        avail = [j for j in range(n) if rem[j] > 0 and r[j] <= t]
        if not avail:
            best = f(t + 1, rem)
        else:
            best = None
            for j in avail:
                nr = list(rem)
                nr[j] -= 1
                v = f(t + 1, tuple(nr)) + (t + 1 if nr[j] == 0 else 0)
                if best is None or v < best:
                    best = v
        memo[key] = best
        return best

    return f(0, tuple(p))


def test_page_example() -> None:
    p = [5, 1, 2, 4, 1]
    r = [0, 1, 2, 3, 8]
    assert srpt(p, r) == [8, 2, 4, 13, 9]
    assert sum(srpt(p, r)) == 36 == best_preemptive_total(p, r)
    order, comp, total = srpt_conversion(p, r)
    assert order == [1, 2, 0, 4, 3] and comp == [9, 2, 4, 14, 10] and total == 39
    ones = [1] * 5
    assert best_one_machine(p, ones, r) == 37 == weighted_sum(p, ones, [1, 2, 3, 4, 0], r)
    assert weighted_sum(p, ones, [0, 1, 2, 3, 4], r) == 44


def test_smith_rule_is_optimal() -> None:
    rng = random.Random(81)
    for _ in range(300):
        n = rng.randint(1, 7)
        p = [rng.randint(0, 9) for _ in range(n)]
        w = [rng.randint(0, 9) for _ in range(n)]
        assert weighted_sum(p, w, wspt_order(p, w)) == best_one_machine(p, w)


def test_srpt_is_optimal_with_preemption() -> None:
    rng = random.Random(82)
    for _ in range(150):
        n = rng.randint(1, 4)
        p = [rng.randint(1, 3) for _ in range(n)]
        r = [rng.randint(0, 5) for _ in range(n)]
        assert sum(srpt(p, r)) == best_preemptive_total(p, r)


def test_conversion_is_a_2_approximation() -> None:
    rng = random.Random(83)
    for _ in range(300):
        n = rng.randint(1, 7)
        p = [rng.randint(0, 9) for _ in range(n)]
        r = [rng.randint(0, 20) for _ in range(n)]
        order, comp, total = srpt_conversion(p, r)
        cp = srpt(p, r)
        assert all(comp[j] <= 2 * cp[j] for j in range(n))
        assert all(comp[j] - p[j] >= r[j] for j in range(n))
        opt = best_one_machine(p, [1] * n, r)
        assert sum(cp) <= opt <= total <= 2 * opt


def test_wspt_list_on_parallel_machines() -> None:
    rng = random.Random(84)
    bound = (1 + math.sqrt(2)) / 2
    for _ in range(150):
        m = rng.randint(2, 3)
        n = rng.randint(1, 7)
        p = [rng.randint(1, 9) for _ in range(n)]
        w = [rng.randint(1, 9) for _ in range(n)]
        machines, total = wspt_list(p, w, m)
        assert sorted(j for mach in machines for j in mach) == list(range(n))
        opt = best_parallel(p, w, m)
        assert opt <= total <= bound * opt + 1e-9


def test_spt_list_is_optimal_for_unit_weights() -> None:
    rng = random.Random(85)
    for _ in range(150):
        m = rng.randint(2, 3)
        n = rng.randint(1, 7)
        p = [rng.randint(1, 9) for _ in range(n)]
        assert wspt_list(p, [1] * n, m)[1] == best_parallel(p, [1] * n, m)
