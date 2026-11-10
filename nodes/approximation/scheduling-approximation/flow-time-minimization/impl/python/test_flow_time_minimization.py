# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flow-time-minimization/. The authors are listed in prov/FGZ81Z.jsonl.

import itertools
import random

import pytest

from flow_time_minimization import fifo_max_flow, flows_of_order, srpt_flow


def best_preemptive(p, r, w, objective="sum"):
    """Optimum of 1|r_j,pmtn| sum w_j F_j (or max F_j) for integer data, by a DP over unit time slots."""
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
                done = w[j] * (t + 1 - r[j]) if nr[j] == 0 else 0
                rest = f(t + 1, tuple(nr))
                v = done + rest if objective == "sum" else max(done, rest)
                if best is None or v < best:
                    best = v
        memo[key] = best
        return best

    return f(0, tuple(p))


def best_nonpreemptive_sum(p, r):
    return min(sum(flows_of_order(p, r, o)) for o in itertools.permutations(range(len(p))))


def test_page_example() -> None:
    p, r = [5, 1, 2, 4, 1], [0, 1, 2, 3, 8]
    comp, total = srpt_flow(p, r)
    assert comp == [8, 2, 4, 13, 9] and total == 22 == best_preemptive(p, r, [1] * 5)
    assert best_nonpreemptive_sum(p, r) == 23
    assert sum(flows_of_order(p, r, [1, 2, 0, 4, 3])) == 25  # the SRPT conversion
    assert sum(flows_of_order(p, r, [0, 1, 2, 3, 4])) == 30  # FIFO
    order, fmax = fifo_max_flow(p, r)
    assert fmax == 9 == best_preemptive(p, r, [1] * 5, "max")


def test_weighted_counterexample() -> None:
    p, r, w = [2, 1], [0, 0], [10, 1]
    comp, _ = srpt_flow(p, r)
    assert sum(w[j] * (comp[j] - r[j]) for j in range(2)) == 31
    assert best_preemptive(p, r, w) == 23


def test_srpt_is_optimal_with_preemption() -> None:
    rng = random.Random(91)
    for _ in range(150):
        n = rng.randint(1, 4)
        p = [rng.randint(1, 3) for _ in range(n)]
        r = [rng.randint(0, 5) for _ in range(n)]
        comp, total = srpt_flow(p, r)
        assert all(comp[j] - p[j] >= r[j] for j in range(n))
        assert total == best_preemptive(p, r, [1] * n)
        assert total <= best_nonpreemptive_sum(p, r)


def test_fifo_is_optimal_for_maximum_flow() -> None:
    rng = random.Random(92)
    for _ in range(200):
        n = rng.randint(1, 6)
        p = [rng.randint(0, 6) for _ in range(n)]
        r = [rng.randint(0, 12) for _ in range(n)]
        _, fmax = fifo_max_flow(p, r)
        brute = min(max(flows_of_order(p, r, o)) for o in itertools.permutations(range(n)))
        assert fmax == brute
    for _ in range(80):
        n = rng.randint(1, 4)
        p = [rng.randint(1, 3) for _ in range(n)]
        r = [rng.randint(0, 5) for _ in range(n)]
        assert fifo_max_flow(p, r)[1] == best_preemptive(p, r, [1] * n, "max")


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        srpt_flow([1, 2], [0])
    with pytest.raises(ValueError):
        srpt_flow([-1], [0])
