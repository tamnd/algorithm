# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regular-chain/. The authors are listed in prov/1VMKVR.jsonl.
"""Tests against the zero sets of the components of each chain.

Every random chain is built so that its quasi-component is a union of explicit
graphs (one per choice of root in each factored polynomial). Then p is in
sat(T) when p vanishes on every graph, and p is regular when p vanishes on
no graph. These facts are checked at random rational points.
"""

import itertools
import random
from fractions import Fraction as Q

from regular_chain import (add, mul, mono, clean, prem, prem_chain, init, mvar,
                           resultant, iterated_resultant, is_regular,
                           is_regular_chain, in_saturation, exact_div, deg, coeff)

N = 4


def const(c):
    return {(0,) * N: Q(c)} if c else {}


def X(i):
    return mono(N, i, 1)


def ev(p, pt):
    s = Q(0)
    for e, c in p.items():
        t = c
        for v, k in zip(pt, e):
            if k:
                t *= v ** k
        s += t
    return s


def rand_poly(rng, vars_, terms=3, maxdeg=2):
    p = {}
    for _ in range(terms):
        e = [0] * N
        for v in vars_:
            e[v] = rng.randint(0, maxdeg)
        if sum(e) > maxdeg + 1:
            continue
        p = add(p, {tuple(e): Q(rng.randint(-4, 4))})
    return p


def rand_chain(rng):
    """Return (T, spec, regular); spec drives point sampling."""
    mv = sorted(rng.sample([1, 2, 3], rng.randint(1, 3)))
    T, spec = [], []
    for i in mv:
        low = list(range(i))
        h = rand_poly(rng, low, 2, 1) or const(1)
        if rng.random() < 0.3 or not mvar(h) >= 0:
            h = add(h, const(rng.randint(1, 3))) or const(1)
        if spec and rng.random() < 0.4:
            j, kind, data = spec[rng.randrange(len(spec))]
            if kind == "two":   # an initial that vanishes on one branch
                h = add(X(j), data[0], -1)
        if rng.random() < 0.5:
            g = rand_poly(rng, low, 2, 1)
            T.append(add(mul(h, X(i)), g, -1))
            spec.append((i, "lin", (h, g)))
        else:
            a = add(rand_poly(rng, low, 2, 1), const(0))
            b = add(a, const(rng.choice([-3, -2, -1, 1, 2, 5])))
            t = mul(h, mul(add(X(i), a, -1), add(X(i), b, -1)))
            T.append(t)
            spec.append((i, "two", (a, b, h)))
    return T, spec


def branches(spec):
    two = [k for k, s in enumerate(spec) if s[1] == "two"]
    for choice in itertools.product([0, 1], repeat=len(two)):
        yield dict(zip(two, choice))


def sample(rng, spec, br, upto=None):
    """A random point of the graph for branch br, using spec[:upto]."""
    spec = spec[:upto] if upto is not None else spec
    for _ in range(50):
        pt = [Q(rng.randint(-10 ** 4, 10 ** 4)) for _ in range(N)]
        ok = True
        for k, (i, kind, data) in enumerate(spec):
            h = data[0] if kind == "lin" else data[2]
            hv = ev(h, pt)
            if hv == 0:
                ok = False
                break
            if kind == "lin":
                pt[i] = ev(data[1], pt) / hv
            else:
                pt[i] = ev(data[br[k]], pt)
        if ok:
            return pt
    return None


def vanishes_on(p, rng, spec, br, upto=None, k=5):
    for _ in range(k):
        pt = sample(rng, spec, br, upto)
        if pt is None:
            return True  # an initial vanishes on this branch
        if ev(p, pt) != 0:
            return False
    return True


def ref_regular_chain(T, spec, rng):
    for k in range(1, len(T)):
        h = init(T[k])
        for br in branches(spec[:k]):
            if vanishes_on(h, rng, spec, br, k):
                return False
    return True


def test_prem_identity():
    rng = random.Random(1)
    for _ in range(150):
        q = rand_poly(rng, range(N), 4, 2)
        p = rand_poly(rng, range(N), 5, 3)
        if mvar(q) < 0:
            continue
        i = mvar(q)
        r = prem(p, q)
        assert deg(r, i) < deg(q, i)
        h, found = init(q), False
        for e in range(max(deg(p, i) - deg(q, i) + 2, 1)):
            hp = dict(p)
            for _ in range(e):
                hp = mul(hp, h)
            diff = add(hp, r, -1)
            try:
                quo = exact_div(diff, q) if diff else {}
            except AssertionError:
                continue
            if add(mul(quo, q), diff, -1) == {}:
                found = True
                break
        assert found


