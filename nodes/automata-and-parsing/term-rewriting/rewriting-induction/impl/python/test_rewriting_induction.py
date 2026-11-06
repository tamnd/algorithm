# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rewriting-induction/. The authors are listed in prov/35E48J.jsonl.

import itertools
import random

import pytest

from rewriting_induction import rewriting_induction

Z = ("0",)
NAT = {"0": 0, "s": 1}


def S(t):
    return ("s", t)


def P(a, b):
    return ("+", a, b)


def D(t):
    return ("d", t)


PLUS = [(P(Z, "y"), "y"), (P(S("x"), "y"), S(P("x", "y")))]
DOUBLE = PLUS + [(D(Z), Z), (D(S("x")), S(S(D("x"))))]
PREC = {"0": 0, "s": 1, "+": 2, "d": 3}


# ---------- an independent evaluator on Python integers ----------

class Budget(Exception):
    pass


def o_match(p, n, env):
    """Match a constructor pattern against the natural number n."""
    if isinstance(p, str):
        env[p] = n
        return True
    if p[0] == "0":
        return n == 0
    return n > 0 and o_match(p[1], n - 1, env)


def o_eval(t, R, env, budget):
    budget[0] -= 1
    if budget[0] < 0:
        raise Budget
    if isinstance(t, str):
        return env[t]
    if t[0] == "0":
        return 0
    if t[0] == "s":
        return o_eval(t[1], R, env, budget) + 1
    args = [o_eval(a, R, env, budget) for a in t[1:]]
    if max(args, default=0) > 200:
        raise Budget
    for l, r in R:
        e = {}
        if l[0] == t[0] and all(o_match(p, n, e) for p, n in zip(l[1:], args)):
            return o_eval(r, R, e, budget)
    raise AssertionError("not sufficiently complete")


def o_holds(eq, R, n):
    """Does eq hold for all values 0..n of its variables? None if too costly."""
    vs = sorted({v for side in eq for v in o_vars(side)})
    try:
        for vals in itertools.product(range(n + 1), repeat=len(vs)):
            env = dict(zip(vs, vals))
            b = [20000]
            if o_eval(eq[0], R, env, b) != o_eval(eq[1], R, env, b):
                return False
    except Budget:
        return None
    return True


def o_vars(t):
    if isinstance(t, str):
        return {t}
    return set().union(*(o_vars(a) for a in t[1:])) if len(t) > 1 else set()


# ---------- tests ----------

def test_page_examples():
    r = rewriting_induction(PLUS, [(P("x", Z), "x")], NAT, PREC)
    assert r.verdict == "proved" and r.steps == 3 and r.hypotheses == [(P("x", Z), "x")]
    assoc = (P(P("x", "y"), "z"), P("x", P("y", "z")))
    r = rewriting_induction(PLUS, [assoc], NAT, PREC)
    assert r.verdict == "proved" and r.steps == 3
    # commutativity: the two sides are incomparable in the LPO
    r = rewriting_induction(PLUS, [(P("x", "y"), P("y", "x"))], NAT, PREC)
    assert r.verdict == "unknown" and r.steps == 1
    r = rewriting_induction(PLUS, [(P("x", "y"), "x")], NAT, PREC)
    assert r.verdict == "disproved" and r.witness == (S(Z), Z)


def test_needs_a_lemma():
    """d(x) = x + x diverges alone and is proved with x + s(y) = s(x + y)."""
    goal = (D("x"), P("x", "x"))
    r = rewriting_induction(DOUBLE, [goal], NAT, PREC, max_steps=50)
    assert r.verdict == "unknown" and r.steps == 50
    lemma = (P("x", S("y")), S(P("x", "y")))
    for conj in ([goal, lemma], [lemma, goal]):
        r = rewriting_induction(DOUBLE, conj, NAT, PREC)
        assert r.verdict == "proved" and r.steps == 6


def test_empty_system():
    assert rewriting_induction([], [("x", "x")], NAT, {"0": 0, "s": 1}).verdict == "proved"
    assert rewriting_induction([], [], NAT, {"0": 0, "s": 1}).verdict == "proved"
    r = rewriting_induction([], [("x", "y")], NAT, {"0": 0, "s": 1})
    assert r.verdict == "disproved" and r.witness[0] != r.witness[1]
    r = rewriting_induction([], [(S("x"), "x")], NAT, {"0": 0, "s": 1})
    assert r.verdict == "disproved"


