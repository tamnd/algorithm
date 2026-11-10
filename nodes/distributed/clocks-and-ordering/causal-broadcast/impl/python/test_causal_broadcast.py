# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-broadcast/. The authors are listed in prov/Y3V5CE.jsonl.

import random

from causal_broadcast import Simulation


def closure(deps: dict[int, frozenset[int]], m: int) -> set[int]:
    """All messages in the causal past of the broadcast of m, by graph search on deps."""
    out: set[int] = set()
    todo = list(deps[m])
    while todo:
        x = todo.pop()
        if x not in out:
            out.add(x)
            todo.extend(deps[x])
    return out


def causal_violations(order: list[int], deps: dict[int, frozenset[int]]) -> int:
    pos = {m: k for k, m in enumerate(order)}
    bad = 0
    for m in order:
        for d in closure(deps, m):
            if d not in pos or pos[d] > pos[m]:
                bad += 1
    return bad


def deliver(sim: Simulation, dst: int, mid: int) -> None:
    k = next(k for k, (q, msg) in enumerate(sim.network) if q == dst and msg[2] == mid)
    sim.step_network(k, may_crash=False)


def test_example_buffers_a_message_that_overtakes_its_cause() -> None:
    sim = Simulation(3, random.Random(0))
    m1 = sim.broadcast(0, may_crash=False)
    deliver(sim, 1, m1)  # p1 delivers m1
    m2 = sim.broadcast(1, may_crash=False)  # so m1 -> m2
    assert sim.procs[1].vc == [1, 1, 0]
    deliver(sim, 2, m2)  # m2 overtakes m1 at p2
    assert sim.procs[2].delivered == [] and len(sim.procs[2].pending) == 1
    deliver(sim, 2, m1)
    assert sim.procs[2].delivered == [m1, m2]
    assert sim.procs[2].vc == [1, 1, 0]


def test_concurrent_messages_are_not_delayed() -> None:
    sim = Simulation(3, random.Random(0))
    a = sim.broadcast(0, may_crash=False)
    b = sim.broadcast(1, may_crash=False)
    deliver(sim, 2, b)
    deliver(sim, 2, a)
    assert sim.procs[2].delivered == [b, a]


def check(sim: Simulation) -> None:
    correct = sim.correct()
    for p, proc in enumerate(sim.procs):
        order = proc.delivered
        assert len(order) == len(set(order))  # no duplication
        assert all(m in sim.sender for m in order)  # no creation
        assert causal_violations(order, sim.deps) == 0  # causal order, also at crashed processes
        assert proc.vc == [sum(1 for m in order if sim.sender[m] == k) for k in range(sim.n)]
    sets = [set(sim.procs[p].delivered) for p in correct]
    for s in sets:
        assert s == sets[0]  # agreement among correct processes
    for m, p in sim.sender.items():
        if p in correct:
            for q in correct:
                assert m in sim.procs[q].delivered  # validity


def test_random_runs_with_crashes_and_adversarial_delays() -> None:
    rng = random.Random(1991)
    saw_crash = saw_buffering = 0
    for _ in range(500):
        n = rng.randint(1, 5)
        sim = Simulation(n, rng, crash_prob=rng.choice([0.0, 0.1, 0.3]))
        sim.run(rng.randint(0, 40))
        check(sim)
        saw_crash += bool(sim.crashed)
        saw_buffering += any(r != p.delivered[: len(r)] for r, p in zip(sim.received, sim.procs))
    assert saw_crash > 50 and saw_buffering > 50


def test_receipt_order_alone_violates_causality() -> None:
    # The reliable broadcast layer hands messages over in network order; the causal layer is needed.
    rng = random.Random(3)
    violations = 0
    for _ in range(200):
        sim = Simulation(4, rng)
        sim.run(30)
        violations += sum(causal_violations(r, sim.deps) > 0 for r in sim.received)
    assert violations > 0
