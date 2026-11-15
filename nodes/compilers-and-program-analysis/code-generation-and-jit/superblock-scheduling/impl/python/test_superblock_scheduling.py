# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superblock-scheduling/. The authors are listed in prov/WWP2JP.jsonl.
import random

import pytest

import toyir
import superblock_scheduling as sbs

EXAMPLE = """# params: a, b
B0:
  c = b < 5
  s = a - b
  br c B1 B2
B1:
  y = a / b
  jump B3
B2:
  y = a - 1
  jump B3
B3:
  w = b + 1
  v = w * w
  z = y + v
  r = z + s
  ret r
"""
EXAMPLE_FREQ = {("B0", "B1"): 90, ("B0", "B2"): 10, ("B1", "B3"): 90, ("B2", "B3"): 10}


def same_meaning(p, q, inputs):
    return all(toyir.run(p, a) == toyir.run(q, a) for a in inputs)


def grid():
    return [[a, b] for a in range(-6, 7) for b in range(-6, 8)]


def ninstrs(prog):
    return sum(len(b.instrs) for b in prog.blocks.values())


def legal(items, edges, t, machine):
    for (u, v), d in edges.items():
        if u in t and v in t and t[v] < t[u] + d:
            return False
    by_cycle = {}
    for v in t:
        by_cycle.setdefault(t[v], []).append(items[v].unit())
    for units in by_cycle.values():
        if len(units) > machine["width"]:
            return False
        for u, m in machine["cap"].items():
            if units.count(u) > m:
                return False
    return True


def brute_optimum(items, edges, machine):
    """Try every start cycle for every item, in index order (a topological
    order), and keep the shortest legal schedule."""
    n = len(items)
    horizon = sum(it.latency() for it in items) + 1
    preds = [[] for _ in range(n)]
    for (u, v), d in edges.items():
        preds[v].append((u, d))
    best = [horizon + 10]

    def rec(j, t):
        if j == n:
            assert legal(items, edges, t, machine)
            best[0] = min(best[0], sbs.length(items, t))
            return
        lo = max([t[u] + d for u, d in preds[j]], default=0)
        for c in range(lo, horizon):
            if c + items[j].latency() >= best[0]:
                break
            t[j] = c
            if legal(items, {}, t, machine):
                rec(j + 1, t)
            del t[j]

    rec(0, {})
    return best[0]


def test_example_formation():
    p = toyir.parse(EXAMPLE)
    f, superblocks, freq = sbs.form_superblocks(p, EXAMPLE_FREQ)
    assert superblocks == [["B0", "B1", "B3"], ["B2", "B3.1"]]
    assert f.blocks["B2"].term == ("jump", "B3.1")
    assert f.blocks["B3.1"].instrs == f.blocks["B3"].instrs
    assert toyir.preds(f)["B3"] == ["B1"]
    assert freq[("B2", "B3.1")] == 10 and freq[("B1", "B3")] == 90
    assert same_meaning(p, f, grid())


def test_example_schedule():
    p = toyir.parse(EXAMPLE)
    q, superblocks, log = sbs.superblock_schedule(p, EXAMPLE_FREQ)
    items, t = log[0]
    got = {it.ins[1]: t[v] for v, it in enumerate(items) if it.kind == "op"}
    assert got == {"c": 0, "s": 1, "y": 2, "w": 0, "v": 3, "z": 6, "r": 7}
    assert [(it.kind, t[v]) for v, it in enumerate(items) if it.kind != "op"] == [("br", 1), ("end", 8)]
    assert sbs.length(items, t) == 9
    f, _, _ = sbs.form_superblocks(p, EXAMPLE_FREQ)
    live = sbs.liveness(f)
    assert live["B2"] == {"a", "b", "s"}
    assert brute_optimum(items, sbs.build_dag(items, live), sbs.MACHINE) == 8
    assert list(q.blocks) == ["B0", "B0.1", "B2"]
    assert q.blocks["B0"].instrs == [("op", "c", "<", "b", 5), ("op", "w", "+", "b", 1), ("op", "s", "-", "a", "b")]
    assert q.blocks["B0"].term == ("br", "c", "B0.1", "B2")
    assert sbs.length(*log[1]) == 7
    assert ninstrs(q) == ninstrs(f)
    assert same_meaning(p, q, grid())
    assert toyir.run(q, [1, 7]) == ("ret", 58)
    assert toyir.run(q, [4, 2]) == ("ret", 13)
    assert toyir.run(q, [4, 0]) == ("trap",)


