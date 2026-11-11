# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secret-sharing/. The authors are listed in prov/P8BB3K.jsonl.
"""Three secret sharing schemes over a prime field GF(p).

1. Additive n-of-n sharing: s = s_1 + ... + s_n mod p.
2. Blakley's t-of-n scheme (1979): the secret is the first coordinate of a
   point x in GF(p)^t, and each party gets a hyperplane a_i . x = b_i through
   it. Any t hyperplanes meet in x. The dealer picks the normals so that any t
   of them are independent and e_1 is not in the span of any t - 1 of them,
   which makes the scheme perfect.
3. Benaloh-Leichter (1988) for a monotone formula of AND and OR gates over
   the parties: an OR gate gives its value to every child, an AND gate splits
   its value additively among its children, and each leaf gives its value to
   its party.

Shamir's scheme has its own page and code.

For study only. The code is not constant time and must not be used to protect
real data. Use a reviewed implementation built on libsodium or a FIPS 140
validated module.
"""

import itertools
import secrets


def field_rand(p):
    return lambda: secrets.randbelow(p)


# ------------------------------------------------------------ additive n-of-n
def additive_share(s, n, p, rand=None):
    rand = rand or field_rand(p)
    shares = [rand() for _ in range(n - 1)]
    shares.append((s - sum(shares)) % p)
    return shares


def additive_reconstruct(shares, p):
    return sum(shares) % p


# ------------------------------------------------------------ linear algebra mod p
def solve(rows, rhs, p):
    """Solve rows . x = rhs mod p by Gaussian elimination; None if singular."""
    n = len(rows)
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] % p), None)
        if piv is None:
            return None
        m[col], m[piv] = m[piv], m[col]
        inv = pow(m[col][col], -1, p)
        m[col] = [v * inv % p for v in m[col]]
        for r in range(n):
            if r != col and m[r][col]:
                f = m[r][col]
                m[r] = [(a - f * b) % p for a, b in zip(m[r], m[col])]
    return [m[r][n] for r in range(n)]


def rank(rows, p):
    m = [list(r) for r in rows]
    rk, cols = 0, len(m[0]) if m else 0
    for col in range(cols):
        piv = next((r for r in range(rk, len(m)) if m[r][col] % p), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        inv = pow(m[rk][col], -1, p)
        m[rk] = [v * inv % p for v in m[rk]]
        for r in range(len(m)):
            if r != rk and m[r][col]:
                f = m[r][col]
                m[r] = [(a - f * b) % p for a, b in zip(m[r], m[rk])]
        rk += 1
    return rk


# ------------------------------------------------------------ Blakley
def blakley_normals_ok(normals, t, p):
    """Any t normals are independent, and e_1 is outside the span of any t - 1."""
    e1 = [1] + [0] * (t - 1)
    for sub in itertools.combinations(normals, t):
        if rank(sub, p) < t:
            return False
    for sub in itertools.combinations(normals, t - 1):
        if rank(list(sub) + [e1], p) < t:
            return False
    return True


def blakley_normals(t, n, p, rand=None):
    """Public normals a_1..a_n in GF(p)^t; retry until the conditions hold."""
    rand = rand or field_rand(p)
    for _ in range(10000):
        normals = [[rand() for _ in range(t)] for _ in range(n)]
        if blakley_normals_ok(normals, t, p):
            return normals
    raise ValueError("p is too small for these t and n")


def blakley_share(s, normals, p, rand=None):
    """Share b_i = a_i . x for a point x whose first coordinate is s."""
    rand = rand or field_rand(p)
    t = len(normals[0])
    x = [s % p] + [rand() for _ in range(t - 1)]
    return [sum(a * v for a, v in zip(normal, x)) % p for normal in normals]


def blakley_reconstruct(normals, ids, values, p):
    """The secret from the shares of the t parties `ids`."""
    x = solve([normals[i] for i in ids], values, p)
    return None if x is None else x[0]


# ------------------------------------------------------------ Benaloh-Leichter
# A formula is a party number (an int) or a tuple ("and" | "or", child, ...).
def bl_share(s, formula, p, rand=None):
    """Return {party: [(leaf, value), ...]}; leaves are numbered left to right."""
    rand = rand or field_rand(p)
    out, counter = {}, [0]

    def walk(value, node):
        if isinstance(node, int):
            out.setdefault(node, []).append((counter[0], value))
            counter[0] += 1
        elif node[0] == "or":
            for child in node[1:]:
                walk(value, child)
        else:
            parts = additive_share(value, len(node) - 1, p, rand)
            for part, child in zip(parts, node[1:]):
                walk(part, child)

    walk(s % p, formula)
    return out


def bl_satisfies(formula, parties):
    if isinstance(formula, int):
        return formula in parties
    results = [bl_satisfies(c, parties) for c in formula[1:]]
    return any(results) if formula[0] == "or" else all(results)


def bl_reconstruct(formula, shares, p):
    """The secret from {party: [(leaf, value)]} of an authorized set, else None."""
    leaf_value = {leaf: v for lst in shares.values() for leaf, v in lst}
    counter = [0]

    def walk(node):
        if isinstance(node, int):
            leaf = counter[0]
            counter[0] += 1
            return leaf_value.get(leaf)
        vals = [walk(c) for c in node[1:]]
        if node[0] == "or":
            return next((v for v in vals if v is not None), None)
        if any(v is None for v in vals):
            return None
        return sum(vals) % p

    return walk(formula)


def counting_rand(values):
    """A deterministic source of 'random' field elements, for exhaustive tests."""
    it = iter(values)
    return lambda: next(it)
