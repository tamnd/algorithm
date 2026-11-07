# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expression-dag/. The authors are listed in prov/46Z0DH.jsonl.

import random
from fractions import Fraction
from typing import Dict, List, Tuple, Union

import pytest

from expression_dag import ExprDAG

# The oracle: plain nested tuples, with no sharing and no hashing.
# ("c", Fraction) | ("s", name) | (op, left, right) | ("^", base, k)
T = tuple
Poly = Dict[Tuple[int, int], Fraction]


def t_eval(t: T, env: Dict[str, Fraction]) -> Fraction:
    if t[0] == "c":
        return t[1]
    if t[0] == "s":
        return env[t[1]]
    if t[0] == "^":
        return t_eval(t[1], env) ** t[2]
    a, b = t_eval(t[1], env), t_eval(t[2], env)
    return a + b if t[0] == "+" else a - b if t[0] == "-" else a * b


def t_size(t: T) -> int:
    if t[0] in "cs":
        return 1
    if t[0] == "^":
        return 2 + t_size(t[1])
    return 1 + t_size(t[1]) + t_size(t[2])


def pmul(a: Poly, b: Poly) -> Poly:
    r: Poly = {}
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            r[(i + k, j + l)] = r.get((i + k, j + l), 0) + c * d
    return {m: c for m, c in r.items() if c != 0}


def t_expand(t: T) -> Poly:
    if t[0] == "c":
        return {(0, 0): t[1]} if t[1] != 0 else {}
    if t[0] == "s":
        return {(1, 0) if t[1] == "x" else (0, 1): Fraction(1)}
    if t[0] == "^":
        r: Poly = {(0, 0): Fraction(1)}
        a = t_expand(t[1])
        for _ in range(t[2]):
            r = pmul(r, a)
        return r
    a, b = t_expand(t[1]), t_expand(t[2])
    if t[0] == "*":
        return pmul(a, b)
    r = dict(a)
    for m, c in b.items():
        r[m] = r.get(m, 0) + (c if t[0] == "+" else -c)
    return {m: c for m, c in r.items() if c != 0}


def d_expand(D: ExprDAG, u: int) -> Poly:
    """Expansion of a DAG node, through memoization over the distinct nodes."""
    memo: Dict[int, Poly] = {}
    for w in D.reachable(u):
        op = D.op[w]
        if op == "const":
            memo[w] = {(0, 0): D.val[w]} if D.val[w] != 0 else {}
        elif op == "sym":
            memo[w] = {(1, 0) if D.val[w] == "x" else (0, 1): Fraction(1)}
        else:
            a, b = D.kids[w]
            if op == "^":
                r: Poly = {(0, 0): Fraction(1)}
                for _ in range(int(D.val[b])):
                    r = pmul(r, memo[a])
                memo[w] = r
            elif op == "*":
                memo[w] = pmul(memo[a], memo[b])
            else:
                r = dict(memo[a])
                for m, c in memo[b].items():
                    r[m] = r.get(m, 0) + (c if op == "+" else -c)
                memo[w] = {m: c for m, c in r.items() if c != 0}
    return memo[u]


def build(D: ExprDAG, t: T) -> int:
    if t[0] == "c":
        return D.const(t[1])
    if t[0] == "s":
        return D.sym(t[1])
    if t[0] == "^":
        return D.power(build(D, t[1]), t[2])
    a, b = build(D, t[1]), build(D, t[2])
    return {"+": D.add, "-": D.sub, "*": D.mul}[t[0]](a, b)


def rand_tuple(rng: random.Random, depth: int, pool: List[Tuple[T, int]]) -> T:
    """Random tree of height at most depth that often reuses earlier subtrees,
    so the DAG has sharing; pool holds (subtree, height) pairs."""
    fits = [t for t, h in pool if h <= depth]
    if fits and rng.random() < 0.3:
        return rng.choice(fits)
    if depth <= 1 or rng.random() < 0.1:
        r = rng.random()
        t: T = ("c", Fraction(rng.randint(-4, 4), rng.randint(1, 3))) if r < 0.4 else ("s", "x" if r < 0.75 else "y")
        h = 0
    elif rng.random() < 0.15:
        t = ("^", rand_tuple(rng, depth - 2, pool), rng.randint(0, 3))
        h = depth
    else:
        t = (rng.choice("+-*"), rand_tuple(rng, depth - 1, pool), rand_tuple(rng, depth - 1, pool))
        h = depth
    pool.append((t, h))
    return t


