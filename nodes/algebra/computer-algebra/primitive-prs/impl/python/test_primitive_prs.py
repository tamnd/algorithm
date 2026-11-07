# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primitive-prs/. The authors are listed in prov/1021Z1.jsonl.
import random
from fractions import Fraction
from math import gcd

from primitive_prs import content, prem, primitive_part, primitive_prs


def qstrip(p):
    p = [Fraction(x) for x in p]
    while p and p[0] == 0:
        p.pop(0)
    return p


def qrem(a, b):
    a = qstrip(a)
    while len(a) >= len(b) and a:
        q = a[0] / b[0]
        a = qstrip([x - q * y for x, y in zip(a, b + [0] * (len(a) - len(b)))])
    return a


def euclid_q(f, g):
    """Monic gcd over Q and the list of Euclidean remainders (oracle)."""
    a, b = qstrip(f), qstrip(g)
    if len(a) < len(b):
        a, b = b, a
    rems = [a, b] if b else [a]
    while b:
        a, b = b, qrem(a, b)
        if b:
            rems.append(b)
    if not a:
        return [], rems
    return [x / a[0] for x in a], rems


def mul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def divides(d, p):
    """True if d divides p in Z[x]."""
    p = list(p)
    while len(p) >= len(d) and p:
        if p[0] % d[0]:
            return False
        q = p[0] // d[0]
        for k in range(len(d)):
            p[k] -= q * d[k]
        p = p[1:]
        while p and p[0] == 0:
            p = p[1:]
    return not p


def proportional(a, b):
    return len(a) == len(b) and all(x * b[0] == y * a[0] for x, y in zip(a, b))


def check(f, g):
    G, seq = primitive_prs(f, g)
    monic, rems = euclid_q(f, g)
    if not monic:
        assert G == []
        return
    assert G[0] > 0
    assert proportional([Fraction(x) for x in G], monic)
    cf, cg = content(qint(f)), content(qint(g))
    assert content(G) == gcd(cf, cg) or (not any(g) and content(G) == abs(cf)) or (not any(f) and content(G) == abs(cg))
    assert divides(G, qint(f)) and divides(G, qint(g))
    assert len(seq) == len(rems)
    for s, r in zip(seq, rems):
        assert content(s) == 1 and s[0] > 0
        assert proportional([Fraction(x) for x in s], r)


def qint(p):
    p = list(p)
    while p and p[0] == 0:
        p.pop(0)
    return p


def test_knuth_example():
    u = [1, 0, 1, 0, -3, -3, 8, 2, -5]
    v = [3, 0, 5, 0, -4, -9, 21]
    G, seq = primitive_prs(u, v)
    assert G == [1]
    assert seq[2:] == [[5, 0, -1, 0, 3], [13, 25, -49], [4663, -6150], [1]]
    assert prem(u, v) == [-15, 0, 3, 0, -9]
    check(u, v)


def test_edges():
    assert primitive_prs([], []) == ([], [])
    assert primitive_prs([0, 0], [])[0] == []
    assert primitive_prs([-6, 4], [])[0] == [6, -4]
    assert primitive_prs([], [4])[0] == [4]
    assert primitive_prs([6, 3], [9])[0] == [3]
    assert primitive_prs([7], [5])[0] == [1]
    assert primitive_prs([2, 4], [6, 0, -24])[0] == [2, 4]
    assert primitive_prs([3, 6], [3, 6])[0] == [3, 6]
    assert primitive_part([-4, 6]) == [2, -3] and content([-4, 6]) == -2


def test_random_against_euclid_over_q():
    rng = random.Random(1021)
    for trial in range(600):
        h = [rng.randint(-5, 5) for _ in range(rng.randint(1, 3))]
        a = [rng.randint(-6, 6) for _ in range(rng.randint(1, 5))]
        b = [rng.randint(-6, 6) for _ in range(rng.randint(1, 5))]
        if trial % 2:
            f, g = mul(h, a), mul(h, b)
        else:
            f, g = a, b
        f, g = [rng.choice([1, 2, 3]) * x for x in f], [rng.choice([1, -1, 4]) * x for x in g]
        check(f, g)


def test_many_steps():
    # Consecutive Fibonacci-like pairs force a long sequence of degree drops by one.
    f, g = [1], [1, 1]
    for _ in range(12):
        f, g = g, [a + b for a, b in zip(g + [0], [0] * (len(g) + 1 - len(f)) + f)]
    G, seq = primitive_prs(g, f)
    check(g, f)
    assert len(seq) >= 10
