# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbolic-reachability/. The authors are listed in prov/5F99Q0.jsonl.

import itertools
import random

from symbolic_reachability import SymbolicSystem, backward_reachable, reachable, step

X = lambda j: ("x", j)
NOT = lambda a: ("not", a)
AND = lambda a, b: ("and", a, b)

# A 3-bit counter that counts up when the input is 1 and resets at 5.
x0, x1, x2, en = X(0), X(1), X(2), ("in", 0)
AT5 = AND(AND(x0, NOT(x1)), x2)
COUNTER = {
    "init": (0, 0, 0),
    "inputs": 1,
    "next": [AND(NOT(AT5), ("xor", x0, en)), AND(NOT(AT5), ("xor", x1, AND(x0, en))), AND(NOT(AT5), ("xor", x2, AND(AND(x0, x1), en)))],
}


def rand_expr(rng, nl, ni, depth):
    if depth == 0 or rng.random() < 0.3:
        if ni and rng.random() < 0.3:
            return ("in", rng.randrange(ni))
        return X(rng.randrange(nl))
    op = rng.choice(["not", "and", "or", "xor"])
    if op == "not":
        return NOT(rand_expr(rng, nl, ni, depth - 1))
    return (op, rand_expr(rng, nl, ni, depth - 1), rand_expr(rng, nl, ni, depth - 1))


def bfs(c):
    """Explicit BFS: the distance of each reachable state from the initial state."""
    dist = {c["init"]: 0}
    frontier = [c["init"]]
    while frontier:
        nxt = []
        for s in frontier:
            for i in itertools.product((0, 1), repeat=c["inputs"]):
                t = step(c, s, i)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    nxt.append(t)
        frontier = nxt
    return dist


def test_counter():
    sys = SymbolicSystem(COUNTER)
    r, images = reachable(sys)
    assert sys.states(r) == {(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1)}
    assert images == 6
    assert sys.bdd.size(r) == 4
    seven = sys.cube((1, 1, 1))
    back, _ = backward_reachable(sys, seven)
    assert sys.states(back) == {(1, 1, 1), (0, 1, 1)}
    assert sys.bdd.apply("and", back, r) == 0


def test_random_against_bfs():
    rng = random.Random(1990)
    for _ in range(80):
        nl, ni = rng.randint(2, 5), rng.randint(0, 2)
        c = {"init": tuple(rng.randint(0, 1) for _ in range(nl)), "inputs": ni, "next": [rand_expr(rng, nl, ni, 3) for _ in range(nl)]}
        dist = bfs(c)
        sys = SymbolicSystem(c)
        for frontier in (True, False):
            r, images = reachable(sys, frontier)
            assert sys.states(r) == set(dist)
            assert images == max(dist.values()) + 1
        assert r == sys.bdd.apply("or", r, 0)
        explicit = 0
        for s in dist:
            explicit = sys.bdd.apply("or", explicit, sys.cube(s))
        assert explicit == r


def test_image_and_preimage_by_brute_force():
    rng = random.Random(8)
    for _ in range(40):
        nl, ni = rng.randint(2, 4), rng.randint(0, 2)
        c = {"init": (0,) * nl, "inputs": ni, "next": [rand_expr(rng, nl, ni, 3) for _ in range(nl)]}
        sys = SymbolicSystem(c)
        states = list(itertools.product((0, 1), repeat=nl))
        part = {s for s in states if rng.random() < 0.4}
        f = 0
        for s in part:
            f = sys.bdd.apply("or", f, sys.cube(s))
        inputs = list(itertools.product((0, 1), repeat=ni))
        post = {step(c, s, i) for s in part for i in inputs}
        pre = {s for s in states if any(step(c, s, i) in part for i in inputs)}
        assert sys.states(sys.image(f)) == post
        assert sys.states(sys.preimage(f)) == pre
