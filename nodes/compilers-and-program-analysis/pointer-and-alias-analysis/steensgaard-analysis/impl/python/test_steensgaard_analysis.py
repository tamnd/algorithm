# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steensgaard-analysis/. The authors are listed in prov/EFB787.jsonl.

import random

import ptsgen
from steensgaard_analysis import classes, points_to, steensgaard

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
    ab = {"a", "b"}
    assert pts == {"p": ab, "a": set(), "q": ab, "b": set(), "r": {"p"}, "s": ab, "t": ab}
    groups, target = classes(ptsgen.parse(PAGE))
    assert groups == [["a", "b"], ["p"], ["q"], ["r"], ["s"], ["t"]]
    assert target == {1: 0, 2: 0, 3: 1, 4: 0, 5: 0}


def test_copy_from_a_pointer_with_no_target_waits():
    # q has no target when p = q is seen; the join waits on the pending list
    # and happens when q = &b arrives. No placeholder is joined with b.
    pts = points_to("p = q\nq = &b")
    assert pts == {"p": {"b"}, "q": {"b"}, "b": set()}
    # A copy between two pointers that never get targets merges nothing.
    assert points_to("p = q\nr = &a") == {"p": set(), "q": set(), "r": {"a"}, "a": set()}


def test_unification_merges_targets():
    # Two different targets of one pointer end up in one class.
    pts = points_to("p = &a\np = &b\nq = &a")
    assert pts["q"] == {"a", "b"}


def test_store_and_load_through_unknown_targets():
    # *p = q before p has a target makes a placeholder class; p = &a later
    # joins a with it, so a gets the target of q.
    pts = points_to("*p = q\nq = &x\np = &a\nr = *p")
    assert pts["a"] == {"x"} and pts["r"] == {"x"}


def is_unification(pts):
    # Two sets are equal or disjoint, as in a storage graph where each
    # class points to at most one class.
    sets = [frozenset(s) for s in pts.values() if s]
    return all(a == b or not (a & b) for a in sets for b in sets)


def test_contains_andersen_on_random_programs():
    rng = random.Random(1996)
    for trial in range(400):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), rng.randint(1, 30))
        pts = steensgaard(stmts)
        least = ptsgen.least_solution(stmts)
        for v in least:
            assert least[v] <= pts[v], ptsgen.show(stmts)
        assert ptsgen.is_solution(stmts, pts)
        assert is_unification(pts)


def test_order_of_statements_does_not_change_the_result():
    rng = random.Random(11)
    for trial in range(200):
        stmts = ptsgen.random_program(rng, rng.randint(2, 10), 30)
        first = steensgaard(stmts)
        for _ in range(3):
            shuffled = stmts[:]
            rng.shuffle(shuffled)
            assert steensgaard(shuffled) == first, ptsgen.show(stmts)


def test_sound_against_concrete_runs():
    rng = random.Random(42)
    for trial in range(150):
        stmts = ptsgen.random_program(rng, rng.randint(3, 10), 30)
        pts = steensgaard(stmts)
        for p, a in ptsgen.concrete_facts(stmts, rng, runs=10, steps=150):
            assert a in pts[p]


def test_long_chain_needs_no_recursion():
    # p0 = &p1, p1 = &p2, ..., and a copy that joins the two ends of the
    # chain; the joins run through the queue, not the call stack.
    n = 3000
    lines = ["p%d = &p%d" % (i, i + 1) for i in range(n)]
    lines += ["q%d = &p%d" % (i, i) for i in range(1, n, 2)]
    lines += ["x = q1", "x = q%d" % (n - 1)]
    pts = points_to("\n".join(lines))
    assert pts["x"] == pts["q1"] and "p1" in pts["x"] and "p%d" % (n - 1) in pts["x"]
