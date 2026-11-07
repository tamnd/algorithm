# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/risch-norman-heuristic/. The authors are listed in prov/XPCGZH.jsonl.
"""Tests for the Risch-Norman heuristic, checked by differentiation.

Integrands are built as derivatives of known answers U0 / B0 + sum c log v
in several towers, so an elementary integral is known to exist. Every
answer is checked by differentiating it with code written here, and the
log coefficients of the normal candidates are compared with the known ones
(they are unique). Known non-elementary integrands must give None.
"""

import random
from fractions import Fraction

import pytest

from risch_norman_heuristic import ansatz_denominator, risch_norman


def F(d):
    return {k: Fraction(v) for k, v in d.items() if v}


def add(*ps):
    r = {}
    for p in ps:
        for e, c in p.items():
            r[e] = r.get(e, Fraction(0)) + c
    return {e: c for e, c in r.items() if c}


def mul(*ps):
    r = ps[0]
    for p in ps[1:]:
        out = {}
        for a, x in r.items():
            for b, y in p.items():
                k = tuple(i + j for i, j in zip(a, b))
                out[k] = out.get(k, Fraction(0)) + x * y
        r = {e: c for e, c in out.items() if c}
    return r


def scale(p, c):
    return {e: v * c for e, v in p.items() if v * c}


def deg(p):
    return max((sum(e) for e in p), default=0)


def dx(p, tower):
    """The true derivative d/dx of p, as a pair (numerator, denominator d)."""
    d, N = tower
    out = {}
    for e, c in p.items():
        if e[0]:
            k = (e[0] - 1,) + e[1:]
            for m, v in d.items():
                kk = tuple(i + j for i, j in zip(k, m))
                out[kk] = out.get(kk, Fraction(0)) + c * e[0] * v
        for i, Ni in enumerate(N):
            if e[i + 1]:
                k = e[:i + 1] + (e[i + 1] - 1,) + e[i + 2:]
                for m, v in Ni.items():
                    kk = tuple(a + b for a, b in zip(k, m))
                    out[kk] = out.get(kk, Fraction(0)) + c * e[i + 1] * v
    return {e: c for e, c in out.items() if c}


def check_derivative(P, Qf, tower, ans):
    """d/dx (U / B + sum c log v) == P / prod q^e, cleared of denominators."""
    U, B, logs = ans
    d = tower[0]
    nv = len(tower[1]) + 1
    one = {tuple([0] * nv): Fraction(1)}
    Q = one
    for q, e in Qf:
        for _ in range(e):
            Q = mul(Q, q)
    W = one
    for _, v in logs:
        W = mul(W, v)
    # d (U/B)' = (DU B - U DB) / B^2 and d (log v)' = Dv / v
    lhs = mul(add(mul(dx(U, tower), B), scale(mul(U, dx(B, tower)), -1)) or {}, W) \
        if U else {}
    for j, (c, v) in enumerate(logs):
        rest = one
        for k, (_, w) in enumerate(logs):
            if k != j:
                rest = mul(rest, w)
        lhs = add(lhs, scale(mul(dx(v, tower) or {tuple([0] * nv): 0}, B, B, rest), c))
    lhs = mul(lhs, Q) if lhs else {}
    rhs = mul(d, P, B, B, W)
    assert add(lhs, scale(rhs, -1)) == {}


def X(nv, i=0, k=1):
    return {tuple(k if j == i else 0 for j in range(nv)): Fraction(1)}


def C(nv, c):
    return {tuple([0] * nv): Fraction(c)} if c else {}


# towers (d, [N_1, ...]): t_i' = N_i / d
RAT = (F({(0,): 1}), [])
EXP = (F({(0, 0): 1}), [F({(0, 1): 1})])                  # t = exp(x)
EXP2 = (F({(0, 0): 1}), [F({(1, 1): 2})])                 # t = exp(x^2)
LOG = (F({(1, 0): 1}), [F({(0, 0): 1})])                  # t = log(x)
TAN = (F({(0, 0): 1}), [F({(0, 0): 1, (0, 2): 1})])       # t = tan(x)
LOGEXP = (F({(1, 0, 0): 1}), [F({(0, 0, 0): 1}), F({(1, 0, 1): 1})])  # log x, exp x


