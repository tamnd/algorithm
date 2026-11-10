# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epaxos/. The authors are listed in prov/D37K98.jsonl.

import random
from itertools import combinations

from epaxos import EPaxos, fast_quorum_size, tarjan

CMDS = [(f"c{i}", f"k{i % 3}") for i in range(15)]


def test_fast_quorum_sizes_and_overlap() -> None:
    assert [fast_quorum_size(f) for f in (1, 2, 3, 4, 5)] == [2, 3, 5, 6, 8]
    for f in range(1, 5):
        n, fq = 2 * f + 1, fast_quorum_size(f)
        leader = 0
        others = range(1, n)
        for q in combinations(others, fq - 1):
            for m in combinations(others, f + 1):
                # A recovery majority without the leader meets the fast
                # quorum in at least floor((F + 1) / 2) replicas.
                assert len(set(q) & set(m)) >= (f + 1) // 2


def test_tarjan_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(1, 9)
        edges = {v: sorted(rng.sample(range(n), rng.randrange(0, min(3, n + 1)))) for v in range(n)}

        def reach(v: int) -> set:
            seen, todo = {v}, [v]
            while todo:
                for w in edges[todo.pop()]:
                    if w not in seen:
                        seen.add(w)
                        todo.append(w)
            return seen

        comps = tarjan(0, lambda v: edges[v])
        assert sorted(v for c in comps for v in c) == sorted(reach(0))
        pos = {v: i for i, c in enumerate(comps) for v in c}
        for v in reach(0):
            for w in reach(v):
                # w reaches back to v exactly when they share a component,
                # and otherwise w's component comes first.
                if v in reach(w):
                    assert pos[v] == pos[w]
                else:
                    assert pos[w] < pos[v]


def test_conflicting_commands_run_in_the_same_order_everywhere() -> None:
    for f in (1, 2, 3):
        for seed in range(60):
            sim = EPaxos(f, seed, CMDS, dup=0.1).run()
            assert sim.all_executed(), (f, seed)
            assert sim.conflicts_are_ordered(), (f, seed)
            assert sim.same_order_for_conflicts(), (f, seed)


def test_crashes_of_replicas_that_lead_nothing() -> None:
    for seed in range(60):
        sim = EPaxos(2, seed, CMDS, proposers=[0, 1, 2], dup=0.1, crashes=2,
                     crash_prob=0.02).run()
        assert sim.all_executed() and sim.same_order_for_conflicts(), seed


def test_no_interference_means_fast_path_only() -> None:
    cmds = [(f"c{i}", f"key{i}") for i in range(12)]
    for f in (1, 2, 3):
        for seed in range(20):
            sim = EPaxos(f, seed, cmds, dup=0.1).run()
            assert sim.slow_commits == 0 and sim.fast_commits == len(cmds)
            assert sim.all_executed()


def test_conflicts_force_the_slow_path_sometimes() -> None:
    slow = sum(EPaxos(2, seed, CMDS).run().slow_commits for seed in range(20))
    assert slow > 0
    # With F = 1 a fast quorum is the leader and one other replica, so one
    # reply always agrees with itself.
    assert sum(EPaxos(1, seed, CMDS).run().slow_commits for seed in range(20)) == 0


def test_fast_commit_with_the_leaders_attributes_is_unsafe() -> None:
    bad = sum(not EPaxos(2, seed, CMDS, dup=0.1, unsafe_fast=True).run().conflicts_are_ordered()
              for seed in range(30))
    assert bad > 0


def test_executing_in_commit_order_diverges() -> None:
    bad = sum(not EPaxos(2, seed, CMDS, dup=0.1, naive_execute=True).run().same_order_for_conflicts()
              for seed in range(30))
    assert bad > 0
