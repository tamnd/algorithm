# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/griesmer-bound/. The authors are listed in prov/9D53Y5.jsonl.

"""The Griesmer bound for linear codes, the residual code of its proof, and a search
for the shortest binary linear codes of small dimension.

Words over GF(p), p prime, are tuples of ints in range(p).
"""

from itertools import combinations_with_replacement, product


def griesmer_length(k: int, d: int, q: int = 2) -> int:
    """g_q(k, d) = sum_{i=0}^{k-1} ceil(d / q^i): every linear [n, k, d]_q code has n >= this."""
    return sum(-(-d // q ** i) for i in range(k))


def span(gen: list[tuple[int, ...]], p: int) -> list[tuple[int, ...]]:
    """All p^k words m G of the code with generator rows gen over GF(p)."""
    n = len(gen[0])
    words = []
    for m in product(range(p), repeat=len(gen)):
        words.append(tuple(sum(a * row[j] for a, row in zip(m, gen)) % p for j in range(n)))
    return words


def weight(w: tuple[int, ...]) -> int:
    return sum(1 for a in w if a)


def min_distance(words: list[tuple[int, ...]]) -> int:
    return min(weight(w) for w in words if any(w))


def rank(rows: list[tuple[int, ...]], p: int) -> int:
    """Rank over GF(p) by Gaussian elimination."""
    m = [list(r) for r in rows]
    r = 0
    ncols = len(m[0]) if m else 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(m)) if m[i][c] % p), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], p - 2, p)
        m[r] = [(x * inv) % p for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] % p:
                f = m[i][c]
                m[i] = [(x - f * y) % p for x, y in zip(m[i], m[r])]
        r += 1
    return r


def residual_code(words: list[tuple[int, ...]], c: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The residual code: every word restricted to the positions where c is zero (as a set)."""
    keep = [j for j, a in enumerate(c) if a == 0]
    return sorted({tuple(w[j] for j in keep) for w in words})


def binary_min_length(k: int, d: int, n_max: int) -> int | None:
    """Least n for which a binary linear [n, k, >= d] code exists, or None if n > n_max.

    A binary [n, k] code with no zero column is a multiset of n nonzero columns in GF(2)^k,
    and the weight of the message m is the number of columns c with m . c = 1. The search
    tries every multiset, from the Griesmer length up.
    """
    points = list(range(1, 2 ** k))
    msgs = list(range(1, 2 ** k))
    # ind[p][i] = 1 when message msgs[i] has odd inner product with column p
    ind = {p: [bin(m & p).count("1") & 1 for m in msgs] for p in points}
    for n in range(griesmer_length(k, d), n_max + 1):
        for cols in combinations_with_replacement(points, n):
            w = [0] * len(msgs)
            for p in cols:
                for i, b in enumerate(ind[p]):
                    w[i] += b
            if min(w) >= d:
                return n
    return None


def simplex_generator(k: int, q: int) -> list[tuple[int, ...]]:
    """Generator rows of the q-ary simplex code: one column per point of PG(k - 1, q)."""
    cols = []
    for v in product(range(q), repeat=k):
        if any(v):
            first = next(a for a in v if a)
            if first == 1:  # one representative per projective point
                cols.append(v)
    return [tuple(col[i] for col in cols) for i in range(k)]


def paley_code(p: int) -> list[tuple[int, ...]]:
    """A nonlinear binary (p, p + 1, (p + 1)/2) code from the Paley Hadamard matrix,
    for a prime p = 3 mod 4: the zero word and the p cyclic shifts of the word whose
    1s sit at 0 and at the quadratic nonresidues."""
    squares = {(x * x) % p for x in range(1, p)}
    base = [1 if (j == 0 or j not in squares) else 0 for j in range(p)]
    words = [tuple([0] * p)]
    for s in range(p):
        words.append(tuple(base[(j - s) % p] for j in range(p)))
    return words


def cyclic_generator(g: list[int], n: int) -> list[tuple[int, ...]]:
    """Generator rows x^i g(x), i < n - deg g, of a cyclic code; g is low degree first."""
    k = n - (len(g) - 1)
    return [tuple([0] * i + g + [0] * (n - len(g) - i)) for i in range(k)]