def test_formation_on_random_programs():
    rng = random.Random(11)
    for _ in range(150):
        p = toyir.random_program(rng, rng.randint(2, 6), rng.randint(1, 8), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(p)}
        f, superblocks, _ = sbs.form_superblocks(p, freq)
        assert toyir.is_acyclic(f)
        assert f.entry == p.entry and any(sb[0] == p.entry for sb in superblocks)
        assert sorted(lab for sb in superblocks for lab in sb) == sorted(f.blocks)
        pr = toyir.preds(f)
        for sb in superblocks:
            for i in range(1, len(sb)):
                assert pr[sb[i]] == [sb[i - 1]]
                assert sb[i] in toyir.succs(f, sb[i - 1])
        inputs = [[rng.randint(-6, 9), rng.randint(-6, 9)] for _ in range(20)]
        assert same_meaning(p, f, inputs)


def test_meaning_random_programs():
    rng = random.Random(12)
    for _ in range(120):
        p = toyir.random_program(rng, rng.randint(2, 6), rng.randint(1, 8), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(p)}
        q, _, _ = sbs.superblock_schedule(p, freq)
        assert toyir.is_acyclic(q)
        f, _, _ = sbs.form_superblocks(p, freq)
        assert ninstrs(q) == ninstrs(f)
        inputs = [[rng.randint(-6, 9), rng.randint(-6, 9)] for _ in range(25)]
        assert same_meaning(p, q, inputs)


def test_meaning_with_profiles():
    rng = random.Random(13)
    for _ in range(35):
        p = toyir.random_program(rng, rng.randint(2, 6), rng.randint(2, 8), True)
        inputs = [[rng.randint(-6, 9), rng.randint(-6, 9)] for _ in range(25)]
        for freq in (sbs.profile(p, inputs), sbs.static_profile(p), None):
            q, _, _ = sbs.superblock_schedule(p, freq)
            assert same_meaning(p, q, inputs)


def potential(prog, done):
    memo = {}

    def paths(lab):
        if lab not in memo:
            s = toyir.succs(prog, lab)
            memo[lab] = 1 if lab in done or not s else sum(paths(x) for x in s)
        return memo[lab]

    return sum(paths(lab) for lab in prog.blocks if lab not in done)


def test_formation_stops():
    rng = random.Random(14)
    for _ in range(200):
        prog = toyir.random_program(rng, 3, rng.randint(2, 9), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(prog)}
        done = set()
        phi = potential(prog, done)
        while any(lab not in done for lab in prog.blocks):
            trace = sbs.pick_trace(prog, freq, done)
            prog, freq = sbs.tail_duplicate(prog, trace, freq)
            done |= set(trace)
            nphi = potential(prog, done)
            assert nphi < phi
            phi = nphi


def test_motion_rules():
    rng = random.Random(15)
    seen = {"above": 0, "below": 0}
    for _ in range(120):
        p = toyir.random_program(rng, rng.randint(2, 6), rng.randint(2, 8), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(p)}
        prog, superblocks, _ = sbs.form_superblocks(p, freq)
        for sb in superblocks:
            live = sbs.liveness(prog)
            new, _, (items, t) = sbs.schedule_superblock(prog, sb)
            pos = {v: k for k, v in enumerate(sorted(range(len(items)), key=lambda v: (t[v], v)))}
            for b, it in enumerate(items):
                if it.kind != "br":
                    continue
                for v, w in enumerate(items):
                    if w.kind != "op":
                        assert (v < b) == (pos[v] < pos[b])
                        continue
                    if (v < b) != (pos[v] < pos[b]):
                        assert not sbs.can_trap(w.ins) and w.defs not in live[it.off]
                        seen["above" if v > b else "below"] += 1
            prog = new
    assert min(seen.values()) > 20


def test_schedules_against_brute_force():
    rng = random.Random(16)
    checked = 0
    while checked < 60:
        p = toyir.random_program(rng, 3, rng.randint(2, 4), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(p)}
        f, superblocks, _ = sbs.form_superblocks(p, freq)
        sb = superblocks[0]
        live = sbs.liveness(f)
        items = sbs.superblock_items(f, sb)
        if len(items) > 9:
            continue
        edges = sbs.build_dag(items, live)
        assert all(u < v for u, v in edges)
        t = sbs.list_schedule(items, edges)
        assert legal(items, edges, t, sbs.MACHINE)
        best = brute_optimum(items, edges, sbs.MACHINE)
        assert sbs.length(items, t) >= best
        local = 0
        for lab in sb:
            one = sbs.superblock_items(f, [lab])
            local += brute_optimum(one, sbs.build_dag(one, live), sbs.MACHINE)
        assert best <= local
        checked += 1


def test_input_checks():
    with pytest.raises(ValueError):
        sbs.superblock_schedule(toyir.parse("B0:\n  x = 1\n  br x B1 B0\nB1:\n  ret x\n"))
    with pytest.raises(ValueError):
        sbs.superblock_schedule(toyir.parse("# params: p\nB0:\n  x = *p\n  ret x\n"))
    one = toyir.parse("# params: a\nB0:\n  x = a + 1\n  ret x\n")
    q, superblocks, _ = sbs.superblock_schedule(one)
    assert superblocks == [["B0"]] and toyir.run(q, [4]) == ("ret", 5)
