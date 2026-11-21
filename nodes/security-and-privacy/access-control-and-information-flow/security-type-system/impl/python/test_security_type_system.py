# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/security-type-system/. The authors are listed in prov/8RQ898.jsonl.

import itertools
import random

from security_type_system import expr_level, typecheck

L = frozenset()
H = frozenset({"h"})
GAMMA = {"l": L, "m": L, "h": H}
VARS = ["l", "m", "h"]
DOMAIN = [0, 1, 2]
MOD = 256
FUEL = 200


# An independent oracle: the original "tau var / tau cmd" form of the rules.
# A command gets the type "c cmd", where c is the meet (here the
# intersection) of the levels of the variables it may assign. A branch
# on e is typable when level(e) <= the type of each arm.

TOP = None  # stands for the top of the "tau cmd" order (no assignment)


def meet(a, b):
    if a is TOP:
        return b
    if b is TOP:
        return a
    return a & b


def oracle_level(e, gamma):
    if isinstance(e, int):
        return frozenset()
    if isinstance(e, str):
        return gamma[e]
    return oracle_level(e[1], gamma) | oracle_level(e[2], gamma)


def oracle_cmd_type(c, gamma):
    """Return (ok, write level) for c."""
    tag = c[0]
    if tag == "skip":
        return True, TOP
    if tag == "assign":
        return oracle_level(c[2], gamma) <= gamma[c[1]], gamma[c[1]]
    if tag == "seq":
        ok1, w1 = oracle_cmd_type(c[1], gamma)
        ok2, w2 = oracle_cmd_type(c[2], gamma)
        return ok1 and ok2, meet(w1, w2)
    if tag == "if":
        ok1, w1 = oracle_cmd_type(c[2], gamma)
        ok2, w2 = oracle_cmd_type(c[3], gamma)
        w = meet(w1, w2)
        guard_ok = w is TOP or oracle_level(c[1], gamma) <= w
        return ok1 and ok2 and guard_ok, w
    if tag == "while":
        ok, w = oracle_cmd_type(c[2], gamma)
        guard_ok = w is TOP or oracle_level(c[1], gamma) <= w
        return ok and guard_ok, w
    raise ValueError(tag)


def oracle_typable(c, gamma):
    return oracle_cmd_type(c, gamma)[0]


# A small interpreter, used only to check noninterference by brute force.

def ev(e, s):
    if isinstance(e, int):
        return e % MOD
    if isinstance(e, str):
        return s[e]
    a, b = ev(e[1], s), ev(e[2], s)
    op = e[0]
    if op == "+":
        return (a + b) % MOD
    if op == "-":
        return (a - b) % MOD
    if op == "*":
        return (a * b) % MOD
    if op == "<":
        return int(a < b)
    return int(a == b)


def run(c, s):
    s = dict(s)
    work = [c]
    fuel = FUEL
    while work:
        fuel -= 1
        if fuel < 0:
            return None
        d = work.pop()
        tag = d[0]
        if tag == "assign":
            s[d[1]] = ev(d[2], s)
        elif tag == "seq":
            work.append(d[2])
            work.append(d[1])
        elif tag == "if":
            work.append(d[2] if ev(d[1], s) != 0 else d[3])
        elif tag == "while":
            if ev(d[1], s) != 0:
                work.append(d)
                work.append(d[2])
    return s


def low(s, gamma):
    return tuple(s[x] for x in sorted(gamma) if gamma[x] == frozenset())


def is_tini(c, gamma, variables=VARS):
    seen = {}
    for vals in itertools.product(DOMAIN, repeat=len(variables)):
        s = dict(zip(variables, vals))
        t = run(c, s)
        if t is None:
            continue
        key = low(s, gamma)
        out = low(t, gamma)
        if seen.setdefault(key, out) != out:
            return False
    return True


# Random programs of at most 10 statements.

def rand_expr(rng, variables, depth=0):
    r = rng.random()
    if depth >= 2 or r < 0.35:
        return rng.choice(variables)
    if r < 0.5:
        return rng.randrange(3)
    return (rng.choice(["+", "-", "*", "<", "=="]),
            rand_expr(rng, variables, depth + 1),
            rand_expr(rng, variables, depth + 1))


