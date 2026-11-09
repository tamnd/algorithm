# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-bounded-model-checking/. The authors are listed in prov/3TYGHB.jsonl.

import itertools
import random

from sat_based_bounded_model_checking import Solver, bmc_lasso, bmc_safety, evaluate, step, unroll

X = lambda j: ("x", j)
NOT = lambda a: ("not", a)
AND = lambda a, b: ("and", a, b)
OR = lambda a, b: ("or", a, b)
XOR = lambda a, b: ("xor", a, b)

# A 3-bit counter that counts up when the input is 1. P says "not 7".
COUNTER = {
    "init": (0, 0, 0),
    "inputs": 1,
    "next": [XOR(X(0), ("in", 0)), XOR(X(1), AND(X(0), ("in", 0))), XOR(X(2), AND(AND(X(0), X(1)), ("in", 0)))],
    "prop": NOT(AND(AND(X(0), X(1)), X(2))),
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


def rand_circuit(rng, nl, ni):
    """Random latches; P is true in the initial state, and is either a random
    expression or "the state is not t" for a random state t."""
    init = tuple(rng.randint(0, 1) for _ in range(nl))
    if rng.random() < 0.5:
        t = init
        while t == init:
            t = tuple(rng.randint(0, 1) for _ in range(nl))
        cube = X(0) if t[0] else NOT(X(0))
        for j in range(1, nl):
            cube = AND(cube, X(j) if t[j] else NOT(X(j)))
        prop = NOT(cube)
    else:
        prop = rand_expr(rng, nl, 0, 2)
        if not evaluate(prop, init):
            prop = NOT(prop)
    return {"init": init, "inputs": ni, "next": [rand_expr(rng, nl, ni, 2) for _ in range(nl)], "prop": prop}


def succs(c, s):
    return {step(c, s, i) for i in itertools.product((0, 1), repeat=c["inputs"])}


def shortest_bad(c):
    """Explicit BFS: the length of the shortest path to a state where P is false."""
    dist = {c["init"]: 0}
    frontier = [c["init"]]
    while frontier:
        nxt = []
        for s in frontier:
            if not evaluate(c["prop"], s):
                return dist[s]
            for t in succs(c, s):
                if t not in dist:
                    dist[t] = dist[s] + 1
                    nxt.append(t)
        frontier = nxt
    return None


def eg_not_q(c, q):
    """Explicit check of EG not q at the initial state (greatest fixed point)."""
    z = {s for s in itertools.product((0, 1), repeat=len(c["init"])) if not evaluate(q, s)}
    while True:
        z2 = {s for s in z if succs(c, s) & z}
        if z2 == z:
            return c["init"] in z
        z = z2


def check_trace(c, states, inputs):
    assert states[0] == c["init"]
    for i, ins in enumerate(inputs):
        if i + 1 < len(states):
            assert step(c, states[i], ins) == states[i + 1]


def test_counter_example():
    states, inputs = bmc_safety(COUNTER, 10)
    assert len(states) == 8 and states[-1] == (1, 1, 1)
    check_trace(COUNTER, states, inputs)
    assert bmc_safety(COUNTER, 6) is None
    cnf, _, _ = unroll(COUNTER, 7)
    assert (cnf.nv, len(cnf.clauses)) == (74, 192)


def test_solver_brute_force():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 7)
        cls = [[rng.choice([-1, 1]) * rng.randint(1, n) for _ in range(3)] for _ in range(rng.randint(1, 30))]
        model = Solver(n, cls).solve()
        brute = any(all(any((l > 0) == bits[abs(l) - 1] for l in c) for c in cls) for bits in itertools.product((False, True), repeat=n))
        assert (model is not None) == brute
        if model is not None:
            assert all(any((l > 0) == model[abs(l)] for l in c) for c in cls)


def test_random_safety_against_bfs():
    rng = random.Random(2024)
    for _ in range(60):
        c = rand_circuit(rng, rng.randint(2, 4), rng.randint(0, 2))
        want = shortest_bad(c)
        got = bmc_safety(c, 16)
        if want is None:
            assert got is None
        else:
            states, inputs = got
            assert len(states) - 1 == want
            check_trace(c, states, inputs)
            assert not evaluate(c["prop"], states[-1])
            assert all(evaluate(c["prop"], s) for s in states[:-1])


def test_random_lasso_against_fixed_point():
    rng = random.Random(99)
    for _ in range(50):
        c = rand_circuit(rng, rng.randint(2, 3), rng.randint(0, 1))
        q = rand_expr(rng, len(c["init"]), 0, 2)
        got = bmc_lasso(c, q, 2 ** len(c["init"]))
        assert (got is not None) == eg_not_q(c, q)
        if got is not None:
            states, inputs, l = got
            check_trace(c, states, inputs)
            assert step(c, states[-1], inputs[-1]) == states[l]
            assert not any(evaluate(q, s) for s in states)
