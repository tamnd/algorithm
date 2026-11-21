# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-sensitive-upgrade/. The authors are listed in prov/V9BYDH.jsonl.

import itertools
import random

from no_sensitive_upgrade import MOD, evaluate, nsu_run, observe

L = frozenset()
H = frozenset({"h"})
LABELS = {"l": L, "m": L, "h": H}
VARS = ["h", "l", "m"]
DOMAIN = [0, 1, 2]
FUEL = 200


# Independent oracle: a recursive big-step form of the same monitor, with
# the same step count (one step per command that starts, and one step per
# test of a loop guard).

class Stop(Exception):
    pass


class OutOfFuel(Exception):
    pass


def o_eval(e, s, lab):
    if isinstance(e, int):
        return e % MOD, frozenset()
    if isinstance(e, str):
        return s[e], lab[e]
    a, la = o_eval(e[1], s, lab)
    b, lb = o_eval(e[2], s, lab)
    op = e[0]
    v = {"+": (a + b) % MOD, "-": (a - b) % MOD, "*": (a * b) % MOD,
         "<": int(a < b), "==": int(a == b)}[op]
    return v, la | lb


def o_exec(c, pc, s, lab, fuel, check=True):
    fuel[0] -= 1
    if fuel[0] < 0:
        raise OutOfFuel
    tag = c[0]
    if tag == "skip":
        return
    if tag == "assign":
        if check and not pc <= lab[c[1]]:
            raise Stop
        v, le = o_eval(c[2], s, lab)
        s[c[1]] = v
        lab[c[1]] = le | pc
    elif tag == "seq":
        o_exec(c[1], pc, s, lab, fuel, check)
        o_exec(c[2], pc, s, lab, fuel, check)
    elif tag == "if":
        v, le = o_eval(c[1], s, lab)
        o_exec(c[2] if v else c[3], pc | le, s, lab, fuel, check)
    elif tag == "while":
        v, le = o_eval(c[1], s, lab)
        if v:
            o_exec(c[2], pc | le, s, lab, fuel, check)
            o_exec(c, pc | le, s, lab, fuel, check)


def oracle(c, s, lab, fuel=FUEL, check=True):
    s, lab = dict(s), dict(lab)
    try:
        o_exec(c, frozenset(), s, lab, [fuel], check)
    except Stop:
        return ("stop", None, None)
    except OutOfFuel:
        return ("diverge", None, None)
    return ("ok", s, lab)


def plain(c, s, fuel=FUEL):
    r = oracle(c, s, {x: frozenset() for x in s}, fuel)
    return r[1]


def stores():
    for vals in itertools.product(DOMAIN, repeat=len(VARS)):
        yield dict(zip(VARS, vals))


def low_part(s):
    return tuple(s[x] for x in VARS if LABELS[x] == L)


def is_tini(run, c):
    seen = {}
    for s in stores():
        status, t, lab = run(c, s)
        if status != "ok":
            continue
        out = observe(t, lab)
        if seen.setdefault(low_part(s), out) != out:
            return False
    return True


def nsu(c, s):
    return nsu_run(c, s, LABELS, FUEL)


def naive(c, s):
    # A monitor that tracks labels but has no check at line L5.
    return oracle(c, s, LABELS, FUEL, check=False)


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


# The worked example: a flow through a branch that is not taken.
FENTON = seq(("assign", "l", 1), ("assign", "m", 1),
             ("if", "h", ("assign", "m", 0), ("skip",)),
             ("if", "m", ("assign", "l", 0), ("skip",)))


def test_worked_example():
    # With h = 0 the run ends and l = 0 is public.
    status, t, lab = nsu_run(FENTON, {"h": 0, "l": 5, "m": 5}, LABELS)
    assert status == "ok"
    assert t["l"] == 0 and lab["l"] == L
    assert lab["m"] == L
    # With h = 1 the assignment m := 0 runs under pc = H to a public m.
    assert nsu_run(FENTON, {"h": 1, "l": 5, "m": 5}, LABELS)[0] == "stop"
    assert is_tini(nsu, FENTON)


def test_naive_monitor_leaks():
    # Without the check of line L5 the final public l equals (h == 0).
    for hv, expect in [(0, 0), (1, 1), (2, 1)]:
        status, t, lab = naive(FENTON, {"h": hv, "l": 5, "m": 5})
        assert status == "ok" and t["l"] == expect and lab["l"] == L
    assert not is_tini(naive, FENTON)


def test_explicit_flow_upgrades_label():
    status, t, lab = nsu_run(("assign", "l", "h"), {"h": 2, "l": 0, "m": 0}, LABELS)
    assert status == "ok" and t["l"] == 2 and lab["l"] == H
    assert observe(t, lab) == (("h", "*"), ("l", "*"), ("m", 0))


def test_flow_sensitive():
    # A public variable may hold a secret for a while and then a public value.
    prog = seq(("assign", "l", "h"), ("assign", "l", 0))
    status, t, lab = nsu_run(prog, {"h": 2, "l": 1, "m": 0}, LABELS)
    assert status == "ok" and lab["l"] == L and t["l"] == 0


def test_secure_program_is_stopped():
    # The program is secure, but NSU stops it: NSU is not complete.
    prog = ("if", "h", ("assign", "l", 0), ("assign", "l", 0))
    assert nsu_run(prog, {"h": 1, "l": 0, "m": 0}, LABELS)[0] == "stop"
    assert all(plain(prog, s)["l"] == 0 for s in stores())


def test_high_target_under_high_pc():
    prog = ("if", "h", ("assign", "h", 0), ("skip",))
    status, t, lab = nsu_run(prog, {"h": 1, "l": 0, "m": 0}, LABELS)
    assert status == "ok" and t["h"] == 0 and lab["h"] == H


def test_pc_ends_with_branch():
    prog = seq(("if", "h", ("skip",), ("skip",)), ("assign", "l", 3))
    status, t, lab = nsu_run(prog, {"h": 1, "l": 0, "m": 0}, LABELS)
    assert status == "ok" and t["l"] == 3 and lab["l"] == L


def test_divergence_and_inputs_unchanged():
    s = {"h": 0, "l": 1, "m": 0}
    lab = dict(LABELS)
    assert nsu_run(("while", 1, ("skip",)), s, lab, fuel=50)[0] == "diverge"
    assert s == {"h": 0, "l": 1, "m": 0} and lab == LABELS


def test_evaluate():
    assert evaluate(("+", "l", ("*", "h", 2)), {"l": 1, "h": 3}, {"l": L, "h": H}) == (7, H)
    assert evaluate(("-", 0, 1), {}, {}) == (MOD - 1, L)


def test_deep_program_no_recursion():
    prog = ("assign", "l", 0)
    for _ in range(3000):
        prog = ("seq", ("assign", "l", ("+", "l", 1)), prog)
    status, t, _lab = nsu_run(prog, {"h": 0, "l": 0, "m": 0}, LABELS)
    assert status == "ok" and t["l"] == 0


def test_random_against_oracle_soundness_transparency():
    rng = random.Random(9512)
    ok_runs = 0
    for _ in range(500):
        prog, _n = rand_cmd(rng, rng.randint(1, 10))
        for s in stores():
            got = nsu(prog, s)
            assert got == oracle(prog, s, LABELS), (prog, s)
            if got[0] == "ok":
                ok_runs += 1
                assert got[1] == plain(prog, s)
        assert is_tini(nsu, prog), prog
    assert ok_runs > 1000
