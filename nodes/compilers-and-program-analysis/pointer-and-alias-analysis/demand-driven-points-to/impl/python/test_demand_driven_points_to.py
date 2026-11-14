# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/demand-driven-points-to/. The authors are listed in prov/MGQX2W.jsonl.

import random
from collections import deque

import ptsgen
from demand_driven_points_to import demand_points_to

PAGE = """
entry:
  p = &a
  q = &b
  r = &p
  s = q
  *r = s
  t = *r
  u = &c
  v = u
  w = *v
  ret 0
"""


def andersen(stmts):
    """The exhaustive analysis, a copy of the solver of the Andersen page:
    a constraint graph with difference propagation over all variables."""
    names = ptsgen.variables(stmts)
    pts = {v: set() for v in names}
    succ = {v: set() for v in names}
    delta = {v: set() for v in names}
    loads = {v: set() for v in names}
    stores = {v: set() for v in names}
    work = deque()
    queued = set()

    def push(v):
        if v not in queued:
            queued.add(v)
            work.append(v)

    def propagate(s, v):
        new = s - pts[v]
        if new:
            pts[v] |= new
            delta[v] |= new
            push(v)

    def add_edge(u, v):
        if v not in succ[u]:
            succ[u].add(v)
            propagate(pts[u], v)

    for kind, x, y in stmts:
        if kind == "addr":
            pts[x].add(y)
            delta[x].add(y)
            push(x)
        elif kind == "load":
            loads[y].add(x)
        elif kind == "store":
            stores[x].add(y)
    for kind, x, y in stmts:
        if kind == "copy":
            add_edge(y, x)
    while work:
        n = work.popleft()
        queued.discard(n)
        d = delta[n]
        delta[n] = set()
        for a in d:
            for p in loads[n]:
                add_edge(a, p)
            for q in stores[n]:
                add_edge(q, a)
        for w in list(succ[n]):
            propagate(d, w)
    return pts


def test_page_example():
    stmts = ptsgen.parse(PAGE)
    answer, demanded = demand_points_to(stmts, ["t"])
    assert answer == {"t": {"a", "b"}}
    assert demanded == {"t", "r", "p", "s", "q"}
    answer, demanded = demand_points_to(stmts, ["q"])
    assert answer == {"q": {"b"}}
    assert demanded == {"q"}
    answer, demanded = demand_points_to(stmts, ["w"])
    assert answer == {"w": set()}
    assert demanded == {"w", "v", "u", "c", "r"}


def test_empty_and_unknown_queries():
    assert demand_points_to([], ["x"]) == ({"x": set()}, {"x"})
    assert demand_points_to([("addr", "p", "a")], []) == ({}, set())


def test_store_through_self():
    stmts = [("addr", "p", "p"), ("store", "p", "p")]
    answer, _ = demand_points_to(stmts, ["p"])
    assert answer == {"p": {"p"}}


def programs(seed, count):
    rng = random.Random(seed)
    for _ in range(count):
        nvars = rng.randint(2, 12)
        yield rng, ptsgen.random_program(rng, nvars, rng.randint(1, 40))


def test_same_as_exhaustive_analysis_for_every_query():
    for rng, stmts in programs(2001, 400):
        full = andersen(stmts)
        assert full == ptsgen.least_solution(stmts)
        names = ptsgen.variables(stmts)
        for _ in range(3):
            q = rng.choice(names)
            answer, demanded = demand_points_to(stmts, [q])
            assert answer == {q: full[q]}, ptsgen.show(stmts)
            assert q in demanded <= set(names) | {q}
        some = rng.sample(names, rng.randint(1, len(names)))
        answer, _ = demand_points_to(stmts, some)
        assert answer == {q: full[q] for q in some}


def test_queries_together_or_alone():
    for rng, stmts in programs(2006, 200):
        names = ptsgen.variables(stmts)
        together, both = demand_points_to(stmts, names)
        assert together == andersen(stmts)
        alone = set()
        for q in names:
            answer, demanded = demand_points_to(stmts, [q])
            assert answer[q] == together[q]
            alone |= demanded
        assert alone == both


def test_sound_against_concrete_runs():
    for rng, stmts in programs(1990, 300):
        facts = ptsgen.concrete_facts(stmts, rng, runs=10, steps=80)
        names = ptsgen.variables(stmts)
        answer, _ = demand_points_to(stmts, names[: len(names) // 2 + 1])
        for p, a in facts:
            if p in answer:
                assert a in answer[p], ptsgen.show(stmts)


def test_demand_skips_unrelated_variables():
    rng = random.Random(2005)
    total, part = 0, 0
    for _ in range(200):
        stmts = ptsgen.random_program(rng, 60, 60)
        names = ptsgen.variables(stmts)
        q = rng.choice(names)
        _, demanded = demand_points_to(stmts, [q])
        total += len(names)
        part += len(demanded)
    assert part < 0.5 * total
