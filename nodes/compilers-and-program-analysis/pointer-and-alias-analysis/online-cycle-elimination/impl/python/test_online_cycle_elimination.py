# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-cycle-elimination/. The authors are listed in prov/DDXZCS.jsonl.

import random

import ptsgen
from online_cycle_elimination import oce, points_to

PAGE = """
entry:
  p = &a
  a = &x
  q = *p
  r = q
  a = r
  s = &b
  r = s
  ret 0
"""


def acyclic(edges):
    succ = {}
    for u, v in edges:
        succ.setdefault(u, []).append(v)
    state = {}
    for start in succ:
        if start in state:
            continue
        state[start] = 1
        stack = [(start, iter(succ.get(start, [])))]
        while stack:
            node, it = stack[-1]
            for w in it:
                if state.get(w) == 1:
                    return False
                if w not in state:
                    state[w] = 1
                    stack.append((w, iter(succ.get(w, []))))
                    break
            else:
                state[node] = 2
                stack.pop()
    return True


def test_page_example():
    stmts = ptsgen.parse(PAGE)
    pts, stats = oce(stmts)
    assert pts["p"] == {"a"} and pts["s"] == {"b"}
    assert pts["a"] == pts["q"] == pts["r"] == {"x", "b"}
    # The load adds the edge a -> q, which closes the cycle a -> q -> r -> a.
    assert sorted(stats["classes"]["a"]) == ["a", "q", "r"]
    assert stats["merged"] == 2
    assert pts == ptsgen.least_solution(stmts)


def test_copy_cycle():
    pts, stats = oce(ptsgen.parse("p = &a\nq = p\nr = q\np = r"))
    assert pts["p"] == pts["q"] == pts["r"] == {"a"}
    assert stats["merged"] == 2


def test_no_cycle_no_merge():
    pts, stats = oce(ptsgen.parse("p = &a\nq = p\nr = q\nt = *r\n*q = p"))
    assert stats["merged"] == 0
    assert pts == ptsgen.least_solution(ptsgen.parse("p = &a\nq = p\nr = q\nt = *r\n*q = p"))


def test_self_store_and_load():
    stmts = ptsgen.parse("p = &p\n*p = p\nq = *p")
    assert oce(stmts)[0] == ptsgen.least_solution(stmts)


def test_equals_andersen_on_random_programs():
    rng = random.Random(4100)
    merges = 0
    for trial in range(400):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), rng.randint(1, 30))
        pts, stats = oce(stmts)
        assert pts == ptsgen.least_solution(stmts), ptsgen.show(stmts)
        merges += stats["merged"]
    assert merges > 100  # the random programs do have cycles


def test_graph_of_classes_has_no_cycle():
    rng = random.Random(4200)
    for trial in range(300):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), 30, (2, 6, 2, 2))
        pts, stats = oce(stmts)
        assert acyclic(stats["edges"]), ptsgen.show(stmts)
        # Every class holds variables with one and the same least set.
        least = ptsgen.least_solution(stmts)
        for members in stats["classes"].values():
            assert all(least[v] == least[members[0]] for v in members)


def test_order_of_statements_does_not_change_the_result():
    rng = random.Random(4300)
    for trial in range(200):
        stmts = ptsgen.random_program(rng, rng.randint(2, 10), 30)
        first = oce(stmts)[0]
        shuffled = stmts[:]
        rng.shuffle(shuffled)
        assert oce(shuffled)[0] == first


def test_sound_against_concrete_runs():
    rng = random.Random(4400)
    for trial in range(150):
        stmts = ptsgen.random_program(rng, rng.randint(3, 10), 30)
        pts = points_to(ptsgen.show(stmts))
        for p, a in ptsgen.concrete_facts(stmts, rng, runs=10, steps=150):
            assert a in pts[p]


def test_long_copy_cycle():
    n = 2000
    text = "\n".join(["v0 = &a"] + ["v%d = v%d" % ((i + 1) % n, i) for i in range(n)])
    pts, stats = oce(ptsgen.parse(text))
    assert all(pts["v%d" % i] == {"a"} for i in range(n))
    assert stats["merged"] == n - 1
