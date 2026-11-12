# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/connection-draining/. The authors are listed in prov/T00ABF.jsonl.

import random

from connection_draining import REMOVED, Balancer, goaway_shutdown, simulate


def check_run(lb: Balancer, b: int, drain_at: int, timeout: int, lag: int) -> None:
    deadline = drain_at + timeout
    on_b = {r: v for r, v in lb.assigned.items() if v[0] == b}
    # No new request reaches the draining backend once the balancer knows.
    assert all(start < drain_at + lag for _, start, _ in on_b.values())
    # Requests that end by the deadline finish; the others are cut at it.
    expect_cut = {r for r, (_, _, end) in on_b.items() if end > deadline}
    assert lb.cut == expect_cut
    for r, (_, _, end) in on_b.items():
        if end <= deadline:
            assert r in lb.completed
    # Nothing on another backend is cut, and every request is accounted for.
    assert all(lb.assigned[r][0] == b for r in lb.cut)
    assert lb.completed.isdisjoint(lb.cut)
    # The backend leaves the pool when it is empty, or at the deadline.
    last_end = max((end for _, _, end in on_b.values()), default=0)
    be = lb.backends[b]
    assert be.state == REMOVED
    assert be.removed_at == min(deadline, max(drain_at + lag, last_end))


def test_drain_many_seeds():
    for seed in range(200):
        rng = random.Random(seed)
        timeout = rng.choice([0, 5, 10, 15, 25, 40])
        lag = rng.choice([0, 0, 2, 5])
        b = rng.randrange(4)
        lb = simulate(random.Random(seed + 1000), drain_backend=b, timeout=timeout, lag=lag)
        check_run(lb, b, 50, timeout, lag)
        assert lb.errors == []


def test_worked_example():
    lb = Balancer(2)
    lb.tick(0)
    assert lb.arrive(1, 0, 4) == 0
    assert lb.arrive(2, 0, 12) == 1
    assert lb.arrive(3, 0, 9) == 0
    lb.drain(0, 1, timeout=6)  # deadline 7
    t_events = {}
    for t in range(1, 15):
        lb.tick(t)
        if t == 2:
            assert lb.arrive(4, 2, 3) == 1  # not to the draining backend 0
        t_events[t] = (sorted(lb.completed), sorted(lb.cut), lb.backends[0].state)
    assert t_events[4] == ([1], [], "draining")
    assert t_events[5] == ([1, 4], [], "draining")
    assert t_events[7] == ([1, 4], [3], REMOVED)
    assert lb.backends[0].removed_at == 7
    assert t_events[12] == ([1, 2, 4], [3], REMOVED)


def test_abrupt_removal_cuts_everything_in_flight():
    lb = simulate(random.Random(5), timeout=0)
    on_b = [r for r, v in lb.assigned.items() if v[0] == 0 and v[1] <= 50 < v[2]]
    assert sorted(lb.cut) == sorted(on_b)
    assert len(on_b) > 0


def test_deregistration_lag_race():
    # The backend refuses new work at once, but the balancer learns 5 ticks late.
    lb = simulate(random.Random(3), lag=5, refuse_after=0, timeout=30)
    routed_late = [r for r, b in lb.errors if b == 0]
    assert len(routed_late) > 0
    assert all(b == 0 for _, b in lb.errors)
    # The fix: keep accepting until every balancer has seen the drain.
    lb2 = simulate(random.Random(3), lag=5, refuse_after=5, timeout=30)
    assert lb2.errors == []


def test_goaway_two_step_loses_nothing():
    rng = random.Random(11)
    for _ in range(300):
        sends = sorted(rng.randint(0, 100) for _ in range(rng.randint(1, 30)))
        d = rng.randint(1, 10)
        g = rng.randint(0, 100)
        two = goaway_shutdown(sends, d, g, two_step=True)
        assert two.refused == []
        one = goaway_shutdown(sends, d, g, two_step=False)
        inflight = [2 * i + 1 for i, t in enumerate(sends) if g - d < t < g + d]
        assert one.refused == inflight


def test_goaway_example():
    sends = [0, 4, 9, 11, 13, 20]
    one = goaway_shutdown(sends, delay=3, goaway_at=10, two_step=False)
    assert (one.last_stream_id, one.processed, one.refused) == (3, [1, 3], [5, 7])
    two = goaway_shutdown(sends, delay=3, goaway_at=10, two_step=True)
    assert (two.last_stream_id, two.processed, two.refused) == (7, [1, 3, 5, 7], [])
