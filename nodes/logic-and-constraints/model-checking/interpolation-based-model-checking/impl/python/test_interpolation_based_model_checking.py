# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interpolation-based-model-checking/. The authors are listed in prov/6ZZFCD.jsonl.

import itertools
import random

from interpolation_based_model_checking import Solver, evaluate, itp_check, step

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


def reachable(c):
    seen, frontier = {c["init"]}, {c["init"]}
    while frontier:
        frontier = post(c, frontier) - seen
        seen |= frontier
    return seen


def states_of(c, f):
    return {s for s in all_states(c) if evaluate(f, s)}


def reaches_bad(c, s, steps):
    """True when s can reach a state where P is false in at most steps steps."""
    cur = {s}
    for _ in range(steps + 1):
        if any(not evaluate(c["prop"], t) for t in cur):
            return True
        cur = post(c, cur)
    return False


def test_interpolants_of_random_cnf():
    """A implies I, I and B is unsatisfiable, and I uses only shared variables."""
    rng = random.Random(11)
    done = 0
    while done < 150:
        n = rng.randint(2, 8)
        cls = [[rng.choice([-1, 1]) * rng.randint(1, n) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(2, 26))]
        n_a = rng.randint(1, len(cls) - 1)
        va = {abs(l) for c in cls[:n_a] for l in c}
        vb = {abs(l) for c in cls[n_a:] for l in c}
        s = Solver(n, cls, n_a, {v: X(v) for v in va & vb})
        sat = lambda part, bits: all(any((l > 0) == bits[abs(l)] for l in c) for c in part)
        rows = [(0,) + b for b in itertools.product((0, 1), repeat=n)]
        brute = any(sat(cls, r) for r in rows)
        if s.solve() is not None:
            assert brute
            continue
        assert not brute
        done += 1
        itp = s.interpolant
        for r in rows:
            if sat(cls[:n_a], r):
                assert evaluate(itp, r)
            if sat(cls[n_a:], r):
                assert not evaluate(itp, r)
        assert all(evaluate(itp, r) == evaluate(itp, tuple(r[v] if v in va & vb else 0 for v in range(n + 1))) for r in rows)


def run_checked(c):
    """itp_check with each interpolant checked by brute force."""

    def observer(r, j, k):
        rs, js = states_of(c, r), states_of(c, j)
        assert post(c, rs) <= js
        assert not any(reaches_bad(c, s, k - 1) for s in js)

    return itp_check(c, 64, observer)


def check_result(c, verdict, info):
    if verdict == "holds":
        inv = states_of(c, info)
        assert c["init"] in inv and post(c, inv) <= inv
        assert all(evaluate(c["prop"], s) for s in inv)
    else:
        states, inputs = info
        assert states[0] == c["init"]
        for i, ins in enumerate(inputs):
            assert step(c, states[i], ins) == states[i + 1]
        assert not evaluate(c["prop"], states[-1])


def test_trap():
    verdict, inv = run_checked(TRAP)
    assert verdict == "holds"
    check_result(TRAP, verdict, inv)


def test_random_against_reachability():
    rng = random.Random(777)
    counts = {"holds": 0, "fails": 0}
    for _ in range(60):
        c = rand_circuit(rng, rng.randint(2, 4), rng.randint(0, 2))
        good = all(evaluate(c["prop"], s) for s in reachable(c))
        verdict, info = run_checked(c)
        assert verdict == ("holds" if good else "fails")
        counts[verdict] += 1
        check_result(c, verdict, info)
    assert counts["holds"] >= 15 and counts["fails"] >= 15
