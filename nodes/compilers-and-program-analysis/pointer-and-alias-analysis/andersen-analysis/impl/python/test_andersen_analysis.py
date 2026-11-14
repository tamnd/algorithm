# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/andersen-analysis/. The authors are listed in prov/MBB0JP.jsonl.

import random

import ptsgen
from andersen_analysis import andersen, may_alias, points_to

PAGE = """
entry:
  p = &a
  q = &b
  r = &p
  s = q
  *r = s
  t = *r
  ret 0
"""


def test_page_example():
    pts = points_to(PAGE)
    assert pts == {
        "p": {"a", "b"},
        "a": set(),
        "q": {"b"},
        "b": set(),
        "r": {"p"},
        "s": {"b"},
        "t": {"a", "b"},
    }
    assert may_alias(pts, "p", "t")
    assert may_alias(pts, "q", "s")
    assert may_alias(pts, "p", "q")
    assert not may_alias(pts, "r", "p")


def test_parse_and_show():
    stmts = ptsgen.parse(PAGE)
    assert [k for k, _, _ in stmts] == ["addr", "addr", "addr", "copy", "store", "load"]
    assert ptsgen.parse(ptsgen.show(stmts)) == stmts


def test_allocation_sites():
    # Each alloc instruction is one abstract location.
    pts = points_to("p = alloc\nq = alloc\nr = p\n*r = q\ns = *p")
    assert pts["p"] == {"h1"} and pts["q"] == {"h2"}
    assert pts["h1"] == {"h2"} and pts["s"] == {"h2"}


def test_empty_and_trivial():
    assert andersen([]) == {}
    assert points_to("p = p") == {"p": set()}
    assert points_to("p = &p\nq = *p") == {"p": {"p"}, "q": {"p"}}


def test_store_through_self():
    # *p = p with p = &a writes the address of a into a.
    assert points_to("p = &a\n*p = p") == {"p": {"a"}, "a": {"a"}}


def test_same_as_least_solution_on_random_programs():
    rng = random.Random(1994)
    for trial in range(400):
        nvars = rng.randint(2, 12)
        stmts = ptsgen.random_program(rng, nvars, rng.randint(1, 30))
        pts = andersen(stmts)
        assert pts == ptsgen.least_solution(stmts), ptsgen.show(stmts)
        assert ptsgen.is_solution(stmts, pts)


def test_every_fact_is_needed():
    # The result is the least solution, so no smaller assignment is a
    # solution: removing any one fact breaks some constraint.
    rng = random.Random(7)
    for trial in range(100):
        stmts = ptsgen.random_program(rng, 6, 20)
        pts = andersen(stmts)
        for v in pts:
            for a in pts[v]:
                smaller = {w: set(s) for w, s in pts.items()}
                smaller[v].discard(a)
                assert not ptsgen.is_solution(stmts, smaller)


def test_sound_against_concrete_runs():
    rng = random.Random(2024)
    for trial in range(150):
        stmts = ptsgen.random_program(rng, rng.randint(3, 10), 30)
        pts = andersen(stmts)
        facts = ptsgen.concrete_facts(stmts, rng, runs=10, steps=150)
        for p, a in facts:
            assert a in pts[p], (p, a, ptsgen.show(stmts))


def test_concrete_runs_reach_most_facts():
    # The analysis is the least solution, and with enough runs the concrete
    # program shows nearly every fact of it. The check uses programs without
    # loads and stores, where every fact must show up.
    rng = random.Random(5)
    for trial in range(50):
        stmts = ptsgen.random_program(rng, 6, 15, weights=(1, 2, 0, 0))
        pts = andersen(stmts)
        facts = ptsgen.concrete_facts(stmts, rng, runs=40, steps=200)
        assert facts == {(p, a) for p in pts for a in pts[p]}
