# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zippel-sparse-interpolation/. The authors are listed in prov/GB4A8V.jsonl.
"""Zippel's probabilistic sparse interpolation over Z/pZ.

Input: a black box f: (Z/pZ)^n -> Z/pZ for a polynomial of degree at most d
in each variable, the number of variables n, the bound d, a prime p and a
random generator. Output: the polynomial as {exponent tuple: coefficient}.

The variables are added one at a time. After stage i the skeleton is the set
of monomials of f(x_1, ..., x_i, a_{i+1}, ..., a_n) for a random anchor a.
Stage i + 1 assumes that adding x_{i+1} keeps the same monomials in
x_1, ..., x_i, finds their coefficients at d + 1 values of x_{i+1} with
transposed Vandermonde systems, and interpolates each coefficient in x_{i+1}.

Cost model: operations in Z/pZ and calls of the black box. With t terms,
the method makes at most (d + 1)(1 + (n - 1) t) probes and
O(n d t (t + d)) field operations (both proved). The answer is correct with
probability at least 1 - n (n - 1) d t / (2 (p - 1)) over the random anchor
(proved in the proof file); otherwise terms can be missing, and no error is
reported. Colliding Vandermonde nodes are detected and only cost a retry.
"""

from __future__ import annotations

import random


def interp_dense(xs: list, ys: list, p: int) -> list:
    """Coefficients (low degree first) of the polynomial through (xs, ys) mod p."""
    n = len(xs)
    coef = list(ys)
    for j in range(1, n):  # Newton divided differences
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) * pow(xs[i] - xs[i - j], p - 2, p) % p
    poly = [0]  # Newton form to monomial form, by Horner's rule
    for i in range(n - 1, -1, -1):
        # poly <- poly * (x - xs[i]) + coef[i]
        nxt = [0] * (len(poly) + 1)
        for k, c in enumerate(poly):
            nxt[k + 1] = (nxt[k + 1] + c) % p
            nxt[k] = (nxt[k] - c * xs[i]) % p
        nxt[0] = (nxt[0] + coef[i]) % p
        poly = nxt
    return poly[:n]


def solve_vandermonde(nodes: list, w: list, p: int) -> list:
    """c with sum_m c_m nodes[m]^k = w[k] for k < T; the nodes are distinct."""
    T = len(nodes)
    lam = [1]  # Lambda(z) = prod (z - v)
    for v in nodes:
        nxt = [0] * (len(lam) + 1)
        for k, c in enumerate(lam):
            nxt[k + 1] = (nxt[k + 1] + c) % p
            nxt[k] = (nxt[k] - c * v) % p
        lam = nxt
    out = []
    for v in nodes:
        q = [0] * T  # Lambda(z) / (z - v) by synthetic division
        acc = 0
        for k in range(T, 0, -1):
            acc = (lam[k] + acc * v) % p
            q[k - 1] = acc
        num = sum(qk * wk for qk, wk in zip(q, w)) % p
        den = 0
        for c in reversed(q):
            den = (den * v + c) % p
        out.append(num * pow(den, p - 2, p) % p)
    return out


def zippel(f, n: int, d: int, p: int, rng: random.Random) -> dict:
    """Sparse interpolation of the black box f with degree at most d in each variable."""
    anchor = [rng.randrange(1, p) for _ in range(n)]          # @line L1
    xs = rng.sample(range(1, p), d + 1)
    ys = [f([x] + anchor[1:]) for x in xs]                    # @line L2
    skel = {(e,) + (0,) * (n - 1): c
            for e, c in enumerate(interp_dense(xs, ys, p)) if c}
    for i in range(1, n):                                     # @line L3
        S = list(skel)
        T = len(S)
        if T == 0:
            return {}
        while True:                                           # @line L4
            r = [rng.randrange(1, p) for _ in range(i)]
            nodes = []
            for m in S:
                v = 1
                for l in range(i):
                    v = v * pow(r[l], m[l], p) % p
                nodes.append(v)
            if len(set(nodes)) == T:
                break
        bs = rng.sample(range(1, p), d + 1)
        vals = []
        for b in bs:                                          # @line L5
            w = []
            for k in range(T):
                pt = [pow(r[l], k, p) for l in range(i)] + [b] + anchor[i + 1:]
                w.append(f(pt))
            vals.append(solve_vandermonde(nodes, w, p))       # @line L6
        new = {}
        for j, m in enumerate(S):                             # @line L7
            cs = interp_dense(bs, [vals[jj][j] for jj in range(d + 1)], p)
            for e, c in enumerate(cs):
                if c:
                    new[m[:i] + (e,) + m[i + 1:]] = c
        skel = new
    return skel                                               # @line L8