def test_rejects_unoriented_rules():
    loop = [(("f", "x"), ("f", S("x")))]
    with pytest.raises(ValueError):
        rewriting_induction(loop, [(("f", Z), Z)], NAT, {"0": 0, "s": 1, "f": 2})


def test_non_linear_conjectures():
    # x + x = d(x) and d(x) + 0 = x + x share variables between and within sides
    lemma = (P("x", S("y")), S(P("x", "y")))
    r = rewriting_induction(DOUBLE, [lemma, (P("x", "x"), D("x")), (P(D("x"), Z), P("x", "x"))], NAT, PREC)
    assert r.verdict == "proved"
    r = rewriting_induction(DOUBLE, [(P("x", "x"), S(D("x")))], NAT, PREC)
    assert r.verdict == "disproved"


def rand_rhs(rng, depth, vars_, funcs, rec=None):
    """A random right side over vars_, 0, s and the functions funcs; rec, if
    given, is a recursive call head f(x, ...) that may appear once."""
    if depth == 0 or rng.random() < 0.3:
        if vars_ and rng.random() < 0.7:
            return rng.choice(vars_)
        return Z
    choice = rng.random()
    if rec is not None and choice < 0.35:
        name, k, x = rec
        return (name, x) + tuple(rand_rhs(rng, depth - 1, vars_, funcs) for _ in range(k - 1))
    if funcs and choice < 0.75:
        name, k = rng.choice(funcs)
        return (name,) + tuple(rand_rhs(rng, depth - 1, vars_, funcs, rec) for _ in range(k))
    return S(rand_rhs(rng, depth - 1, vars_, funcs, rec))


def random_system(rng):
    """A terminating, orthogonal, sufficiently complete constructor system
    over the naturals, with functions defined by recursion on the first argument."""
    R = []
    funcs = []
    prec = {"0": 0, "s": 1}
    for i in range(rng.randint(1, 3)):
        name, k = f"f{i}", rng.randint(1, 2)
        prec[name] = 2 + i
        ys = ["y"] if k == 2 else []
        if rng.random() < 0.8:
            R.append(((name, Z, *ys), rand_rhs(rng, 2, ys, funcs)))
            R.append(((name, S("x"), *ys), rand_rhs(rng, 3, ["x"] + ys, funcs, (name, k, "x"))))
        else:
            xs = ["x"] + ys
            R.append(((name, *xs), rand_rhs(rng, 3, xs, funcs)))
        funcs.append((name, k))
    return R, funcs, prec


def rand_term(rng, depth, funcs):
    if depth == 0 or rng.random() < 0.25:
        return rng.choice(["x", "y", "x", Z])
    if rng.random() < 0.75:
        name, k = rng.choice(funcs)
        return (name,) + tuple(rand_term(rng, depth - 1, funcs) for _ in range(k))
    return S(rand_term(rng, depth - 1, funcs))


def test_random_against_evaluation():
    rng = random.Random(7)
    counts = {"proved": 0, "disproved": 0, "unknown": 0}
    cases = 0
    while cases < 600:
        R, funcs, prec = random_system(rng)
        pool = [rand_term(rng, 2, funcs) for _ in range(30)]
        conj = []
        for _ in range(rng.randint(1, 2)):
            s, t = rng.choice(pool), rng.choice(pool)
            if rng.random() < 0.5:
                # bias toward true conjectures: pick t with the same values as s on 0..3
                same = [u for u in pool if u != s and o_holds((s, u), R, 3)]
                if same:
                    t = rng.choice(same)
            conj.append((s, t))
        truth = [o_holds(e, R, 4) for e in conj]
        if None in truth:
            continue
        cases += 1
        r = rewriting_induction(R, conj, NAT, prec, max_steps=40)
        counts[r.verdict] += 1
        if r.verdict == "proved":
            assert all(truth), (R, conj)
        elif r.verdict == "disproved":
            a, b = r.witness
            assert a != b and not o_vars(a) and not o_vars(b)
            assert o_holds(r.witness, R, 0) is False
            # some conjecture has a counterexample (searched over a larger range)
            assert any(o_holds(e, R, 12) is False for e in conj), (R, conj)
    assert counts["proved"] >= 100 and counts["disproved"] >= 100, counts
