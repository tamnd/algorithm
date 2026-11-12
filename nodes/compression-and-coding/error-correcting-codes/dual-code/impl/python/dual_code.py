# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-code/. The authors are listed in prov/WBZ251.jsonl.

"""The dual of a linear code over GF(q), q prime, and tests for self-orthogonal and self-dual codes.

C^⊥ = { v : v . c = 0 for every c in C }, with the standard inner product
v . c = sum v_i c_i in GF(q). A generator matrix of C^⊥ is a parity-check
matrix of C, found here from the reduced row echelon form of G.
"""

Matrix = list[list[int]]


def rref(rows: Matrix, q: int) -> tuple[Matrix, list[int]]:
    m = [list(r) for r in rows]
    pivots: list[int] = []
    rank = 0
    for col in range(len(m[0]) if m else 0):
        piv = next((i for i in range(rank, len(m)) if m[i][col] % q), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        inv = pow(m[rank][col], q - 2, q)
        m[rank] = [x * inv % q for x in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][col]:
                f = m[i][col]
                m[i] = [(x - f * y) % q for x, y in zip(m[i], m[rank])]
        pivots.append(col)
        rank += 1
    return m[:rank], pivots


def dual_generator(g: Matrix, q: int = 2) -> Matrix:
    """Rows: a basis of C^⊥, one for each non-pivot column of RREF(G). Cost: O(k^2 n) field operations."""
    n = len(g[0])
    red, pivots = rref(g, q)
    out = []
    for f in (j for j in range(n) if j not in pivots):
        v = [0] * n
        v[f] = 1
        for i, col in enumerate(pivots):
            v[col] = (-red[i][f]) % q
        out.append(v)
    return out


def inner(u: list[int], v: list[int], q: int) -> int:
    return sum(a * b for a, b in zip(u, v)) % q


def is_self_orthogonal(g: Matrix, q: int = 2) -> bool:
    """C is contained in C^⊥ if and only if G G^T = 0."""
    return all(inner(u, v, q) == 0 for u in g for v in g)


def is_self_dual(g: Matrix, q: int = 2) -> bool:
    """C = C^⊥ if and only if C is self-orthogonal and 2k = n (G of full rank)."""
    return is_self_orthogonal(g, q) and 2 * len(rref(g, q)[1]) == len(g[0])
