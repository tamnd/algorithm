# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deficit-round-robin/. The authors are listed in prov/4F8MEF.jsonl.

import random
from fractions import Fraction

from deficit_round_robin import DRR, packet_round_robin


def run_online(rng: random.Random, quantum: dict, max_size: int, steps: int):
    """Mix random arrivals with departures. After each departure, record the
    bytes sent so far per flow and the set of flows in the ActiveList."""
    drr = DRR(quantum)
    flows = list(quantum)
    sent = {f: 0 for f in flows}
    trace = []
    pid = 0
    for _ in range(steps):
        for _ in range(rng.choice([0, 1, 1, 2, 3])):
            drr.enqueue(rng.choice(flows), rng.randint(1, max_size), pid)
            pid += 1
        got = drr.next_packet()
        if got is not None:
            sent[got[0]] += got[1]
        trace.append((dict(sent), frozenset(drr.in_list)))
    return trace


def check_fairness(trace, quantum: dict, max_size: int) -> int:
    """Over every run of points in which flows i and j both stay in the
    ActiveList, |sent_i / Q_i - sent_j / Q_j| between any two points is less
    than 1 + M / Q_i + M / Q_j. Return the number of runs checked."""
    flows = list(quantum)
    runs = 0
    for a in flows:
        for b in flows:
            if a >= b:
                continue
            bound = 1 + Fraction(max_size, quantum[a]) + Fraction(max_size, quantum[b])
            lo = hi = None
            for sent, in_list in trace:
                if a in in_list and b in in_list:
                    d = Fraction(sent[a], quantum[a]) - Fraction(sent[b], quantum[b])
                    if lo is None:
                        lo = hi = d
                        runs += 1
                    lo, hi = min(lo, d), max(hi, d)
                    assert hi - lo < bound
                else:
                    lo = hi = None
    return runs


def test_fairness_bound_on_random_traces() -> None:
    for seed in range(20):
        rng = random.Random(seed)
        max_size = rng.choice([100, 1500])
        quantum = {f: rng.randint(max_size // 3, 3 * max_size) for f in range(rng.randint(2, 5))}
        trace = run_online(rng, quantum, max_size, 2000)
        assert check_fairness(trace, quantum, max_size) > 0


def test_equal_quanta_bound() -> None:
    # Equal quanta Q: two backlogged flows differ by less than Q + 2 Max bytes.
    rng = random.Random(7)
    q, m = 500, 1500
    drr = DRR({0: q, 1: q, 2: q})
    for f in range(3):
        for k in range(2000):
            drr.enqueue(f, rng.randint(1, m), (f, k))
    sent = [0, 0, 0]
    diffs = []
    while (got := drr.next_packet()) is not None:
        sent[got[0]] += got[1]
        if all(drr.queues[f] for f in range(3)):
            diffs.append(sent[0] - sent[1])
    assert max(diffs) - min(diffs) < q + 2 * m


def test_long_run_shares_follow_the_quanta() -> None:
    rng = random.Random(3)
    quantum = {"a": 1000, "b": 2000, "c": 3000}
    drr = DRR(quantum)
    for f in quantum:
        for k in range(6000):
            drr.enqueue(f, rng.randint(40, 1500), k)
    sent = {f: 0 for f in quantum}
    for _ in range(6000):
        f, size, _ = drr.next_packet()
        sent[f] += size
    total = sum(sent.values())
    for f in quantum:
        assert abs(sent[f] / total - quantum[f] / 6000) < 0.01


def test_packet_round_robin_favours_large_packets() -> None:
    big, small = [1500] * 1000, [100] * 15000
    rr = {"big": 0, "small": 0}
    for k, (f, size) in enumerate(packet_round_robin({"big": big, "small": small})):
        if k == 1000:
            break
        rr[f] += size
    assert rr["big"] == 15 * rr["small"]  # 15 : 1 in bytes

    drr = DRR({"big": 1500, "small": 1500})
    for k, s in enumerate(big):
        drr.enqueue("big", s, k)
    for k, s in enumerate(small):
        drr.enqueue("small", s, k)
    sent = {"big": 0, "small": 0}
    for _ in range(3000):
        f, size, _ = drr.next_packet()
        sent[f] += size
    assert abs(sent["big"] - sent["small"]) <= 1500


def test_constant_work_when_quantum_covers_max_packet() -> None:
    # With Q_i >= Max, every turn sends at least one packet, so the number of
    # turns is at most the number of packets (Theorem 4.5 of the paper).
    rng = random.Random(11)
    drr = DRR({f: 1500 for f in range(4)})
    n = 0
    for f in range(4):
        for k in range(500):
            drr.enqueue(f, rng.randint(64, 1500), k)
            n += 1
    while drr.next_packet() is not None:
        pass
    assert drr.empty_turns == 0 and drr.turns <= n
    # With a small quantum, some turns send nothing.
    drr = DRR({f: 100 for f in range(4)})
    for f in range(4):
        for k in range(50):
            drr.enqueue(f, 1500, k)
    while drr.next_packet() is not None:
        pass
    assert drr.empty_turns > 0