def sylv_det_num(cp, cq):
    dp, dq = len(cp) - 1, len(cq) - 1
    n = dp + dq
    M = [[Q(0)] * n for _ in range(n)]
    for r in range(dq):
        for j, c in enumerate(cp):
            M[r][r + j] = c
    for r in range(dp):
        for j, c in enumerate(cq):
            M[dq + r][r + j] = c
    det = Q(1)
    for k in range(n):
        piv = next((r for r in range(k, n) if M[r][k] != 0), None)
        if piv is None:
            return Q(0)
        if piv != k:
            M[k], M[piv] = M[piv], M[k]
            det = -det
        det *= M[k][k]
        for r in range(k + 1, n):
            f = M[r][k] / M[k][k]
            for j in range(k, n):
                M[r][j] -= f * M[k][j]
    return det


def test_resultant_specializes():
    rng = random.Random(2)
    for _ in range(40):
        p = add(rand_poly(rng, [0, 1, 2], 4, 2), mono(N, 2, 2))
        q = add(rand_poly(rng, [0, 1, 2], 3, 2), mono(N, 2, 1, 3))
        r = resultant(p, q, 2)
        for _ in range(3):
            pt = [Q(rng.randint(-9, 9)) for _ in range(N)]
            cp = [ev(coeff(p, 2, k), pt) for k in range(deg(p, 2), -1, -1)]
            cq = [ev(coeff(q, 2, k), pt) for k in range(deg(q, 2), -1, -1)]
            assert ev(r, pt) == sylv_det_num(cp, cq)


def test_random_chains():
    rng = random.Random(3)
    seen = {True: 0, False: 0, "mem": 0, "non": 0, "zd": 0}
    for _ in range(80):
        T, spec = rand_chain(rng)
        reg = ref_regular_chain(T, spec, rng)
        assert is_regular_chain(T) == reg
        seen[reg] += 1
        if not reg:
            continue
        brs = list(branches(spec))
        cands = [rand_poly(rng, range(N), 3, 1)]
        comb = {}
        for t in T:
            comb = add(comb, mul(rand_poly(rng, range(N), 1, 1), t))
        cands.append(comb)
        for (i, kind, data) in spec:
            if kind == "two":
                f = add(X(i), data[0], -1)
                cands.append(add(mul(f, add(X(i), data[1], -1)), comb))  # in sat(T)
                cands.append(add(f, comb))  # a zero divisor
        for p in cands:
            van = [vanishes_on(p, rng, spec, br) for br in brs]
            assert in_saturation(p, T) == all(van)
            assert is_regular(p, T) == (not any(van))
            seen["mem" if all(van) else ("zd" if any(van) else "non")] += 1
    assert min(seen.values()) >= 3, seen


def test_hand_examples():
    x1, x2, x3 = X(1), X(2), X(3)
    t1 = add(mul(X(0), x1), X(0), -1)            # x0*x1 - x0, sat = (x1 - 1)
    T = [t1]
    assert is_regular_chain(T)
    assert in_saturation(add(x1, const(1), -1), T)
    assert not in_saturation(x1, T)
    # x1^2 - x0^2 and (x1 - x0) x2 - 1 is not regular: init x1 - x0 is a zero divisor
    s1 = add(mul(x1, x1), mul(X(0), X(0)), -1)
    s2 = add(mul(add(x1, X(0), -1), x2), const(1), -1)
    assert not is_regular_chain([s1, s2])
    assert is_regular_chain([s1, add(mul(x1, x2), const(1), -1)])
    # worked example of the page: x1^2 - 2, x1 x2 - 1, x2 x3^2 - x1
    T = [add(mul(x1, x1), const(2), -1), add(mul(x1, x2), const(1), -1),
         add(mul(x2, mul(x3, x3)), x1, -1)]
    assert is_regular_chain(T)
    assert prem_chain(mul(x3, x3), T) == x1          # the page example
    q = add(mul(x3, x3), const(2), -1)
    assert in_saturation(q, T)
    assert not in_saturation(add(x3, const(1), -1), T)
    assert is_regular(add(x3, const(1), -1), T)
    assert not is_regular(add(x3, x1, -1), T)        # vanishes where x3 = x1
    assert not in_saturation(add(x3, x1, -1), T)


def test_edges():
    z = {}
    assert in_saturation(z, [])
    assert not is_regular(z, [])
    assert is_regular(const(5), [])
    assert not in_saturation(const(5), [])
    assert is_regular_chain([])
    assert not is_regular_chain([const(3)])
    assert not is_regular_chain([X(2), X(1)])
    assert in_saturation(z, [X(1)])
    assert iterated_resultant(const(7), [X(1)]) == const(7)
    assert not is_regular(X(1), [X(1)])
    assert is_regular(add(X(1), const(1)), [X(1)])
