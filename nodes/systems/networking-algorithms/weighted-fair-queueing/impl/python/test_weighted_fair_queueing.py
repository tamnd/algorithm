# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-fair-queueing/. The authors are listed in prov/XAQ195.jsonl.

import random
from collections import deque
from fractions import Fraction

from weighted_fair_queueing import WFQ, simulate


def gps_finish(arrivals, phi, rate):
    """Exact fluid GPS, event-driven, as an independent reference."""
    rate = Fraction(rate)
    queues = {f: deque() for f in phi}
    out = {}
    t = Fraction(0)
    i, n = 0, len(arrivals)
    while True:
        while i < n and arrivals[i][0] <= t:
            queues[arrivals[i][1]].append([Fraction(arrivals[i][2]), i])
            i += 1
        busy = [f for f in phi if queues[f]]
        if not busy:
            if i == n:
                return out
            t = Fraction(arrivals[i][0])
            continue
        total = sum(Fraction(phi[f]) for f in busy)
        share = {f: Fraction(phi[f]) * rate / total for f in busy}
        dt = min(queues[f][0][0] / share[f] for f in busy)
        if i < n and t + dt > arrivals[i][0]:
            dt = Fraction(arrivals[i][0]) - t
        t += dt
        for f in busy:
            queues[f][0][0] -= share[f] * dt
            if queues[f][0][0] == 0:
                out[queues[f].popleft()[1]] = t


def random_trace(rng: random.Random, flows, n: int, lmax: int):
    t, out = 0, []
    for _ in range(n):
        t += rng.choice([0, 0, 1, 2, 5, 15, 40])
        out.append((t, rng.choice(flows), rng.randint(1, lmax)))
    return out


def test_tags_by_hand() -> None:
    # Weights 1 and 3, rate 1: A sends 4 bits and B 6 bits at time 0.
    w = WFQ(1, {"A": 1, "B": 3})
    assert w.arrive(0, "A", 4, 0) == (0, 4)
    assert w.arrive(0, "B", 6, 1) == (0, 2)
    w.advance(8)  # V grows at rate 1/4 while both are backlogged in GPS
    assert w.v == 2
    w.advance(9)  # only A is left in GPS, so V grows at rate 1
    assert w.v == 3
    assert w.arrive(9, "B", 3, 2) == (3, 4)


def test_parekh_gallager_bound() -> None:
    # Every packet finishes at most L_max / r after its GPS finish time.
    for seed in range(40):
        rng = random.Random(seed)
        flows = list(range(rng.randint(2, 5)))
        phi = {f: rng.randint(1, 5) for f in flows}
        lmax = 16
        rate = rng.choice([1, 2, 3])
        arrivals = random_trace(rng, flows, 60, lmax)
        out = simulate(WFQ(rate, phi), arrivals)
        gps = gps_finish(arrivals, phi, rate)
        for p in range(len(arrivals)):
            assert out[p][1] <= gps[p] + Fraction(lmax, rate)
            for q in range(len(arrivals)):  # tag order is GPS finish order
                if out[p][2] < out[q][2]:
                    assert gps[p] <= gps[q]


def test_weighted_shares() -> None:
    # Two flows with weights 1 and 3, both always backlogged: bytes sent
    # stay in the ratio 1 : 3 up to a few packets.
    arrivals = [(0, "A", 10)] * 300 + [(0, "B", 7)] * 1200
    out = simulate(WFQ(1, {"A": 1, "B": 3}), arrivals)
    order = sorted(out, key=lambda p: out[p][0])
    sent = {"A": 0, "B": 0}
    for p in order[:1000]:
        sent[arrivals[p][1]] += arrivals[p][2]
        assert abs(3 * sent["A"] - sent["B"]) <= 3 * 10 + 7


def test_wfq_runs_ahead_of_gps() -> None:
    # The example of Bennett and Zhang: flow 0 has weight 10 and 11 packets,
    # ten other flows have weight 1 and one packet each, all at time 0.
    # GPS serves flow 0 at rate 1/2; WFQ sends its first ten packets first.
    phi = {0: 10, **{k: 1 for k in range(1, 11)}}
    arrivals = [(0, 0, 1)] * 11 + [(0, k, 1) for k in range(1, 11)]
    out = simulate(WFQ(1, phi), arrivals)
    first_ten = sorted(out, key=lambda p: out[p][0])[:10]
    assert all(arrivals[p][1] == 0 for p in first_ten)
    gps = gps_finish(arrivals, phi, 1)
    assert sorted(gps[p] for p in range(11))[:10] == list(range(2, 21, 2))
    # flow 0 then waits while the ten small flows are sent
    assert out[10][0] == 20
