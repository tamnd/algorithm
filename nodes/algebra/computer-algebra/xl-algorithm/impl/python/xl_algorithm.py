# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xl-algorithm/. The authors are listed in prov/JSBYXR.jsonl.
"""XL (extended linearization) over the prime field GF(p), with field equations.

A polynomial in GF(p)[x_0, ..., x_{n-1}] is a dict {exponent tuple: int mod p}.
All monomials are reduced by x_i^p = x_i, so exponents lie in 0..p-1 and we
look only for solutions in GF(p)^n. Cost model: operations in GF(p).

    xl_step(F, n, p, D)  -> ("none", None) | ("univariate", [g, ...]) | ("fail", None)
    xl_solve(F, n, p)    -> the sorted list of all solutions in GF(p)^n
"""

from __future__ import annotations

from itertools import product


def red_exp(e, p):
    return 0 if e == 0 else 1 + (e - 1) % (p - 1)


def clean(f, p):
    return {e: c % p for e, c in f.items() if c % p}


def reduce_poly(f, p):
    out = {}
    for e, c in f.items():
        k = tuple(red_exp(a, p) for a in e)
        out[k] = (out.get(k, 0) + c) % p
    return clean(out, p)


def mul_mono(f, u, p):
    out = {}
    for e, c in f.items():
        k = tuple(red_exp(a + b, p) for a, b in zip(e, u))
        out[k] = (out.get(k, 0) + c) % p
    return clean(out, p)


def tdeg(f):
    return max((sum(e) for e in f), default=-1)


def monomials(n, p, D):
    """All reduced monomials of total degree at most D."""
    return [e for e in product(range(p), repeat=n) if sum(e) <= D]


def is_univariate(e):
    return all(a == 0 for a in e[1:])


def rref(rows, ncols, p):
    """Reduced row echelon form over GF(p); rows are lists, changed in place."""
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [v * inv % p for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
    return rows[:r]


def xl_step(F, n, p, D):
    """One XL step at degree D. Univariate results are lists of coefficients
    of x_0^0, x_0^1, ... (low degree first)."""
    F = [reduce_poly(f, p) for f in F]
    F = [f for f in F if f]
    rows_p = []
    for f in F:                                          # @line L1
        for u in monomials(n, p, D - tdeg(f)):
            rows_p.append(mul_mono(f, u, p))
    cols = monomials(n, p, D)                            # @line L2
    cols.sort(key=lambda e: (is_univariate(e), -sum(e), [-a for a in e]))
    index = {e: j for j, e in enumerate(cols)}
    M = []
    for g in rows_p:
        row = [0] * len(cols)
        for e, c in g.items():
            row[index[e]] = c
        M.append(row)
    E = rref(M, len(cols), p)                            # @line L3
    first_uni = next((j for j, e in enumerate(cols) if is_univariate(e)), len(cols))
    G = []
    for row in E:                                        # @line L4
        if not any(row[:first_uni]):
            g = [0] * p
            for j in range(first_uni, len(cols)):
                if row[j]:
                    g[cols[j][0]] = row[j]
            G.append(g)
    if any(not any(g[1:]) for g in G):                   # @line L5
        return "none", None
    if G:                                                # @line L6
        return "univariate", G
    return "fail", None                                  # @line L7


def ev_uni(g, a, p):
    s = 0
    for c in reversed(g):
        s = (s * a + c) % p
    return s


def substitute_first(f, a, p):
    out = {}
    for e, c in f.items():
        k = e[1:]
        out[k] = (out.get(k, 0) + c * pow(a, e[0], p)) % p
    return clean(out, p)


def xl_solve(F, n, p, trace=None):
    """All solutions in GF(p)^n, by XL on x_0 and substitution."""
    sols = []
    stack = [(tuple(), [reduce_poly(f, p) for f in F], n)]
    while stack:
        prefix, G, k = stack.pop()
        G = [g for g in G if g]
        if k == 0:                                       # @line S4
            if not G:
                sols.append(prefix)
            continue
        if not G:
            for rest in product(range(p), repeat=k):
                sols.append(prefix + rest)
            continue
        D_full = k * (p - 1) + max(tdeg(g) for g in G)
        D = max(tdeg(g) for g in G)
        while True:                                      # @line S1
            status, U = xl_step(G, k, p, D)
            if status != "fail" or D >= D_full:
                break
            D += 1
        if trace is not None:
            trace.append((k, D, status))
        if status == "none":
            continue
        if status == "univariate":                       # @line S2
            roots = [a for a in range(p) if all(ev_uni(g, a, p) == 0 for g in U)]
        else:
            roots = list(range(p))
        for a in roots:                                  # @line S3
            stack.append((prefix + (a,), [substitute_first(g, a, p) for g in G], k - 1))
    return sorted(sols)
