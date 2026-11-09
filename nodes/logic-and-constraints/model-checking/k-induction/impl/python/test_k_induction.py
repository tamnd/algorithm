# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-induction/. The authors are listed in prov/ZHFE5T.jsonl.

import itertools
import random

from k_induction import evaluate, k_induction, step, step_case

X = lambda j: ("x", j)
NOT = lambda a: ("not", a)
AND = lambda a, b: ("and", a, b)
OR = lambda a, b: ("or", a, b)

# The state (1, 0) is unreachable, loops on itself, and can step to the bad
# state (1, 1). Plain induction never proves P; with simple paths k = 1 works.
TRAP = {
    "init": (0, 0),
    "inputs": 1,
    "next": [X(0), OR(X(1), AND(X(0), ("in", 0)))],
    "prop": NOT(AND(X(0), X(1))),
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


def reachable(c):
    seen = {c["init"]}
    stack = [c["init"]]
    while stack:
        s = stack.pop()
        for i in itertools.product((0, 1), repeat=c["inputs"]):
            t = step(c, s, i)
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


def test_trap_needs_simple_paths():
    assert k_induction(TRAP, 6, simple_path=False) == ("unknown", 6)
    assert k_induction(TRAP, 6) == ("holds", 1)
    assert not step_case(TRAP, 0)


def test_random_against_reachability():
    rng = random.Random(31)
    holds = 0
    for _ in range(80):
        nl = rng.randint(2, 4)
        c = rand_circuit(rng, nl, rng.randint(0, 2))
        good = all(evaluate(c["prop"], s) for s in reachable(c))
        verdict, info = k_induction(c, 2 ** nl)
        assert verdict == ("holds" if good else "fails")
        if good:
            holds += 1
            assert info <= 2 ** nl - 1
        else:
            states, inputs = info
            assert states[0] == c["init"]
            for i, ins in enumerate(inputs):
                assert step(c, states[i], ins) == states[i + 1]
            assert not evaluate(c["prop"], states[-1])
    assert 20 <= holds <= 60


def test_step_case_by_brute_force():
    """The step case without simple paths against enumeration of all paths."""
    rng = random.Random(5)
    for _ in range(40):
        nl = rng.randint(2, 3)
        c = rand_circuit(rng, nl, 1)
        states = list(itertools.product((0, 1), repeat=nl))
        for k in range(3):
            paths = [[s] for s in states if evaluate(c["prop"], s)]
            for _ in range(k):
                paths = [p + [step(c, p[-1], (i,))] for p in paths for i in (0, 1)]
                paths = [p for p in paths if evaluate(c["prop"], p[-1])]
            bad = any(not evaluate(c["prop"], step(c, p[-1], (i,))) for p in paths for i in (0, 1))
            assert step_case(c, k, simple_path=False) == (not bad)