def test_examples():
    # x exp(x^2) -> exp(x^2) / 2
    U, B, logs = risch_norman(F({(1, 1): 1}), [], *EXP2)
    assert U == F({(0, 1): Fraction(1, 2)}) and B == F({(0, 0): 1}) and logs == []
    # log x -> x log x - x
    U, B, logs = risch_norman(F({(0, 1): 1}), [], *LOG)
    assert U == F({(1, 1): 1, (1, 0): -1}) and logs == []
    # tan x -> log(1 + tan^2 x) / 2, with 1 + t^2 as a candidate
    v = F({(0, 0): 1, (0, 2): 1})
    U, B, logs = risch_norman(F({(0, 1): 1}), [], *TAN, extra_logs=(v,))
    assert U == {} and logs == [(Fraction(1, 2), v)]
    # 1 / x -> log x; 1 / (x^2 - 1) -> (log(x - 1) - log(x + 1)) / 2
    U, B, logs = risch_norman(F({(0,): 1}), [(F({(1,): 1}), 1)], *RAT)
    assert U == {} and logs == [(1, F({(1,): 1}))]
    fa, fb = F({(1,): 1, (0,): -1}), F({(1,): 1, (0,): 1})
    U, B, logs = risch_norman(F({(0,): 1}), [(fa, 1), (fb, 1)], *RAT)
    assert U == {} and logs == [(Fraction(1, 2), fa), (Fraction(-1, 2), fb)]
    # 1 / (x log x) -> log(log x)
    t = F({(0, 1): 1})
    U, B, logs = risch_norman(F({(0, 0): 1}), [(F({(1, 0): 1}), 1), (t, 1)], *LOG)
    assert U == {} and logs == [(1, t)]


def test_failures():
    # exp(x^2), exp(x) / x and 1 / (x^2 - 2) have no answer of the guessed form
    for b in range(1, 7):
        assert risch_norman(F({(0, 1): 1}), [], *EXP2, deg_bound=b) is None
        assert risch_norman(F({(0, 1): 1}), [(F({(1, 0): 1}), 1)], *EXP, deg_bound=b) is None
        assert risch_norman(F({(0,): 1}), [(F({(2,): 1, (0,): -2}), 1)], *RAT,
                            deg_bound=b) is None


def test_edges():
    # the zero integrand, a constant, and a polynomial in x only
    assert risch_norman({}, [], *EXP) == ({}, F({(0, 0): 1}), [])
    U, B, logs = risch_norman(F({(0, 0): 3}), [], *EXP)
    assert U == F({(1, 0): 3}) and logs == []
    U, B, logs = risch_norman(F({(4,): 5}), [], *RAT)
    assert U == F({(5,): 1})
    # exp(-x) = 1 / t: t is special, so it stays in the denominator
    U, B, logs = risch_norman(F({(0, 0): 1}), [(F({(0, 1): 1}), 1)], *EXP)
    assert B == F({(0, 1): 1}) and U == F({(0, 0): -1}) and logs == []
    # a deep pole (x - 1)^5 needs many terms in U
    q = F({(1,): 1, (0,): -1})
    U, B, logs = risch_norman(F({(0,): 1}), [(q, 6)], *RAT)
    check_derivative(F({(0,): 1}), [(q, 6)], RAT, (U, B, logs))
    # a degree bound that is too small gives None, a larger one succeeds
    assert risch_norman(F({(1, 1): 1}), [], *EXP, deg_bound=1) is None
    U, B, logs = risch_norman(F({(1, 1): 1}), [], *EXP, deg_bound=2)
    assert U == F({(1, 1): 1, (0, 1): -1})


