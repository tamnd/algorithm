# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fifo-broadcast/. The authors are listed in prov/271TJB.jsonl.

import random

from fifo_broadcast import Simulation


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
    return sum(1 for m in order for d in closure(deps, m) if d not in pos or pos[d] > pos[m])


def deliver(sim: Simulation, dst: int, mid: int) -> None:
    k = next(k for k, (q, msg) in enumerate(sim.network) if q == dst and msg[2] == mid)
    sim.step_network(k, may_crash=False)


def test_same_sender_reordering_is_repaired() -> None:
    sim = Simulation(2, random.Random(0))
    a = sim.broadcast(0, may_crash=False)
    b = sim.broadcast(0, may_crash=False)
    c = sim.broadcast(0, may_crash=False)
    deliver(sim, 1, c)
    deliver(sim, 1, b)
    assert sim.procs[1].delivered == [] and len(sim.procs[1].pending) == 2
    deliver(sim, 1, a)
    assert sim.procs[1].delivered == [a, b, c]


def test_fifo_violates_causal_order() -> None:
    # p0 broadcasts m1; p1 delivers m1 and then broadcasts m2; m2 reaches p2 first.
    sim = Simulation(3, random.Random(0))
    m1 = sim.broadcast(0, may_crash=False)
    deliver(sim, 1, m1)
    m2 = sim.broadcast(1, may_crash=False)
    assert m1 in closure(sim.deps, m2)  # m1 -> m2
    deliver(sim, 2, m2)
    assert sim.procs[2].delivered == [m2]  # FIFO allows this: m2 is the first message of p1
    deliver(sim, 2, m1)
    assert sim.procs[2].delivered == [m2, m1]
    assert causal_violations(sim.procs[2].delivered, sim.deps) == 1


def check(sim: Simulation) -> None:
    correct = sim.correct()
    for proc in sim.procs:
        order = proc.delivered
        assert len(order) == len(set(order))  # no duplication
        assert all(m in sim.sender for m in order)  # no creation
        for k in range(sim.n):
            nums = [sim.number[m] for m in order if sim.sender[m] == k]
            assert nums == list(range(1, len(nums) + 1))  # FIFO order, no gaps
        assert proc.next == [1 + sum(1 for m in order if sim.sender[m] == k) for k in range(sim.n)]
    sets = [set(sim.procs[p].delivered) for p in correct]
    for s in sets:
        assert s == sets[0]  # agreement among correct processes
    for m, p in sim.sender.items():
        if p in correct:
            for q in correct:
                assert m in sim.procs[q].delivered  # validity


def test_random_runs_with_crashes_and_adversarial_delays() -> None:
    rng = random.Random(1994)
    saw_crash = saw_violation = 0
    for _ in range(500):
        n = rng.randint(1, 5)
        sim = Simulation(n, rng, crash_prob=rng.choice([0.0, 0.1, 0.3]))
        sim.run(rng.randint(0, 40))
        check(sim)
        saw_crash += bool(sim.crashed)
        saw_violation += any(causal_violations(p.delivered, sim.deps) > 0 for p in sim.procs)
    assert saw_crash > 50
    assert saw_violation > 10  # FIFO order is weaker than causal order
