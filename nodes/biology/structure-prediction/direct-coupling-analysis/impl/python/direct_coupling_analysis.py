# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-coupling-analysis/. The authors are listed in prov/4X9C5V.jsonl.

"""Mean-field direct coupling analysis (Morcos et al. 2011).

An alignment is a list of equal-length tuples of states 0 .. q-1 (in real use
q = 21: twenty amino acids and the gap). State q-1 is the reference state of
the gauge: the couplings e_ij(a, q-1) and e_ij(q-1, b) are 0.

Pair frequencies f2 are stored as a dict that maps (i, j), i < j, to a q x q
list of lists, and couplings e in the same way.
"""

import math
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Alignment = Sequence[Sequence[int]]
Matrix = List[List[float]]
PairTable = Dict[Tuple[int, int], Matrix]


def sequence_weights(msa: Alignment, theta: float = 0.8) -> List[float]:
    """w_m = 1 / (number of sequences with identity >= theta to sequence m, itself included)."""
    n = len(msa[0])
    t = Fraction(theta).limit_denominator(10 ** 6)  # exact threshold test, no rounding at the boundary
    out = []
    for x in msa:
        close = 0
        for y in msa:
            same = sum(1 for a, b in zip(x, y) if a == b)
            if same * t.denominator >= t.numerator * n:
                close += 1
        out.append(1.0 / close)
    return out


def frequencies(msa: Alignment, q: int, weights: Sequence[float], lam: float) -> Tuple[Matrix, PairTable]:
    """Reweighted one- and two-column frequencies with pseudocount lam."""
    n = len(msa[0])
    m_eff = sum(weights)
    z = lam + m_eff
    f1 = [[lam / q] * q for _ in range(n)]
    f2 = {(i, j): [[lam / (q * q)] * q for _ in range(q)] for i in range(n) for j in range(i + 1, n)}
    for x, w in zip(msa, weights):
        for i in range(n):
            f1[i][x[i]] += w
            for j in range(i + 1, n):
                f2[(i, j)][x[i]][x[j]] += w
    f1 = [[v / z for v in row] for row in f1]
    f2 = {k: [[v / z for v in row] for row in t] for k, t in f2.items()}
    return f1, f2


