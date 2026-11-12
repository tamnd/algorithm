# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/load-shedding/. The authors are listed in prov/Q0Y7AN.jsonl.

import math
import random

from load_shedding import Policy, Request, gradient_update, no_shed_useful, periodic, simulate


def brute_force_on_time(arrivals: list[int], service: int, timeout: int) -> int:
    """The best offline schedule: try every subset, served in arrival order
    (an exchange argument shows that order is enough), each as early as possible."""
    n = len(arrivals)
    best = 0
    for mask in range(1 << n):
        t, count, ok = 0, 0, True
        for j in range(n):
            if mask >> j & 1:
                start = max(t, arrivals[j])
                if start + service > arrivals[j] + timeout:
                    ok = False
                    break
                t, count = start + service, count + 1
        if ok:
            best = max(best, count)
    return best


def random_requests(rng: random.Random, horizon: int, per_tick: float, classes: int) -> list[Request]:
    out = []
    for t in range(horizon + 1):
        for _ in range(4):
            if rng.random() < per_tick / 4:
                out.append(Request(len(out), t, rng.randrange(classes)))
    return out


def test_collapse_without_shedding():
    # Theorem 1: the k-th response takes s + k(s - p), so only a finite number are useful.
    for s in range(2, 7):
        for p in range(1, s):
            for timeout in range(1, 40):
                horizon = 400
                res = simulate(periodic(p, horizon), s, Policy(), horizon)
                assert res.goodput(timeout) == no_shed_useful(s, p, timeout)
                for k, (_, a, e) in enumerate(res.completed):
                    assert e - a == s + k * (s - p)


def test_fifo_drop_is_optimal_offline():
    # Theorem 2: FIFO with drop at wait > T - s matches the brute-force optimum.
    rng = random.Random(5)
    for _ in range(300):
        s = rng.randint(1, 4)
        timeout = rng.randint(s, 3 * s + 3)
        arrivals = sorted(rng.randrange(0, 12) for _ in range(rng.randint(1, 9)))
        reqs = [Request(k, a) for k, a in enumerate(arrivals)]
        horizon = max(arrivals) + timeout + s + 2
        res = simulate(reqs, s, Policy(max_wait=timeout - s), horizon)
        assert res.late(timeout) == 0
        assert res.goodput(timeout) == brute_force_on_time(arrivals, s, timeout)


def test_shedding_keeps_server_busy_under_periodic_overload():
    # Corollary: with p <= s and T - s >= p - 1 the server never idles and every response is useful.
    for s in range(2, 7):
        for p in range(1, s + 1):
            for timeout in range(s + p - 1, s + 30):
                horizon = 300
                res = simulate(periodic(p, horizon), s, Policy(max_wait=timeout - s), horizon)
                assert res.busy_ticks == horizon + 1
                assert len(res.completed) == horizon // s
                assert res.late(timeout) == 0


def test_worked_example():
    s, p, timeout, horizon = 4, 2, 20, 100
    reqs = periodic(p, horizon)
    none = simulate(reqs, s, Policy(), horizon)
    assert (len(reqs), len(none.completed), none.goodput(timeout)) == (51, 25, 9)
    assert max(e - a for _, a, e in none.completed) == 52
    fifo = simulate(reqs, s, Policy(max_wait=timeout - s), horizon)
    assert (fifo.goodput(timeout), len(fifo.dropped)) == (25, 17)
    assert fifo.dropped[:3] == [9, 11, 13]
    assert max(e - a for _, a, e in fifo.completed) == 20
    lifo = simulate(reqs, s, Policy(lifo=True, max_wait=timeout - s), horizon)
    assert lifo.goodput(timeout) == 25
    assert {e - a for _, a, e in lifo.completed} == {4}
    lim = simulate(reqs, s, Policy(limit=5), horizon)
    assert (lim.goodput(timeout), len(lim.rejected)) == (25, 21)


def test_concurrency_limit_bounds_latency():
    # With FIFO and at most L outstanding, every admitted request ends within L * s.
    rng = random.Random(11)
    for _ in range(60):
        s = rng.randint(1, 5)
        limit = rng.randint(1, 8)
        reqs = random_requests(rng, 300, rng.uniform(0.1, 1.5), 1)
        res = simulate(reqs, s, Policy(limit=limit), 300)
        assert all(e - a <= limit * s for _, a, e in res.completed)
        assert len(res.completed) + len(res.rejected) <= len(reqs)


def test_priority_eviction_order():
    # A request is never shed while a request of a lower class waits.
    rng = random.Random(3)
    for _ in range(40):
        reqs = random_requests(rng, 200, 1.0, 3)
        cap = rng.randint(1, 6)
        res = simulate(reqs, 3, Policy(capacity=cap), 200)
        prio = {r.rid: r.priority for r in reqs}
        done = {rid for rid, _, _ in res.completed}
        shed = set(res.rejected) | set(res.dropped)
        assert done.isdisjoint(shed)
        assert len(res.evictions) == len(shed)
        assert all(gone <= kept for gone, kept in res.evictions)
        served_by_class = [sum(1 for x in done if prio[x] == c) for c in range(3)]
        assert served_by_class[2] >= served_by_class[0]


def test_priority_eviction_invariant_direct():
    # Check the eviction rule step by step on a full queue.
    reqs = [Request(0, 0, 1), Request(1, 0, 0), Request(2, 0, 2), Request(3, 0, 0), Request(4, 0, 1)]
    res = simulate(reqs, 10, Policy(capacity=2), 0)
    # All five arrive before the server starts: 1 is evicted for 2, then 3 and 4 are refused.
    assert (res.dropped, res.rejected) == ([1], [3, 4])
    assert res.evictions == [(0, 1), (0, 1), (1, 1)]
    reqs = [Request(0, 0, 2), Request(1, 0, 2), Request(2, 0, 2), Request(3, 0, 2)]
    res = simulate(reqs, 10, Policy(capacity=2), 0)
    assert res.rejected == [2, 3]  # all equal: the newest arrival is refused


def test_codel_timeout_switch():
    # After the queue has been busy for more than n ticks, no request waits more than m.
    rng = random.Random(7)
    reqs = random_requests(rng, 1000, 0.5, 1)
    m, n = 4, 20
    res = simulate(reqs, 4, Policy(codel=(m, n)), 1000)
    starts = {rid: e - 4 for rid, _, e in res.completed}
    arrival = {r.rid: r.arrival for r in reqs}
    assert all(starts[r] - arrival[r] <= n for r in starts)
    over = sum(1 for r in starts if starts[r] - arrival[r] > m)
    assert over < len(starts)


def test_gradient_rule():
    assert math.isclose(gradient_update(16, 10, 10, 0.0, 1, 1000), 20.0)
    assert math.isclose(gradient_update(16, 10, 20, 0.0, 1, 1000), 12.0)
    assert gradient_update(4, 10, 100, 0.0, 1, 1000) == 2.4
    assert gradient_update(1, 10, 1000, 0.0, 1, 1000) == 1.01
    assert gradient_update(1000, 10, 10, 0.5, 1, 1000) == 1000


def test_gradient_limit_settles_and_keeps_goodput():
    s, p, timeout, horizon = 4, 2, 20, 2000
    reqs = periodic(p, horizon)
    for start in (1, 10, 50):
        res = simulate(reqs, s, Policy(limit=start, gradient=(5, 0.25), max_limit=100), horizon)
        assert res.busy_ticks == horizon + 1
        assert all(2.5 < x < 4 for x in res.limits[-200:])
        assert res.goodput(timeout) >= 0.95 * len(res.completed)
