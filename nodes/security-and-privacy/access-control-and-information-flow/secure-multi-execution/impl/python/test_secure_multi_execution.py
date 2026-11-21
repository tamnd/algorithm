# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-multi-execution/. The authors are listed in prov/5EGZEC.jsonl.

import itertools
import random

from secure_multi_execution import MOD, evaluate, run, sme

L = frozenset()
H = frozenset({"h"})
GAMMA = {"h": H, "l": L, "m": L}
VARS = ["h", "l", "m"]
DOMAIN = [0, 1, 2]
FUEL = 200


# Independent oracle: a recursive interpreter with the same step count.

class OutOfFuel(Exception):
    pass


def o_eval(e, s):
    if isinstance(e, int):
        return e % MOD
    if isinstance(e, str):
        return s[e]
    a, b = o_eval(e[1], s), o_eval(e[2], s)
    return {"+": (a + b) % MOD, "-": (a - b) % MOD, "*": (a * b) % MOD,
            "<": int(a < b), "==": int(a == b)}[e[0]]


def o_exec(c, s, fuel):
    fuel[0] -= 1
    if fuel[0] < 0:
        raise OutOfFuel
    tag = c[0]
    if tag == "assign":
        s[c[1]] = o_eval(c[2], s)
    elif tag == "seq":
        o_exec(c[1], s, fuel)
        o_exec(c[2], s, fuel)
    elif tag == "if":
        o_exec(c[2] if o_eval(c[1], s) else c[3], s, fuel)
    elif tag == "while":
        if o_eval(c[1], s):
            o_exec(c[2], s, fuel)
            o_exec(c, s, fuel)


def o_run(c, s, fuel=FUEL):
    s = dict(s)
    try:
        o_exec(c, s, [fuel])
    except OutOfFuel:
        return None
    return s


def o_sme_two_point(c, s):
    low_run = o_run(c, {"h": 0, "l": s["l"], "m": s["m"]})
    high_run = o_run(c, s)
    return {"h": None if high_run is None else high_run["h"],
            "l": None if low_run is None else low_run["l"],
            "m": None if low_run is None else low_run["m"]}


def stores():
    for vals in itertools.product(DOMAIN, repeat=len(VARS)):
        yield dict(zip(VARS, vals))


def low_in(s):
    return (s["l"], s["m"])


def low_out(r):
    # None stands for "no output": a run that does not end.
    return None if r is None else (r["l"], r["m"])


def is_tsni_plain(c):
    seen = {}
    for s in stores():
        out = low_out(o_run(c, s))
        if seen.setdefault(low_in(s), out) != out:
            return False
    return True


def is_tini_plain(c):
    seen = {}
    for s in stores():
        out = low_out(o_run(c, s))
        if out is None:
            continue
        if seen.setdefault(low_in(s), out) != out:
            return False
    return True


def sme_is_tsni(c):
    seen = {}
    for s in stores():
        r = sme(c, s, GAMMA, fuel=FUEL)
        out = (r["l"], r["m"])
        if seen.setdefault(low_in(s), out) != out:
            return False
    return True


def rand_expr(rng, depth=0):
    r = rng.random()
    if depth >= 2 or r < 0.35:
        return rng.choice(VARS)
    if r < 0.5:
        return rng.randrange(3)
    return (rng.choice(["+", "-", "*", "<", "=="]),
            rand_expr(rng, depth + 1), rand_expr(rng, depth + 1))