def invert(a: Matrix) -> Matrix:
    """Gauss-Jordan elimination with partial pivoting."""
    n = len(a)
    m = [list(row) + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-300:
            raise ValueError("singular correlation matrix; use a pseudocount lam > 0")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [v / piv for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [row[n:] for row in m]


def correlation_matrix(f1: Matrix, f2: PairTable, q: int) -> Matrix:
    """C[(i,a),(j,b)] = f_ij(a,b) - f_i(a) f_j(b) over the q-1 non-reference states."""
    n = len(f1)
    k = q - 1
    c = [[0.0] * (n * k) for _ in range(n * k)]
    for i in range(n):
        for j in range(n):
            for a in range(k):
                for b in range(k):
                    if i == j:
                        fij = f1[i][a] if a == b else 0.0
                    elif i < j:
                        fij = f2[(i, j)][a][b]
                    else:
                        fij = f2[(j, i)][b][a]
                    c[i * k + a][j * k + b] = fij - f1[i][a] * f1[j][b]
    return c


def mean_field_couplings(f1: Matrix, f2: PairTable, q: int) -> PairTable:
    """e = -C^{-1}, padded with zeros for the reference state."""
    n = len(f1)
    k = q - 1
    c_inv = invert(correlation_matrix(f1, f2, q))
    e = {}
    for i in range(n):
        for j in range(i + 1, n):
            e[(i, j)] = [[-c_inv[i * k + a][j * k + b] if a < k and b < k else 0.0 for b in range(q)]
                         for a in range(q)]
    return e


def zero_sum_gauge(m: Matrix) -> Matrix:
    """Subtract row and column means and add back the total mean."""
    q = len(m)
    row = [sum(r) / q for r in m]
    col = [sum(m[a][b] for a in range(q)) / q for b in range(q)]
    tot = sum(row) / q
    return [[m[a][b] - row[a] - col[b] + tot for b in range(q)] for a in range(q)]


def frobenius_scores(e: PairTable) -> Dict[Tuple[int, int], float]:
    return {k: math.sqrt(sum(v * v for r in zero_sum_gauge(m) for v in r)) for k, m in e.items()}


def apc(scores: Dict[Tuple[int, int], float], n: int) -> Dict[Tuple[int, int], float]:
    """Average product correction: S_ij = F_ij - F_i. F_.j / F_.."""
    def f(i: int, j: int) -> float:
        return scores[(i, j) if i < j else (j, i)]

    mean_i = [sum(f(i, j) for j in range(n) if j != i) / (n - 1) for i in range(n)]
    mean = sum(scores.values()) / len(scores)
    if mean == 0.0:
        return dict(scores)  # all scores are 0; nothing to correct
    return {(i, j): s - mean_i[i] * mean_i[j] / mean for (i, j), s in scores.items()}


def mfdca(msa: Alignment, q: int, theta: float = 0.8, lam: float = -1.0
          ) -> Tuple[List[Tuple[int, int]], Dict[Tuple[int, int], float], PairTable]:
    """Mean-field DCA. lam < 0 means lam = M_eff, the choice of Morcos et al.

    Returns the pairs ranked by APC-corrected Frobenius score, the scores, and the couplings.
    """
    n = len(msa[0])
    w = sequence_weights(msa, theta)  # @line L1
    if lam < 0:
        lam = sum(w)
    f1, f2 = frequencies(msa, q, w, lam)  # @line L2 @line L3
    c = correlation_matrix(f1, f2, q)  # @line L4
    c_inv = invert(c)  # @line L5
    k = q - 1
    e = {(i, j): [[-c_inv[i * k + a][j * k + b] if a < k and b < k else 0.0 for b in range(q)]
                  for a in range(q)] for i in range(n) for j in range(i + 1, n)}
    fro = frobenius_scores(e)  # @line L6
    s = apc(fro, n)  # @line L7
    ranked = sorted(s, key=lambda p: (-s[p], p))  # @line L8
    return ranked, s, e


def direct_information(e_ij: Matrix, fi: Sequence[float], fj: Sequence[float],
                       iters: int = 1000, tol: float = 1e-13) -> Tuple[float, Matrix]:
    """Direct information of Weigt et al. (2009) and Morcos et al. (2011).

    P_dir(a, b) = exp(e_ij(a, b) + h_i(a) + h_j(b)) / Z with the fields fitted so
    that the marginals of P_dir are fi and fj (Sinkhorn scaling of exp(e_ij)).
    Returns DI = sum P_dir log(P_dir / (fi fj)) and P_dir.
    """
    q = len(fi)
    k = [[math.exp(v) for v in row] for row in e_ij]
    u = [1.0] * q
    v = [1.0] * q
    for _ in range(iters):
        u = [fi[a] / sum(k[a][b] * v[b] for b in range(q)) for a in range(q)]
        v = [fj[b] / sum(k[a][b] * u[a] for a in range(q)) for b in range(q)]
        row = [sum(u[a] * k[a][b] * v[b] for b in range(q)) for a in range(q)]
        if max(abs(row[a] - fi[a]) for a in range(q)) < tol:
            break
    p = [[u[a] * k[a][b] * v[b] for b in range(q)] for a in range(q)]
    di = sum(p[a][b] * math.log(p[a][b] / (fi[a] * fj[b])) for a in range(q) for b in range(q) if p[a][b] > 0)
    return di, p


def mutual_information(f1: Matrix, f2: PairTable, i: int, j: int) -> float:
    """MI of columns i < j from the frequency tables."""
    q = len(f1[i])
    t = f2[(i, j)]
    return sum(t[a][b] * math.log(t[a][b] / (f1[i][a] * f1[j][b]))
               for a in range(q) for b in range(q) if t[a][b] > 0)
