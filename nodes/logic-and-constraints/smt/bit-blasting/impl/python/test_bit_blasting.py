# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-blasting/. The authors are listed in prov/65V2ET.jsonl.

import itertools
import random

from bit_blasting import Blaster, blast, dpll, evaluate, evaluate_term, simulate, solve, value_of

X, Y, Z = ("var", "x"), ("var", "y"), ("var", "z")
BINARY = ["and", "or", "xor", "add", "sub", "mul"]
UNARY = ["not", "neg"]
ATOMS = ["eq", "ult", "ule", "slt"]


def satisfied(clauses: list[list[int]], val: list[bool]) -> bool:
    return all(any(val[a] if a > 0 else not val[-a] for a in c) for c in clauses)


def terms(w: int) -> list[tuple]:
    ts = [(op, X, Y) for op in BINARY] + [(op, X) for op in UNARY]
    ts += [("shl", X, k) for k in range(w + 1)] + [("lshr", X, k) for k in range(w + 1)]
    ts += [("add", ("mul", X, ("const", 3)), ("const", 5))]
    return ts


def test_page_example() -> None:
    # x + 1 <u x holds only for the largest value, by overflow.
    f = ("ult", ("add", X, ("const", 1)), X)
    assert solve(f, 4) == {"x": 15}
    assert [x for x in range(16) if evaluate(f, 4, {"x": x})] == [15]
    # The adder trace on 3 bits: 5 + 3 = 8 = 0 modulo 8.
    bb = Blaster(3)
    s = bb.term(("add", X, Y))
    val = simulate(bb, {"x": 5, "y": 3})
    assert value_of(s, val) == 0
    # x * y = 15 with 1 < x <= y on 4 bits: the models are (3, 5), (7, 9) and (11, 13).
    g = ("band", ("eq", ("mul", X, Y), ("const", 15)), ("band", ("ult", ("const", 1), X), ("ule", X, Y)))
    m = solve(g, 4)
    assert m is not None and evaluate(g, 4, m)
    brute = [(x, y) for x in range(16) for y in range(16) if evaluate(g, 4, {"x": x, "y": y})]
    assert brute == [(3, 5), (7, 9), (11, 13)]


def test_circuits_match_python_on_all_inputs() -> None:
    for w in range(1, 5):
        for t in terms(w):
            bb = Blaster(w)
            out = bb.term(t)
            bb.variable("x")
            bb.variable("y")
            for x, y in itertools.product(range(1 << w), repeat=2):
                env = {"x": x, "y": y}
                val = simulate(bb, env)
                assert value_of(out, val) == evaluate_term(t, w, env), (t, w, env)
                assert satisfied(bb.clauses, val)


def test_atoms_match_python_on_all_inputs() -> None:
    for w in range(1, 5):
        for op in ATOMS:
            bb = Blaster(w)
            out = bb.formula((op, X, Y))
            for x, y in itertools.product(range(1 << w), repeat=2):
                env = {"x": x, "y": y}
                val = simulate(bb, env)
                got = val[out] if out > 0 else not val[-out]
                assert got == evaluate((op, X, Y), w, env), (op, w, env)


def test_cnf_forces_the_outputs() -> None:
    # With the inputs fixed by unit clauses, the CNF has exactly the right output:
    # adding a clause that says "some output bit is wrong" makes it unsatisfiable.
    rng = random.Random(65)
    for w in (1, 2, 3):
        for t in terms(w):
            bb = Blaster(w)
            out = bb.term(t)
            bb.variable("x")
            bb.variable("y")
            pairs = list(itertools.product(range(1 << w), repeat=2))
            if w == 3:
                pairs = rng.sample(pairs, 6)
            for x, y in pairs:
                env = {"x": x, "y": y}
                units = [[b if (env[n] >> i) & 1 else -b] for n in "xy" for i, b in enumerate(bb.vars[n])]
                want = evaluate_term(t, w, env)
                wrong = [[-b if (want >> i) & 1 else b for i, b in enumerate(out)]]
                assert dpll(bb.clauses + units + wrong, bb.nvars) is None
                val = dpll(bb.clauses + units, bb.nvars)
                assert val is not None and value_of(out, val) == want


def random_term(rng: random.Random, depth: int) -> tuple:
    if depth == 0 or rng.random() < 0.3:
        if rng.random() < 0.75:
            return rng.choice([X, Y, Z])
        return ("const", rng.randrange(8))
    r = rng.random()
    if r < 0.15:
        return (rng.choice(UNARY), random_term(rng, depth - 1))
    if r < 0.25:
        return (rng.choice(["shl", "lshr"]), random_term(rng, depth - 1), rng.randrange(3))
    return (rng.choice(BINARY), random_term(rng, depth - 1), random_term(rng, depth - 1))


def random_formula(rng: random.Random) -> tuple:
    atoms = [(rng.choice(ATOMS), random_term(rng, 2), random_term(rng, 2)) for _ in range(rng.randint(1, 3))]
    atoms = [a if rng.random() < 0.7 else ("bnot", a) for a in atoms]
    f = atoms[0]
    for a in atoms[1:]:
        f = (rng.choice(["band", "band", "bor"]), f, a)
    return f


def test_solve_against_brute_force() -> None:
    rng = random.Random(2006)
    w = 3
    seen = {True: 0, False: 0}
    for _ in range(120):
        f = random_formula(rng)
        envs = [dict(zip("xyz", v)) for v in itertools.product(range(1 << w), repeat=3)]
        truth = any(evaluate(f, w, e) for e in envs)
        m = solve(f, w)
        assert (m is not None) == truth, f
        if m is not None:
            full = {"x": 0, "y": 0, "z": 0, **m}
            assert evaluate(f, w, full), (f, m)
        seen[truth] += 1
    assert seen[True] > 10 and seen[False] > 10


def test_blast_adds_output_unit() -> None:
    bb, out = blast(("eq", X, X), 3)
    assert out == 1 and [out] in bb.clauses
    assert solve(("bnot", ("eq", X, X)), 3) is None
