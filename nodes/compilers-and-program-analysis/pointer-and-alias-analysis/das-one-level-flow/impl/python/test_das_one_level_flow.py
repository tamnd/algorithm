# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/das-one-level-flow/. The authors are listed in prov/ADSKYW.jsonl.

import random

import ptsgen
from das_one_level_flow import das, points_to, value_classes

PAGE = """
entry:
  a = &x
  b = &y
  p = &a
  q = &b
  p = q
  ret 0
"""


def test_page_example():
    pts = points_to(PAGE)
    assert pts["p"] == {"a", "b"}
    assert pts["q"] == {"b"}  # the top level keeps its direction
    assert pts["a"] == {"x", "y"}  # the level below is unified
    assert pts["b"] == {"x", "y"}
    assert pts["x"] == set() and pts["y"] == set()
    assert ["a", "b"] in value_classes(ptsgen.parse(PAGE))
    # Andersen's analysis keeps a and b apart.
    least = ptsgen.least_solution(ptsgen.parse(PAGE))
    assert least["a"] == {"x"} and least["b"] == {"y"}


def test_store_and_load():
    # The store writes into the value node of a; the load reads it back.
    pts = points_to("p = &a\nq = &x\n*p = q\nr = *p")
    assert pts["a"] == {"x"} and pts["r"] == {"x"}
    assert pts["q"] == {"x"} and pts["p"] == {"a"}


def test_copy_direction_at_top_level():
    pts = points_to("p = &a\nq = &b\np = q")
    assert pts == {"p": {"a", "b"}, "a": set(), "q": {"b"}, "b": set()}


def test_contains_andersen_on_random_programs():
    rng = random.Random(2000)
    for trial in range(400):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), rng.randint(1, 30))
        pts = das(stmts)
        least = ptsgen.least_solution(stmts)
        for v in least:
            assert least[v] <= pts[v], ptsgen.show(stmts)
        assert ptsgen.is_solution(stmts, pts)


def test_equals_andersen_with_one_level_of_pointers():
    # Pointers p0.. take the addresses of targets t0.., which are never
    # assigned, and are copied into each other. Only the top level holds
    # addresses, so the unified level below loses nothing.
    rng = random.Random(3)
    for trial in range(200):
        stmts = []
        for _ in range(30):
            p, q = "p%d" % rng.randrange(8), "p%d" % rng.randrange(8)
            if rng.random() < 0.3:
                stmts.append(("addr", p, "t%d" % rng.randrange(5)))
            else:
                stmts.append(("copy", p, q))
        assert das(stmts) == ptsgen.least_solution(stmts)


def test_unified_level_can_lose_precision():
    # Here the targets a and b are pointers too; p = q unifies the values
    # stored in a and in b, which Andersen's analysis keeps apart.
    pts = points_to("p = &a\nq = &b\na = &x\nb = &y\np = q")
    assert pts["a"] == pts["b"] == {"x", "y"}


def test_sound_against_concrete_runs():
    rng = random.Random(77)
    for trial in range(150):
        stmts = ptsgen.random_program(rng, rng.randint(3, 10), 30)
        pts = das(stmts)
        for p, a in ptsgen.concrete_facts(stmts, rng, runs=10, steps=150):
            assert a in pts[p]


def test_order_of_statements_does_not_change_the_result():
    rng = random.Random(19)
    for trial in range(200):
        stmts = ptsgen.random_program(rng, rng.randint(2, 10), 30)
        first = das(stmts)
        shuffled = stmts[:]
        rng.shuffle(shuffled)
        assert das(shuffled) == first
