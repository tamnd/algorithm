# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wait-die-and-wound-wait/. The authors are listed in prov/8VMTDE.jsonl.

import random

import pytest

from wait_die_and_wound_wait import run_locking, run_serial

INITIAL = {"x": "x0", "y": "y0", "z": "z0"}
# T1 is older than T2. Each one locks one item and then wants the other.
CROSS = {1: [("w", "x"), ("w", "y")], 2: [("w", "y"), ("w", "x")]}


def acyclic(edges) -> bool:
    nodes = {v for e in edges for v in e}
    succ = {v: [w for u, w in edges if u == v] for v in nodes}
    indeg = {v: 0 for v in nodes}
    for _, w in edges:
        indeg[w] += 1
    ready = [v for v in nodes if indeg[v] == 0]
    count = 0
    while ready:
        v = ready.pop()
        count += 1
        for w in succ[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                ready.append(w)
    return count == len(nodes)


def test_wait_die_cross_example() -> None:
    out = run_locking(CROSS, "wait-die", INITIAL, script=[1, 2, 1, 2])
    # w1(x), w2(y); T1 asks for y and waits (older); T2 asks for x and dies (younger).
    assert out["schedule"][:3] == [("w", 1, "x"), ("w", 2, "y"), ("a", 2, None)]
    assert out["commit_order"] == [1, 2]


def test_older_waits_under_wait_die() -> None:
    progs = {1: [("w", "x")], 2: [("w", "x"), ("w", "y")]}
    out = run_locking(progs, "wait-die", INITIAL, script=[2, 1, 2, 2, 1, 1])
    assert out["aborts"] == {1: 0, 2: 0}
    assert (1, 2) in out["waits"][1]
    assert out["commit_order"] == [2, 1]


def test_wound_wait_cross_example() -> None:
    out = run_locking(CROSS, "wound-wait", INITIAL, script=[1, 2, 1, 2])
    # w1(x), w2(y); T1 asks for y and wounds the younger holder T2.
    assert out["schedule"][:4] == [("w", 1, "x"), ("w", 2, "y"), ("a", 2, None), ("w", 1, "y")]
    assert out["commit_order"] == [1, 2]


def test_younger_waits_under_wound_wait() -> None:
    progs = {1: [("w", "x"), ("w", "y")], 2: [("w", "x")]}
    out = run_locking(progs, "wound-wait", INITIAL, script=[1, 2, 1, 1, 2, 2])
    assert out["aborts"] == {1: 0, 2: 0}
    assert (2, 1) in out["waits"][1]


@pytest.mark.parametrize("policy", ["wait-die", "wound-wait"])
def test_random_runs(policy: str) -> None:
    rng = random.Random(31 if policy == "wait-die" else 32)
    total = 0
    for _ in range(400):
        progs = {
            t: [(rng.choice("rw"), rng.choice("xyz")) for _ in range(rng.randint(1, 4))]
            for t in range(1, rng.randint(2, 6) + 1)
        }
        out = run_locking(progs, policy, INITIAL, rng=rng)
        assert sorted(out["commit_order"]) == sorted(progs)
        for edges in out["waits"]:
            for t, u in edges:
                assert (t < u) if policy == "wait-die" else (t > u)
            assert acyclic(edges)
        final, reads = run_serial(progs, out["commit_order"], INITIAL)
        assert out["final"] == final and out["reads"] == reads
        total += sum(out["aborts"].values())
    assert total > 0


def test_oldest_is_never_aborted() -> None:
    rng = random.Random(5)
    for policy in ("wait-die", "wound-wait"):
        for _ in range(200):
            progs = {
                t: [(rng.choice("rw"), rng.choice("xy")) for _ in range(rng.randint(1, 3))]
                for t in range(1, 5)
            }
            out = run_locking(progs, policy, INITIAL, rng=rng)
            assert out["aborts"][1] == 0