def t_d(t: T) -> Poly:
    p = t_expand(t)
    return {(i - 1, j): c * i for (i, j), c in p.items() if i > 0}


def test_worked_example() -> None:
    D = ExprDAG()
    x, y = D.sym("x"), D.sym("y")
    s = D.add(x, y)
    e = D.add(D.mul(s, s), s)  # (x + y)(x + y) + (x + y)
    D.check_invariant()
    assert D.dag_size(e) == 5 and D.tree_size(e) == 11
    assert D.add(D.sym("x"), D.sym("y")) == s  # hash consing finds the old node
    assert len(D.op) == 5
    assert D.eval(e, {"x": 1, "y": 2}) == 12
    de = D.diff(e, "x")  # 2(x + y) + 1
    assert D.eval(de, {"x": 1, "y": 2}) == 7
    assert d_expand(D, de) == {(1, 0): 2, (0, 1): 2, (0, 0): 1}


def test_repeated_squaring() -> None:
    D = ExprDAG()
    u = D.add(D.sym("x"), D.const(1))
    for _ in range(40):
        u = D.mul(u, u)
    D.check_invariant()
    assert D.dag_size(u) == 43
    assert D.tree_size(u) == 2 ** 42 - 1
    assert D.eval(u, {"x": 0}) == 1
    assert D.eval(u, {"x": Fraction(-2)}) == 1
    D2 = ExprDAG()
    w = D2.add(D2.sym("x"), D2.const(1))
    for _ in range(12):
        w = D2.mul(w, w)
    assert D2.eval(w, {"x": 1}) == 2 ** 4096
    assert D2.eval(D2.diff(w, "x"), {"x": 0}) == 4096
    assert D2.dag_size(D2.diff(w, "x")) <= 6 * 15


def test_edge_cases() -> None:
    D = ExprDAG()
    z = D.const(0)
    assert D.eval(z, {}) == 0 and D.diff(z, "x") == z
    assert D.const(Fraction(2, 4)) == D.const(Fraction(1, 2))
    x = D.sym("x")
    assert D.diff(x, "x") == D.const(1) and D.diff(x, "y") == z
    assert D.diff(D.power(x, 0), "x") == z
    assert D.diff(D.power(x, 1), "x") == D.const(1)
    assert D.subs(z, "x", x) == z
    assert D.subs(x, "x", x) == x
    with pytest.raises(ValueError):
        D.power(x, -2)
    D.check_invariant()


def test_long_chain() -> None:
    D = ExprDAG()
    u = D.sym("x")
    for i in range(30000):
        u = D.add(u, D.const(i % 3))
    assert D.eval(u, {"x": 0}) == 30000
    assert D.eval(D.diff(u, "x"), {"x": 5}) == 1
    D.check_invariant()


def test_random_against_tuple_oracle() -> None:
    rng = random.Random(46)
    for _ in range(600):
        D = ExprDAG()
        pool: List[Tuple[T, int]] = []
        ts = [rand_tuple(rng, rng.randint(2, 8), pool) for _ in range(3)]
        ids = [build(D, t) for t in ts]
        D.check_invariant()
        # hash consing: equal ids exactly for equal trees
        for i in range(3):
            assert build(D, ts[i]) == ids[i]
            for j in range(3):
                assert D.equal(ids[i], ids[j]) == (ts[i] == ts[j])
        e, r = ids[0], ids[1]
        assert D.tree_size(e) == t_size(ts[0])
        env = {"x": Fraction(rng.randint(-5, 5), rng.randint(1, 3)), "y": Fraction(rng.randint(-5, 5))}
        assert D.eval(e, env) == t_eval(ts[0], env)
        assert Fraction(eval(D.to_string(e), {"Fraction": Fraction}, dict(env))) == t_eval(ts[0], env)
        de = D.diff(e, "x")
        assert d_expand(D, de) == t_d(ts[0])
        se = D.subs(e, "x", r)
        assert D.eval(se, env) == t_eval(ts[0], {"x": t_eval(ts[1], env), "y": env["y"]})
        assert D.subs(e, "q", r) == e
        D.check_invariant()
