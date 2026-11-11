# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wait-for-graph/. The authors are listed in prov/T6DVQD.jsonl.
import random

from wait_for_graph import WaitForGraph, probe


def reach(succ, s):
    seen, stack = set(), [s]
    while stack:
        v = stack.pop()
        for w in succ.get(v, ()):
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def brute_cycle(edges, nodes):
    succ = {v: {q for p, q in edges if p == v} for v in nodes}
    return any(v in reach(succ, v) for v in nodes)


def test_page_example():
    g = WaitForGraph()
    assert g.add_wait("T1", "T2") is None
    assert g.add_wait("T2", "T3") is None
    assert g.add_wait("T4", "T1") is None
    assert g.add_wait("T3", "T1") == ["T3", "T1", "T2"]
    assert g.deadlocked() == {"T1", "T2", "T3", "T4"}
    g.remove_process("T2")  # abort the victim
    assert g.deadlocked() == set()
    assert g.edges() == {("T4", "T1"), ("T3", "T1")}


def test_incremental_check_matches_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        g = WaitForGraph()
        nodes = list(range(6))
        for _ in range(12):
            p, q = rng.sample(nodes, 2)
            r = rng.random()
            if r < 0.15:
                g.remove_process(p)
                continue
            if r < 0.3 and q in g.succ.get(p, ()):
                g.remove_wait(p, q)
                continue
            had = brute_cycle(g.edges(), nodes)
            cyc = g.add_wait(p, q)
            has = brute_cycle(g.edges(), nodes)
            if not had:
                assert (cyc is not None) == has
            if cyc is not None:
                assert cyc[0] == p and cyc[1] == q
                assert all(cyc[(k + 1) % len(cyc)] in g.succ[cyc[k]] for k in range(len(cyc)))
                g.remove_process(q)  # break it, as a lock manager would
            assert not brute_cycle(g.edges(), nodes) or had


def test_deadlocked_is_the_set_that_reaches_a_cycle():
    rng = random.Random(12)
    for _ in range(300):
        g = WaitForGraph()
        for _ in range(8):
            p, q = rng.sample(range(6), 2)
            g.add_wait(p, q)
        expect = {v for v in g.succ if any(w in reach(g.succ, w) for w in reach(g.succ, v) | {v})}
        assert g.deadlocked() == expect


def test_probe_detects_exactly_the_initiators_on_a_cycle():
    rng = random.Random(13)
    for t in range(400):
        nodes = list(range(7))
        succ = {v: set() for v in nodes}
        for _ in range(rng.randint(3, 10)):
            p, q = rng.sample(nodes, 2)
            succ[p].add(q)
        edges = sum(len(s) for s in succ.values())
        for i in nodes:
            found, sent = probe(succ, i, seed=t)
            assert found == (i in reach(succ, i))
            assert sent <= edges


def test_probe_on_a_process_behind_a_cycle():
    succ = {"a": {"b"}, "b": {"c"}, "c": {"b"}}
    assert probe(succ, "a", 0)[0] is False  # a is deadlocked but not on the cycle
    assert probe(succ, "b", 0)[0] is True
