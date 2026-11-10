# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-paxos/. The authors are listed in prov/8MFRY7.jsonl.

import random
from itertools import combinations, permutations

from generalized_paxos import (BOTTOM, GeneralizedPaxos, History, Inconsistent, glb, lub,
                               lub_all, prefix)

CMDS = [("a", "x"), ("b", "x"), ("c", "y"), ("d", "y"), ("e", "z")]


def small_histories() -> list:
    out = set()
    for k in range(4):
        for seq in permutations(CMDS[:4], k):
            out.add(History.of(seq))
    return sorted(out, key=repr)


def test_cstruct_laws_by_brute_force() -> None:
    hs = small_histories()
    for v in hs:
        assert prefix(BOTTOM, v) and prefix(v, v)
    for v in hs:
        for w in hs:
            g = glb(v, w)
            assert prefix(g, v) and prefix(g, w)
            # g is the greatest common lower bound.
            for u in hs:
                if prefix(u, v) and prefix(u, w):
                    assert prefix(u, g)
            u = lub(v, w)
            ups = [x for x in hs if prefix(v, x) and prefix(w, x)]
            if u is None:
                assert not ups or len(v.cmds | w.cmds) > 3
            else:
                assert prefix(v, u) and prefix(w, u)
                assert all(prefix(u, x) for x in ups)


def test_commuting_commands_in_any_order_are_one_history() -> None:
    a, c, e = ("a", "x"), ("c", "y"), ("e", "z")
    hs = {History.of(p) for p in permutations([a, c, e])}
    assert len(hs) == 1
    b = ("b", "x")
    assert History.of([a, b]) != History.of([b, a])
    assert lub(History.of([a, b]), History.of([b, a])) is None
    assert glb(History.of([a, b, c]), History.of([c, b, a])) == History.of([c])


def test_pairwise_compatible_sets_have_a_lub() -> None:
    hs = small_histories()
    rng = random.Random(1)
    for _ in range(3000):
        s = rng.sample(hs, 3)
        if all(lub(x, y) is not None for x, y in combinations(s, 2)):
            assert lub_all(s) is not None


def test_fast_ballot_with_commuting_commands_needs_no_new_ballot() -> None:
    cmds = [(f"c{i}", f"k{i}") for i in range(6)]
    for seed in range(40):
        sim = GeneralizedPaxos(5, seed, cmds, dup=0.1).run(start_fast=True)
        assert sim.done() and sim.consistent()
        assert sim.ballots_started == 1 and sim.twoa_sent == 1


def test_conflicting_commands_collide_and_recover() -> None:
    cmds = [(f"c{i}", "k") for i in range(5)]
    collided = 0
    for seed in range(40):
        sim = GeneralizedPaxos(5, seed, cmds, dup=0.1).run(start_fast=True)
        assert sim.done() and sim.consistent(), seed
        collided += sim.ballots_started > 1
    assert collided > 0


def test_safety_with_faults_and_duels() -> None:
    cmds = [("a", "x"), ("b", "x"), ("c", "y"), ("d", "y"), ("e", "z"), ("f", "x")]
    for seed in range(120):
        sim = GeneralizedPaxos(5, seed, cmds, dup=0.1, drop=0.05, crashes=1, crash_prob=0.01,
                               duel_prob=0.02, max_steps=4000).run(start_fast=seed % 2 == 0)
        assert sim.consistent() and sim.proposed_only(), seed
        assert sim.done(), seed


def test_quorums_that_break_the_condition_are_unsafe() -> None:
    # n = 4 with classic and fast quorums of 2: two learners can learn
    # different orders of the same two interfering commands.
    cmds = [("a", "x"), ("b", "x"), ("c", "x")]
    bad = 0
    for seed in range(300):
        sim = GeneralizedPaxos(4, seed, cmds, qc=2, qf=2, dup=0.1, duel_prob=0.05,
                               max_steps=2000)
        try:
            sim.run(start_fast=True)
            bad += not sim.consistent()
        except Inconsistent:
            bad += 1
    assert bad > 0
