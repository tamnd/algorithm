# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retrofitting-word-vectors/. The authors are listed in prov/TKNXEG.jsonl.

"""Retrofitting of word vectors to a semantic lexicon (Faruqui et al. 2015).

The input is a mapping from each word to its original vector q_hat and a
lexicon that maps a word to its neighbours. Only neighbours that have a
vector count. A word with no such neighbour keeps its vector.

The update for a word i with neighbours N(i) is

    q_i <- (sum_j beta_ij q_j + alpha_i q_hat_i) / (sum_j beta_ij + alpha_i)

with alpha_i = 1 and beta_ij = 1 / |N(i)| by default, as in the paper and in
its released code. The default order is Gauss-Seidel (each new vector is used
at once, as the released code does); jacobi=True uses only the vectors of the
previous sweep.

The fixed point of the update is the solution of the linear system
(alpha_i + sum_j beta_ij) q_i - sum_j beta_ij q_j = alpha_i q_hat_i. The
function solve_direct solves it by Gaussian elimination, as a reference.
"""

from typing import Callable, Mapping, Sequence

Vector = list[float]
Weight = Callable[[str, str, int], float]


def _neighbours(vectors: Mapping[str, Sequence[float]],
                lexicon: Mapping[str, Sequence[str]]) -> dict[str, list[str]]:
    """Neighbours of each word in the vocabulary, restricted to the vocabulary."""
    out: dict[str, list[str]] = {}
    for w in sorted(vectors):
        nb = sorted({u for u in lexicon.get(w, ()) if u in vectors and u != w})
        if nb:
            out[w] = nb
    return out


def default_beta(i: str, j: str, degree: int) -> float:
    """beta_ij = 1 / |N(i)|, the weight of Faruqui et al."""
    return 1.0 / degree


def default_alpha(i: str) -> float:
    return 1.0


def update(i: str, q: Mapping[str, Sequence[float]], q_hat: Mapping[str, Sequence[float]],
           nb: Sequence[str], alpha: Callable[[str], float] = default_alpha,
           beta: Weight = default_beta) -> Vector:
    """One update of the word i: a weighted mean of its neighbours and its original vector."""
    a = alpha(i)
    num = [a * x for x in q_hat[i]]
    den = a
    for j in nb:
        b = beta(i, j, len(nb))
        den += b
        for t, x in enumerate(q[j]):
            num[t] += b * x
    return [x / den for x in num]  # @line L4


def retrofit(vectors: Mapping[str, Sequence[float]], lexicon: Mapping[str, Sequence[str]],
             iterations: int = 10, alpha: Callable[[str], float] = default_alpha,
             beta: Weight = default_beta, jacobi: bool = False) -> dict[str, Vector]:
    """Return the retrofitted vectors after the given number of sweeps."""
    q_hat = {w: list(map(float, v)) for w, v in vectors.items()}
    q = {w: list(v) for w, v in q_hat.items()}  # @line L1
    nbs = _neighbours(vectors, lexicon)
    for _ in range(iterations):  # @line L2
        src = {w: list(v) for w, v in q.items()} if jacobi else q
        new = {}
        for i, nb in nbs.items():  # @line L3
            new[i] = update(i, src, q_hat, nb, alpha, beta)
            if not jacobi:
                q[i] = new[i]
        if jacobi:
            q.update(new)
    return q  # @line L5


def solve_linear(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Solve A X = B by Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [list(map(float, a[r])) + list(map(float, b[r])) for r in range(n)]
    width = len(m[0])
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-300:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c] / m[c][c]
                for k in range(c, width):
                    m[r][k] -= f * m[c][k]
    return [[m[r][k] / m[r][r] for k in range(n, width)] for r in range(n)]


def solve_direct(vectors: Mapping[str, Sequence[float]], lexicon: Mapping[str, Sequence[str]],
                 alpha: Callable[[str], float] = default_alpha,
                 beta: Weight = default_beta) -> dict[str, Vector]:
    """The fixed point of the update, found by one linear solve (the reference)."""
    nbs = _neighbours(vectors, lexicon)
    words = sorted(nbs)
    idx = {w: r for r, w in enumerate(words)}
    n = len(words)
    out = {w: list(map(float, v)) for w, v in vectors.items()}
    if n == 0:
        return out
    a = [[0.0] * n for _ in range(n)]
    rhs = []
    for i in words:
        r = idx[i]
        ai = alpha(i)
        a[r][r] += ai
        row = [ai * x for x in vectors[i]]
        for j in nbs[i]:
            b = beta(i, j, len(nbs[i]))
            a[r][r] += b
            if j in idx:
                a[r][idx[j]] -= b
            else:  # a neighbour with no neighbours of its own keeps q_hat_j
                row = [x + b * y for x, y in zip(row, vectors[j])]
        rhs.append(row)
    sol = solve_linear(a, rhs)
    for i in words:
        out[i] = sol[idx[i]]
    return out


def objective(q: Mapping[str, Sequence[float]], q_hat: Mapping[str, Sequence[float]],
              lexicon: Mapping[str, Sequence[str]], alpha: Callable[[str], float] = default_alpha,
              weight: Callable[[str, str], float] = lambda i, j: 1.0) -> float:
    """Psi(Q) = sum_i alpha_i |q_i - q_hat_i|^2 + sum over unordered edges w_ij |q_i - q_j|^2.

    Each edge {i, j} of the lexicon is counted once, with a symmetric weight.
    For this objective the update with beta_ij = w_ij is the exact minimizer in q_i.
    """
    nbs = _neighbours(q_hat, lexicon)
    edges = {tuple(sorted((i, j))) for i, nb in nbs.items() for j in nb}
    total = 0.0
    for i in q_hat:
        total += alpha(i) * sum((x - y) ** 2 for x, y in zip(q[i], q_hat[i]))
    for i, j in sorted(edges):
        total += weight(i, j) * sum((x - y) ** 2 for x, y in zip(q[i], q[j]))
    return total
