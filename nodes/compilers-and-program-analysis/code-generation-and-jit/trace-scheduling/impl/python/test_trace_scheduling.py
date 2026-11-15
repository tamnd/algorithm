# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trace-scheduling/. The authors are listed in prov/5GWXK6.jsonl.
import copy
import random

import pytest

import toyir
import trace_scheduling as ts

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


def legal(items, edges, t, machine):
    for (u, v), d in edges.items():
        if t[v] < t[u] + d:
            return False
    by_cycle = {}
    for v in t:
        if items[v].unit() != "join":
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
            best[0] = min(best[0], ts.length(items, t))
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


def test_example():
    p = toyir.parse(EXAMPLE)
    live = ts.liveness(p)
    assert live["B2"] == {"a", "b", "s"}
    q, log = ts.trace_schedule(p, EXAMPLE_FREQ)
    assert [tr for tr, _, _ in log] == [["B0", "B1", "B3"], ["B0.2", "B2", "B3"]]
    items, t = log[0][1], log[0][2]
    got = {it.ins[1]: t[v] for v, it in enumerate(items) if it.kind == "op"}
    assert got == {"c": 0, "w": 0, "s": 2, "y": 1, "v": 2, "z": 5, "r": 6}
    assert [(it.kind, t[v]) for v, it in enumerate(items) if it.kind != "op"] == [("br", 1), ("join", 2), ("end", 7)]
    assert ts.length(items, t) == 8
    assert q.blocks["B0"].instrs == [("op", "c", "<", "b", 5), ("op", "w", "+", "b", 1)]
    assert q.blocks["B0"].term == ("br", "c", "B0.1", "B0.2")
    assert same_meaning(p, q, grid())
    assert toyir.run(q, [1, 7]) == ("ret", 58)
    assert toyir.run(q, [4, 0]) == ("trap",)


def test_example_lengths_against_blocks():
    p = toyir.parse(EXAMPLE)
    live = ts.liveness(p)
    local = 0
    for lab in ("B0", "B1", "B3"):
        items = ts.trace_items(p, [lab])
        edges = ts.build_dag(items, live)
        t = ts.list_schedule(items, edges)
        assert ts.length(items, t) == brute_optimum(items, edges, ts.MACHINE)
        local += ts.length(items, t)
    assert local == 12
    items = ts.trace_items(p, ["B0", "B1", "B3"])
    edges = ts.build_dag(items, live)
    assert brute_optimum(items, edges, ts.MACHINE) == 8


def test_compensation_is_needed():
    p = toyir.parse(EXAMPLE)
    q, _ = ts.trace_schedule(p, EXAMPLE_FREQ)
    broken = copy.deepcopy(q)
    b = broken.blocks["B0.2"]
    b.instrs = [ins for ins in b.instrs if ins[1] != "s"]
    assert toyir.run(p, [1, 7]) == ("ret", 58)
    with pytest.raises(toyir.UndefinedName):
        toyir.run(broken, [1, 7])


def test_meaning_random_programs():
    rng = random.Random(7)
    for _ in range(120):
        p = toyir.random_program(rng, rng.randint(2, 6), rng.randint(1, 8), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(p)}
        q, _ = ts.trace_schedule(p, freq)
        assert toyir.is_acyclic(q)
        inputs = [[rng.randint(-6, 9), rng.randint(-6, 9)] for _ in range(25)]
        assert same_meaning(p, q, inputs)


def test_meaning_with_profiles():
    rng = random.Random(8)
    for _ in range(50):
        p = toyir.random_program(rng, rng.randint(2, 6), rng.randint(2, 8), True)
        inputs = [[rng.randint(-6, 9), rng.randint(-6, 9)] for _ in range(25)]
        for freq in (ts.profile(p, inputs), ts.static_profile(p), None):
            q, _ = ts.trace_schedule(p, freq)
            assert same_meaning(p, q, inputs)


def potential(prog, done):
    memo = {}

    def paths(lab):
        if lab not in memo:
            s = toyir.succs(prog, lab)
            memo[lab] = 1 if lab in done or not s else sum(paths(x) for x in s)
        return memo[lab]

    return sum(paths(lab) for lab in prog.blocks if lab not in done)


def test_motion_rules_and_termination():
    rng = random.Random(9)
    seen = {"exit copy": 0, "entrance copy": 0, "speculation": 0}
    for _ in range(200):
        prog = toyir.random_program(rng, rng.randint(2, 6), rng.randint(2, 8), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(prog)}
        done = set()
        phi = potential(prog, done)
        while any(lab not in done for lab in prog.blocks):
            trace = ts.pick_trace(prog, freq, done)
            live = ts.liveness(prog)
            new, pieces, freq, (items, t) = ts.schedule_trace(prog, trace, freq)
            pos = {v: k for k, v in enumerate(sorted(range(len(items)), key=lambda v: (t[v], v)))}
            for b, it in enumerate(items):
                later = range(b + 1, len(items))
                if it.kind == "br":
                    for v in later:
                        w = items[v]
                        if w.kind in ("br", "end"):
                            assert pos[b] < pos[v]
                        elif w.kind == "op" and pos[v] < pos[b]:
                            assert not ts.can_trap(w.ins) and w.defs not in live[it.off]
                            seen["speculation"] += 1
                    if any(items[u].kind == "op" and pos[u] > pos[b] for u in range(b)):
                        seen["exit copy"] += 1
                if it.kind == "join":
                    assert all(pos[u] < pos[b] for u in range(b))
                    assert all(pos[v] > pos[b] for v in later if items[v].kind in ("br", "end"))
                    if any(items[v].kind == "op" and pos[v] < pos[b] for v in later):
                        seen["entrance copy"] += 1
            prog = new
            done |= pieces
            nphi = potential(prog, done)
            assert nphi < phi
            phi = nphi
    assert min(seen.values()) > 20


def test_schedules_against_brute_force():
    rng = random.Random(10)
    checked = 0
    while checked < 60:
        p = toyir.random_program(rng, 3, rng.randint(2, 4), True)
        freq = {e: rng.randint(0, 9) for e in toyir.edges(p)}
        trace = ts.pick_trace(p, freq, set())
        live = ts.liveness(p)
        items = ts.trace_items(p, trace)
        if len(items) > 9:
            continue
        edges = ts.build_dag(items, live)
        assert all(u < v for u, v in edges)
        t = ts.list_schedule(items, edges)
        assert legal(items, edges, t, ts.MACHINE)
        best = brute_optimum(items, edges, ts.MACHINE)
        assert ts.length(items, t) >= best
        local = 0
        for lab in trace:
            one = ts.trace_items(p, [lab])
            local += brute_optimum(one, ts.build_dag(one, live), ts.MACHINE)
        assert best <= local
        checked += 1


def test_input_checks():
    with pytest.raises(ValueError):
        ts.trace_schedule(toyir.parse("B0:\n  x = 1\n  br x B1 B0\nB1:\n  ret x\n"))
    with pytest.raises(ValueError):
        ts.trace_schedule(toyir.parse("# params: p\nB0:\n  x = *p\n  ret x\n"))