def pools(name):
    """Irreducible factors that are normal in each tower, coprime to d."""
    if name == "RAT":
        return [F({(1,): 1, (0,): a}) for a in (-3, -1, 2, 5)] + [F({(2,): 1, (0,): 1})]
    if name == "LOGEXP":
        return [F({(1, 0, 0): 1, (0, 0, 0): a}) for a in (-2, 1, 3)] + \
               [F({(0, 1, 0): 1, (0, 0, 0): 1}), F({(0, 0, 1): 1, (1, 0, 0): 1})]
    out = [F({(1, 0): 1, (0, 0): a}) for a in (-2, 1, 3)]
    if name in ("EXP", "EXP2"):
        out += [F({(0, 1): 1, (0, 0): 1}), F({(0, 1): 1, (1, 0): -1})]
    else:
        out += [F({(0, 1): 1, (0, 0): -2}), F({(0, 1): 1, (1, 0): 1})]
    if name == "LOG":
        out = out[1:]  # x - 2 stays, x itself is d
    return out


TOWERS = {"RAT": RAT, "EXP": EXP, "EXP2": EXP2, "LOG": LOG, "TAN": TAN, "LOGEXP": LOGEXP}


def build(rng, name):
    d, N = TOWERS[name]
    nv = len(N) + 1
    one = C(nv, 1)
    mons = [e for e in __import__("itertools").product(range(3), repeat=nv) if sum(e) <= 2]
    U0 = {}
    while deg(U0) == 0:
        U0 = F({m: rng.randint(-3, 3) for m in rng.sample(mons, 3)})
    pool = pools(name)
    rng.shuffle(pool)
    nb, nl = rng.randint(0, 2), rng.randint(0, 2)
    bf = [(q, rng.randint(1, 2)) for q in pool[:nb]]
    if name in ("EXP", "EXP2") and rng.random() < 0.5:
        bf.append((X(nv, 1), rng.randint(1, 2)))  # the special factor t
    lf = [(Fraction(rng.choice([-2, -1, 1, 3])), v) for v in pool[nb:nb + nl]]
    B0 = one
    for q, e in bf:
        for _ in range(e):
            B0 = mul(B0, q)
    W = one
    for _, v in lf:
        W = mul(W, v)
    num = mul(add(mul(dx(U0, (d, N)), B0), scale(mul(U0, dx(B0, (d, N))), -1)) or {}, W)
    for j, (c, v) in enumerate(lf):
        rest = one
        for k, (_, w) in enumerate(lf):
            if k != j:
                rest = mul(rest, w)
        num = add(num, scale(mul(dx(v, (d, N)), B0, B0, rest), c))
    # P / Q with Q = d B0^2 W, the factors listed with their multiplicities
    Qf = [(q, 2 * e) for q, e in bf] + [(v, 1) for _, v in lf]
    if deg(d) > 0:
        Qf.append((d, 1))
    return num, Qf, (d, N), U0, B0, lf, bf


@pytest.mark.parametrize("name", list(TOWERS))
def test_random_constructed(name):
    rng = random.Random(sum(map(ord, name)))
    for _ in range({"RAT": 30, "TAN": 25, "LOGEXP": 8}.get(name, 15)):
        P, Qf, tower, U0, B0, lf, bf = build(rng, name)
        if not P:
            continue
        nv = len(tower[1]) + 1
        B = ansatz_denominator(Qf, tower[0], tower[1], nv)
        bound = deg(U0) + deg(B) - deg(B0)
        ans = risch_norman(P, Qf, *tower, deg_bound=bound)
        assert ans is not None
        check_derivative(P, Qf, tower, ans)
        got = {tuple(sorted(v.items())): c for c, v in ans[2]}
        for c, v in lf:
            assert got.get(tuple(sorted(v.items()))) == c
        for q, _ in bf:
            if q != X(nv, 1):
                assert tuple(sorted(q.items())) not in got
