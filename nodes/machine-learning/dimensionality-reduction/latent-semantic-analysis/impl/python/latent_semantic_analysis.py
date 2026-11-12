# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latent-semantic-analysis/. The authors are listed in prov/A919QT.jsonl.

"""Latent semantic analysis: a truncated SVD of a weighted term-document matrix.

A (terms x documents) is weighted, A ~ U_k S_k V_k^T is its rank-k truncated
SVD, document j is represented by row j of V_k S_k (or V_k), and a query
vector q is folded in as q_hat = S_k^(-1) U_k^T q, which lives in the same
space as the rows of V_k. Documents are ranked by cosine similarity there.
"""

import math

Vector = list[float]
Matrix = list[list[float]]


def jacobi_eigh(a: Matrix, tol: float = 1e-14, max_sweeps: int = 100) -> tuple[Vector, Matrix]:
    """Eigenvalues (descending) and eigenvectors (as columns) of a symmetric matrix."""
    d = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(d) for j in range(d) if i != j)
        scale = sum(m[i][i] ** 2 for i in range(d)) + off
        if off <= tol * tol * max(scale, 1e-300):
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    m[k][p], m[k][q] = c * m[k][p] - s * m[k][q], s * m[k][p] + c * m[k][q]
                for k in range(d):
                    m[p][k], m[q][k] = c * m[p][k] - s * m[q][k], s * m[p][k] + c * m[q][k]
                for k in range(d):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    order = sorted(range(d), key=lambda i: -m[i][i])
    return [m[i][i] for i in order], [[v[r][i] for i in order] for r in range(d)]


def term_document_matrix(docs: list[list[str]], vocabulary: list[str]) -> Matrix:
    """Counts: entry (i, j) is the number of times term i occurs in document j."""
    index = {t: i for i, t in enumerate(vocabulary)}
    a = [[0.0] * len(docs) for _ in vocabulary]
    for j, doc in enumerate(docs):
        for tok in doc:
            if tok in index:
                a[index[tok]][j] += 1.0
    return a


def tfidf(a: Matrix) -> Matrix:
    """Weight counts by tf * log(n / df). Terms that occur in every document get weight 0."""
    n = len(a[0])
    out = []
    for row in a:
        df = sum(1 for x in row if x > 0)
        idf = math.log(n / df) if df else 0.0
        out.append([x * idf for x in row])
    return out


def truncated_svd(a: Matrix, k: int) -> tuple[Vector, Matrix, Matrix]:
    """Return (sigma_1..sigma_k, U_k as rows of length k per term, V_k as rows of length k per document).

    Uses the eigendecomposition of A^T A (documents x documents). Only singular
    values above a small threshold are kept, so fewer than k may be returned.
    """
    m, n = len(a), len(a[0])
    ata = [[sum(a[i][p] * a[i][q] for i in range(m)) for q in range(n)] for p in range(n)]
    lam, e = jacobi_eigh(ata)
    top = max(lam[0], 0.0)
    sig, vcols = [], []
    for t in range(min(k, n)):
        if lam[t] <= 1e-12 * max(top, 1e-300):
            break
        sig.append(math.sqrt(lam[t]))
        vcols.append([e[p][t] for p in range(n)])
    ucols = [[sum(a[i][p] * vc[p] for p in range(n)) / s for i in range(m)] for s, vc in zip(sig, vcols)]
    u_rows = [[uc[i] for uc in ucols] for i in range(m)]
    v_rows = [[vc[p] for vc in vcols] for p in range(n)]
    return sig, u_rows, v_rows


def fold_in(q: Vector, sig: Vector, u: Matrix) -> Vector:
    """q_hat = S_k^(-1) U_k^T q, the coordinates of a new document or query."""
    k = len(sig)
    return [sum(u[i][t] * q[i] for i in range(len(q))) / sig[t] for t in range(k)]


def cosine(x: Vector, y: Vector) -> float:
    nx = math.sqrt(sum(a * a for a in x))
    ny = math.sqrt(sum(b * b for b in y))
    if nx == 0 or ny == 0:
        return 0.0
    return sum(a * b for a, b in zip(x, y)) / (nx * ny)


def lsa_search(docs: list[list[str]], vocabulary: list[str], k: int, query: list[str],
               weighting: str = "count", scale_by_sigma: bool = True) -> list[tuple[int, float]]:
    """Rank documents by cosine with the folded-in query in the k-dimensional space.

    With scale_by_sigma the comparison uses rows of V_k S_k and q_hat S_k.
    """
    a = term_document_matrix(docs, vocabulary)  # @line L1
    q = [row[0] for row in term_document_matrix([query], vocabulary)]
    if weighting == "tfidf":
        n = len(docs)
        idf = [math.log(n / sum(1 for x in row if x > 0)) if any(row) else 0.0 for row in a]
        a = [[x * w for x in row] for row, w in zip(a, idf)]
        q = [x * w for x, w in zip(q, idf)]
    sig, u, v = truncated_svd(a, k)  # @line L2
    q_hat = fold_in(q, sig, u)  # @line L3
    w = sig if scale_by_sigma else [1.0] * len(sig)
    qs = [x * s for x, s in zip(q_hat, w)]  # @line L4
    scores = [(j, cosine([x * s for x, s in zip(v[j], w)], qs)) for j in range(len(v))]  # @line L5
    scores.sort(key=lambda p: -p[1])
    return scores  # @line L6


def reconstruct(sig: Vector, u: Matrix, v: Matrix) -> Matrix:
    """A_k = U_k S_k V_k^T."""
    return [[sum(u[i][t] * sig[t] * v[j][t] for t in range(len(sig))) for j in range(len(v))] for i in range(len(u))]
