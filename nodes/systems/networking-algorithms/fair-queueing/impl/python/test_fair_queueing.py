# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fair-queueing/. The authors are listed in prov/YH4B2M.jsonl.

import random
from collections import deque
from fractions import Fraction

from fair_queueing import FairQueueing, simulate


def fluid_equal_share(arrivals, rate):
    """Exact bit-by-bit round robin in the limit: each backlogged flow gets
    rate / (number of backlogged flows), FIFO inside a flow. Return the
    finish time of each packet."""
    rate = Fraction(rate)
    queues: dict = {}
    finish = {}
    t = Fraction(0)
    i, n = 0, len(arrivals)
    while i < n or any(queues.values()):
        backlogged = [q for q in queues.values() if q]
        if not backlogged:
            t = Fraction(arrivals[i][0])
        while i < n and arrivals[i][0] <= t:
            _, flow, size = arrivals[i]
            queues.setdefault(flow, deque()).append([Fraction(size), i])
            i += 1
        backlogged = [q for q in queues.values() if q]
        share = rate / len(backlogged)
        dt = min(q[0][0] for q in backlogged) / share
        if i < n and t + dt > arrivals[i][0]:
            dt = arrivals[i][0] - t
        t += dt
        for q in backlogged:
            q[0][0] -= share * dt
            if q[0][0] == 0:
                finish[q.popleft()[1]] = t
    return finish


def fifo(arrivals, rate):
    t, out = Fraction(0), {}
    for pid, (a, _, size) in enumerate(arrivals):
        t = max(t, Fraction(a)) + Fraction(size) / rate
        out[pid] = t
    return out


def test_hand_trace() -> None:
    # A1, A2 (4 bytes each) and B1 (2 bytes) at t = 0, C1 (6 bytes) at t = 1.
    arrivals = [(0, "A", 4), (0, "A", 4), (0, "B", 2), (1, "C", 6)]
    out = simulate(FairQueueing(1), arrivals)
    assert [out[p][2] for p in range(4)] == [4, 8, 2, Fraction(13, 2)]
    order = sorted(range(4), key=lambda p: out[p][0])
    assert order == [2, 0, 3, 1]  # B1, A1, C1, A2
    assert [out[p][1] for p in order] == [2, 6, 12, 16]
    fluid = fluid_equal_share(arrivals, 1)
    assert [fluid[p] for p in order] == [Fraction(11, 2), Fraction(19, 2), Fraction(29, 2), 16]


def random_trace(rng: random.Random, n: int, flows: int, lmax: int):
    t, out = 0, []
    for _ in range(n):
        t += rng.choice([0, 0, 1, 3, 10, 40])
        out.append((t, rng.randrange(flows), rng.randint(1, lmax)))
    return out


def test_tags_follow_the_fluid_order_and_the_lag_bound() -> None:
    for seed in range(30):
        rng = random.Random(seed)
        lmax = 20
        arrivals = random_trace(rng, 60, rng.randint(2, 5), lmax)
        rate = rng.choice([1, 2, 3])
        out = simulate(FairQueueing(rate), arrivals)
        fluid = fluid_equal_share(arrivals, rate)
        pids = range(len(arrivals))
        # The fluid finish times are in the order of the finish numbers.
        for p in pids:
            for q in pids:
                if out[p][2] < out[q][2]:
                    assert fluid[p] <= fluid[q]
        # No packet finishes later than lmax / rate after the fluid model.
        for p in pids:
            assert out[p][1] <= fluid[p] + Fraction(lmax, rate)


def test_equal_bytes_against_fifo() -> None:
    # Flow A: 100 packets of 1500 bytes; flow B: 1500 packets of 100 bytes;
    # all arrive at t = 0, A first. FIFO serves all of A first.
    arrivals = [(0, "A", 1500)] * 100 + [(0, "B", 100)] * 1500
    out = simulate(FairQueueing(1), arrivals)
    order = sorted(range(len(arrivals)), key=lambda p: out[p][0])
    sent = {"A": 0, "B": 0}
    worst = 0
    for p in order[:-1]:
        sent[arrivals[p][1]] += arrivals[p][2]
        if sent["A"] < 150000 and sent["B"] < 150000:
            worst = max(worst, abs(sent["A"] - sent["B"]))
    assert worst <= 1500
    f = fifo(arrivals, 1)
    assert min(f[p] for p in range(100, 1600)) == 150100  # B waits for all of A


def test_isolation_from_a_heavy_flow() -> None:
    # H sends 1500 bytes every 750 time units, twice the link rate of 1.
    # L sends 100 bytes every 1000. Under FQ the delay of L stays below its
    # fluid delay (100 bytes at half the link) plus one packet of H.
    arrivals = sorted(
        [(750 * k, "H", 1500) for k in range(400)]
        + [(1000 * k + 7, "L", 100) for k in range(300)]
    )
    out = simulate(FairQueueing(1), arrivals)
    light = [out[p][1] - arrivals[p][0] for p in range(len(arrivals)) if arrivals[p][1] == "L"]
    assert max(light) <= 200 + 1500
    f = fifo(arrivals, 1)
    worst_fifo = max(f[p] - arrivals[p][0] for p in range(len(arrivals)) if arrivals[p][1] == "L")
    assert worst_fifo > 100000