def rand_cmd(rng, budget):
    if budget <= 1:
        return ("assign", rng.choice(VARS), rand_expr(rng)), 1
    r = rng.random()
    if r < 0.35:
        return ("assign", rng.choice(VARS), rand_expr(rng)), 1
    if r < 0.4:
        return ("skip",), 1
    if r < 0.65:
        c1, n1 = rand_cmd(rng, budget // 2)
        c2, n2 = rand_cmd(rng, budget - n1)
        return ("seq", c1, c2), n1 + n2
    if r < 0.88:
        c1, n1 = rand_cmd(rng, (budget - 1) // 2)
        c2, n2 = rand_cmd(rng, max(1, budget - 1 - n1))
        return ("if", rand_expr(rng), c1, c2), 1 + n1 + n2
    c1, n1 = rand_cmd(rng, budget - 1)
    return ("while", rand_expr(rng), c1), 1 + n1


def seq(*cs):
    out = cs[-1]
    for c in reversed(cs[:-1]):
        out = ("seq", c, out)
    return out


def test_worked_example():
    # l := h; m := l + 1; h := h + m   with h = 2, l = 5, m = 7.
    prog = seq(("assign", "l", "h"), ("assign", "m", ("+", "l", 1)),
               ("assign", "h", ("+", "h", "m")))
    s = {"h": 2, "l": 5, "m": 7}
    assert run(prog, {"h": 0, "l": 5, "m": 7}) == {"h": 1, "l": 0, "m": 1}
    assert run(prog, s) == {"h": 5, "l": 2, "m": 3}
    assert sme(prog, s, GAMMA) == {"h": 5, "l": 0, "m": 1}


def test_implicit_flow_is_cut():
    prog = ("if", "h", ("assign", "l", 1), ("assign", "l", 0))
    for hv in DOMAIN:
        assert sme(prog, {"h": hv, "l": 9, "m": 0}, GAMMA)["l"] == 0
    assert sme_is_tsni(prog)


def test_termination_channel_is_closed():
    # The plain program leaks h = 0 through termination; SME does not.
    prog = seq(("while", ("==", "h", 0), ("skip",)), ("assign", "l", 1))
    assert not is_tsni_plain(prog)
    assert is_tini_plain(prog)
    assert sme_is_tsni(prog)
    # The low copy sees the default h = 0 and does not end, so SME gives no
    # public output even when the true run ends: SME is not transparent
    # for this TINI program.
    r = sme(prog, {"h": 1, "l": 0, "m": 0}, GAMMA, fuel=FUEL)
    assert run(prog, {"h": 1, "l": 0, "m": 0}, FUEL)["l"] == 1
    assert r["l"] is None and r["h"] == 1


def test_secure_program_is_unchanged():
    prog = seq(("assign", "h", ("+", "h", "l")), ("assign", "m", ("*", "l", 2)))
    for s in stores():
        assert sme(prog, s, GAMMA) == run(prog, s)


def test_only_public_variables():
    gamma = {"a": L, "b": L}
    prog = ("assign", "a", ("+", "a", "b"))
    assert sme(prog, {"a": 1, "b": 2}, gamma) == {"a": 3, "b": 2}


def test_diamond_lattice():
    a, b = frozenset({"a"}), frozenset({"b"})
    gamma = {"x": L, "y": a, "z": b, "w": a | b}
    prog = seq(("assign", "y", ("+", "y", "z")), ("assign", "w", ("+", "y", "z")),
               ("assign", "x", "w"))
    s = {"x": 1, "y": 2, "z": 3, "w": 4}
    r = sme(prog, s, gamma, default=0)
    # Copy a sees x, y; copy b sees x, z; copy a|b sees all.
    assert r == {"x": 0, "y": 2, "z": 3, "w": 8}


def test_evaluate():
    assert evaluate(("-", 1, 2), {}) == MOD - 1
    assert evaluate(("<", "x", 3), {"x": 2}) == 1


def test_deep_program_no_recursion():
    prog = ("assign", "l", 0)
    for _ in range(3000):
        prog = ("seq", ("assign", "l", ("+", "l", 1)), prog)
    assert sme(prog, {"h": 1, "l": 0, "m": 0}, GAMMA)["l"] == 0


def test_random_against_oracle_soundness_precision():
    rng = random.Random(2010)
    tsni_programs = 0
    for _ in range(500):
        prog, _n = rand_cmd(rng, rng.randint(1, 10))
        for s in stores():
            assert run(prog, s, FUEL) == o_run(prog, s)
            assert sme(prog, s, GAMMA, fuel=FUEL) == o_sme_two_point(prog, s)
        assert sme_is_tsni(prog), prog
        if is_tsni_plain(prog):
            tsni_programs += 1
            for s in stores():
                t = o_run(prog, s)
                if t is not None:
                    assert sme(prog, s, GAMMA, fuel=FUEL) == t, (prog, s)
    assert tsni_programs >= 100
