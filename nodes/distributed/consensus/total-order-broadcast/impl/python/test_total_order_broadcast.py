# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-order-broadcast/. The authors are listed in prov/1XEK7N.jsonl.

import random

from total_order_broadcast import ConsensusFromTOB, SequencerTOB, Sim, TOBProcess, check_tob, run_tob


def crash_pattern(rng: random.Random, n: int) -> dict[int, int]:
    """Up to n - 1 faulty processes, each crashing after a random number of sends (0 means at once)."""
    f = rng.randrange(n)
    return {p: rng.randrange(3 * n) for p in rng.sample(range(n), f)}


def test_tob_from_consensus_without_crashes() -> None:
    sim, procs, broadcast = run_tob(4, seed=1, faulty={})
    seqs = {p.pid: p.sequence for p in procs}
    assert check_tob(4, sim, seqs, broadcast) == []
    assert all(len(s) == 12 for s in seqs.values())
    assert len({tuple(s) for s in seqs.values()}) == 1


def test_tob_from_consensus_with_crashes() -> None:
    for seed in range(400):
        rng = random.Random(seed)
        n = rng.randrange(2, 6)
        sim, procs, broadcast = run_tob(n, seed, crash_pattern(rng, n))
        seqs = {p.pid: p.sequence for p in procs}
        assert check_tob(n, sim, seqs, broadcast) == [], seed
        for p in range(n):  # the prefix property
            for q in set(range(n)) - sim.crashed:
                assert seqs[q][: len(seqs[p])] == seqs[p], seed


def test_crash_in_the_middle_of_a_broadcast() -> None:
    # process 0 crashes after 2 sends: its first message reaches only processes 0 and 1
    hits = 0
    for seed in range(50):
        sim, procs, broadcast = run_tob(4, seed, {0: 2}, per_process=1)
        seqs = {p.pid: p.sequence for p in procs}
        assert check_tob(4, sim, seqs, broadcast) == []
        hits += "m0.0" in seqs[1]
    assert 0 < hits  # in some runs the half-sent message still reaches everyone


def test_delivery_without_consensus_breaks_total_order() -> None:
    bad = 0
    for seed in range(50):
        sim, procs, broadcast = run_tob(3, seed, {}, use_consensus=False)
        seqs = {p.pid: p.sequence for p in procs}
        bad += any(v.startswith("total order") for v in check_tob(3, sim, seqs, broadcast))
    assert bad > 0


def consensus_runs(seed: int, layered: bool) -> None:
    rng = random.Random(seed)
    n = rng.randrange(2, 6)
    faulty = crash_pattern(rng, n)
    sim = Sim(n, seed, faulty if layered else {})
    cons: list[ConsensusFromTOB] = []
    if layered:  # consensus over the total-order broadcast that is built from consensus
        procs = [TOBProcess(p, sim) for p in range(n)]
        for p in range(n):
            cons.append(ConsensusFromTOB(p, procs[p].to_broadcast))
            procs[p].on_deliver = cons[p].on_deliver
    else:  # consensus over a black-box total-order broadcast
        tob = SequencerTOB(sim)
        for p in range(n):
            cons.append(ConsensusFromTOB(p, lambda m, p=p: tob.to_broadcast(p, m)))
            tob.on_deliver[p] = cons[p].on_deliver
        for p in faulty:
            if rng.random() < 0.5:
                sim.crashed.add(p)  # crashes before it proposes
    inputs = {p: rng.randrange(1000) for p in range(n)}
    order = list(range(n))
    rng.shuffle(order)
    for p in order:
        if p not in sim.crashed:
            cons[p].propose(inputs[p])
        for _ in range(rng.randrange(4)):
            sim.step()
        if not layered and p in faulty:
            sim.crashed.add(p)  # crashes after it proposes
    while sim.step():
        pass
    decided = {c.decision for c in cons if c.decision is not None}
    assert len(decided) <= 1, seed  # uniform agreement
    assert decided <= set(inputs.values()), seed  # validity
    for p in range(n):
        if p not in sim.crashed:
            assert cons[p].decision is not None, seed  # termination


def test_consensus_from_black_box_tob() -> None:
    for seed in range(300):
        consensus_runs(seed, layered=False)


def test_consensus_from_tob_from_consensus() -> None:
    for seed in range(300):
        consensus_runs(seed, layered=True)
