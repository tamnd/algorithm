# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-variable-substitution/. The authors are listed in prov/Q7GZTS.jsonl.

import random

import ptsgen
from offline_variable_substitution import ovs, points_to, rewrite, substitute

PAGE = """
entry:
  p = &a
  a = &b
  q = p
  r = q
  s = r
  r = s
  u = q
  u = s
  t = *u
  ret 0
"""


def test_page_example():
    stmts = ptsgen.parse(PAGE)
    rep = substitute(stmts)
    assert {v for v in rep if rep[v] == "p"} == {"p", "q", "r", "s", "u"}
    assert rep["a"] == "a" and rep["b"] == "b" and rep["t"] == "t"
    assert ptsgen.show(rewrite(stmts, rep)) == "p = &a\na = &b\nt = *p"
    pts, stats = ovs(stmts)
    assert pts == ptsgen.least_solution(stmts)
    assert pts["u"] == {"a"} and pts["t"] == {"b"}
    assert stats == {"variables": 8, "nodes": 4, "statements": 9, "reduced": 3}


def test_address_taken_variable_keeps_its_own_label():
    # q gets b through the store *w = s, since w points to q. Merging q
    # with its only copy source p would lose that fact.
    stmts = ptsgen.parse("p = &a\nq = p\nw = &q\ns = &b\n*w = s")
    rep = substitute(stmts)
    assert rep["q"] != rep["p"]
    pts = ovs(stmts)[0]
    assert pts["q"] == {"a", "b"} and pts["p"] == {"a"}
    assert pts == ptsgen.least_solution(stmts)


def test_load_target_keeps_its_own_label():
    stmts = ptsgen.parse("p = &a\nq = p\nr = &x\nx = &c\nq = *r")
    rep = substitute(stmts)
    assert rep["q"] != rep["p"]
    assert ovs(stmts)[0] == ptsgen.least_solution(stmts)


def test_two_sources_with_different_labels_stay_apart():
    stmts = ptsgen.parse("p = &a\nq = &b\nr = p\nr = q\ns = r")
    rep = substitute(stmts)
    assert rep["r"] not in (rep["p"], rep["q"])
    assert rep["s"] == rep["r"]
    assert ovs(stmts)[0] == ptsgen.least_solution(stmts)


def test_variables_with_no_source_share_the_empty_label():
    stmts = ptsgen.parse("x = y\nz = x\nw = *z\nu = v")
    rep = substitute(stmts)
    assert rep["x"] == rep["y"] == rep["z"] == rep["u"] == rep["v"]
    assert rep["w"] != rep["x"]
    assert all(s == set() for s in ovs(stmts)[0].values())


def test_equal_labels_mean_equal_least_sets():
    rng = random.Random(5100)
    for trial in range(400):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), rng.randint(1, 30))
        rep = substitute(stmts)
        least = ptsgen.least_solution(stmts)
        for v in rep:
            assert least[v] == least[rep[v]], ptsgen.show(stmts)


def test_equals_andersen_on_random_programs():
    rng = random.Random(5200)
    for trial in range(400):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), rng.randint(1, 30))
        assert ovs(stmts)[0] == ptsgen.least_solution(stmts), ptsgen.show(stmts)


def test_copy_heavy_programs_shrink():
    rng = random.Random(5300)
    before = after = 0
    for trial in range(200):
        stmts = ptsgen.random_program(rng, 20, 30, (1, 8, 1, 1))
        pts, stats = ovs(stmts)
        assert pts == ptsgen.least_solution(stmts)
        before += stats["variables"]
        after += stats["nodes"]
    assert after < before * 0.7


def test_sound_against_concrete_runs():
    rng = random.Random(5400)
    for trial in range(150):
        stmts = ptsgen.random_program(rng, rng.randint(3, 10), 30)
        pts = points_to(ptsgen.show(stmts))
        for p, a in ptsgen.concrete_facts(stmts, rng, runs=10, steps=150):
            assert a in pts[p]


def test_long_chain_without_recursion():
    n = 3000
    text = "\n".join(["v0 = &a"] + ["v%d = v%d" % (i + 1, i) for i in range(n)])
    stmts = ptsgen.parse(text)
    pts, stats = ovs(stmts)
    assert stats["nodes"] == 2  # v0 and its chain, and a
    assert pts["v%d" % n] == {"a"}