def rand_cmd(rng, variables, budget):
    """Return (command, statements used)."""
    if budget <= 1:
        return ("assign", rng.choice(variables), rand_expr(rng, variables)), 1
    r = rng.random()
    if r < 0.35:
        return ("assign", rng.choice(variables), rand_expr(rng, variables)), 1
    if r < 0.4:
        return ("skip",), 1
    if r < 0.65:
        c1, n1 = rand_cmd(rng, variables, budget // 2)
        c2, n2 = rand_cmd(rng, variables, budget - n1)
        return ("seq", c1, c2), n1 + n2
    if r < 0.88:
        c1, n1 = rand_cmd(rng, variables, (budget - 1) // 2)
        c2, n2 = rand_cmd(rng, variables, max(1, budget - 1 - n1))
        return ("if", rand_expr(rng, variables), c1, c2), 1 + n1 + n2
    c1, n1 = rand_cmd(rng, variables, budget - 1)
    return ("while", rand_expr(rng, variables), c1), 1 + n1


# Tests.

def test_worked_example():
    # l := 1; if h then m := h else skip  is rejected (m is low).
    prog = ("seq", ("assign", "l", 1),
            ("if", "h", ("assign", "m", "h"), ("skip",)))
    assert not typecheck(prog, GAMMA)
    # The same program with a high target is typable.
    gamma2 = {"l": L, "m": H, "h": H}
    assert typecheck(prog, gamma2)
    assert is_tini(prog, gamma2)


def test_explicit_and_implicit_flows_rejected():
    assert not typecheck(("assign", "l", "h"), GAMMA)
    implicit = ("if", "h", ("assign", "l", 1), ("assign", "l", 0))
    assert not typecheck(implicit, GAMMA)
    assert not is_tini(implicit, GAMMA)
    loop = ("while", "h", ("assign", "l", 1))
    assert not typecheck(loop, GAMMA)


def test_secure_flows_accepted():
    assert typecheck(("assign", "h", "l"), GAMMA)
    assert typecheck(("assign", "l", ("+", "l", "m")), GAMMA)
    assert typecheck(("if", "l", ("assign", "h", 0), ("assign", "m", 1)), GAMMA)
    assert typecheck(("skip",), GAMMA)


def test_incomplete_but_secure_program_rejected():
    # l := h - h always stores 0, so it is secure, but the type system rejects it.
    prog = ("assign", "l", ("-", "h", "h"))
    assert is_tini(prog, GAMMA)
    assert not typecheck(prog, GAMMA)


def test_high_loop_is_typable_and_only_tini():
    # The type system accepts a loop on a secret. It can diverge on some
    # secrets, so the program is TINI but not termination-sensitive.
    prog = ("seq", ("while", "h", ("skip",)), ("assign", "l", 1))
    assert typecheck(prog, GAMMA)
    assert is_tini(prog, GAMMA)
    assert run(prog, {"l": 0, "m": 0, "h": 1}) is None
    assert run(prog, {"l": 0, "m": 0, "h": 0}) is not None


def test_initial_pc():
    assert typecheck(("assign", "h", 1), GAMMA, pc=H)
    assert not typecheck(("assign", "l", 1), GAMMA, pc=H)


def test_expr_level():
    assert expr_level(3, GAMMA) == L
    assert expr_level(("+", "l", ("*", "m", 2)), GAMMA) == L
    assert expr_level(("<", "l", "h"), GAMMA) == H


def test_diamond_lattice():
    a, b = frozenset({"a"}), frozenset({"b"})
    gamma = {"x": L, "y": a, "z": b, "w": a | b}
    assert typecheck(("assign", "w", ("+", "y", "z")), gamma)
    assert not typecheck(("assign", "y", "z"), gamma)
    assert not typecheck(("if", "y", ("assign", "z", 1), ("skip",)), gamma)
    assert typecheck(("if", "y", ("assign", "w", "z"), ("assign", "y", 0)), gamma)


def test_deep_program_no_recursion():
    prog = ("assign", "l", 0)
    for _ in range(5000):
        prog = ("seq", ("assign", "l", ("+", "l", 1)), prog)
    assert typecheck(prog, GAMMA)
    deep = ("assign", "h", 0)
    for _ in range(5000):
        deep = ("if", "l", deep, ("skip",))
    assert typecheck(deep, GAMMA)


def test_random_against_oracle_and_soundness():
    rng = random.Random(8398)
    typable = 0
    for _ in range(600):
        prog, _n = rand_cmd(rng, VARS, rng.randint(1, 10))
        got = typecheck(prog, GAMMA)
        assert got == oracle_typable(prog, GAMMA), prog
        if got:
            typable += 1
            assert is_tini(prog, GAMMA), prog
    assert typable >= 100


def test_random_diamond_against_oracle():
    rng = random.Random(4242)
    a, b = frozenset({"a"}), frozenset({"b"})
    gamma = {"x": L, "y": a, "z": b, "w": a | b}
    names = sorted(gamma)
    for _ in range(500):
        prog, _n = rand_cmd(rng, names, rng.randint(1, 10))
        assert typecheck(prog, gamma) == oracle_typable(prog, gamma), prog
