# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ic3-pdr/. The authors are listed in prov/S90VY0.jsonl.

import itertools
import random

from ic3_pdr import evaluate, ic3, step

X = lambda j: ("x", j)
NOT = lambda a: ("not", a)
AND = lambda a, b: ("and", a, b)
OR = lambda a, b: ("or", a, b)

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


def all_states(c):
    return list(itertools.product((0, 1), repeat=len(c["init"])))


def post(c, states):
    return {step(c, s, i) for s in states for i in itertools.product((0, 1), repeat=c["inputs"])}


def models(c, clauses):
    return {s for s in all_states(c) if all(any((s[abs(l) - 1] == 1) == (l > 0) for l in cl) for cl in clauses)}


def reachable(c):
    seen, frontier = {c["init"]}, {c["init"]}
    while frontier:
        frontier = post(c, frontier) - seen
        seen |= frontier
    return seen


class FrameChecker:
    """Check the four frame invariants by brute force after each change."""

    def __init__(self, c):
        self.c, self.calls = c, 0

    def __call__(self, frames, k):
        self.calls += 1
        c = self.c
        sets = [{c["init"]}] + [models(c, f) for f in frames[1:]]
        good = {s for s in all_states(c) if evaluate(c["prop"], s)}
        for i in range(k):
            assert sets[i] <= sets[i + 1]
            assert post(c, sets[i]) <= sets[i + 1]
            assert sets[i] <= good
        for i in range(1, k):
            assert frames[i] >= frames[i + 1]


def check_result(c, verdict, info):
    if verdict == "holds":
        inv = models(c, info)
        assert c["init"] in inv
        assert post(c, inv) <= inv
        assert all(evaluate(c["prop"], s) for s in inv)
    else:
        states, inputs = info
        assert states[0] == c["init"] and len(inputs) == len(states) - 1
        for i, ins in enumerate(inputs):
            assert step(c, states[i], ins) == states[i + 1]
        assert not evaluate(c["prop"], states[-1])


def test_trap():
    checker = FrameChecker(TRAP)
    verdict, inv = ic3(TRAP, checker)
    assert verdict == "holds" and checker.calls > 0
    check_result(TRAP, verdict, inv)
    assert inv == {frozenset({-1}), frozenset({-2})}


def test_random_against_reachability():
    rng = random.Random(4242)
    counts = {"holds": 0, "fails": 0}
    for _ in range(70):
        c = rand_circuit(rng, rng.randint(2, 4), rng.randint(0, 2))
        good = all(evaluate(c["prop"], s) for s in reachable(c))
        verdict, info = ic3(c, FrameChecker(c))
        assert verdict == ("holds" if good else "fails")
        counts[verdict] += 1
        check_result(c, verdict, info)
    assert counts["holds"] >= 15 and counts["fails"] >= 15


def test_counter_with_enable():
    """A 3-bit counter that resets at 5: the state 7 is never reached."""
    x0, x1, x2, en = X(0), X(1), X(2), ("in", 0)
    at5 = AND(AND(x0, NOT(x1)), x2)
    inc0 = ("xor", x0, en)
    inc1 = ("xor", x1, AND(x0, en))
    inc2 = ("xor", x2, AND(AND(x0, x1), en))
    zero = ("const", 0)
    c = {
        "init": (0, 0, 0),
        "inputs": 1,
        "next": [("or", AND(at5, zero), AND(NOT(at5), inc0)), AND(NOT(at5), inc1), AND(NOT(at5), inc2)],
        "prop": NOT(AND(AND(x0, x1), x2)),
    }
    verdict, inv = ic3(c, FrameChecker(c))
    assert verdict == "holds"
    check_result(c, verdict, inv)
    c["prop"] = NOT(at5)
    verdict, cex = ic3(c, FrameChecker(c))
    assert verdict == "fails" and len(cex[0]) == 6
    check_result(c, verdict, cex)
