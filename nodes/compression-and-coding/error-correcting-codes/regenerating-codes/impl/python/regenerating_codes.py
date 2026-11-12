# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regenerating-codes/. The authors are listed in prov/SKYSW3.jsonl.
"""Regenerating codes: the storage and repair bandwidth tradeoff of Dimakis et al., and the
product-matrix MBR code of Rashmi, Shah and Kumar over a prime field GF(p).

Parameters: a file of B symbols on n nodes, alpha symbols per node; any k nodes rebuild the
file; a failed node is rebuilt from d helpers that send beta symbols each.
"""

from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

Num = Fraction


# ---------- the tradeoff ----------

def cut_set(alpha: Num, beta: Num, k: int, d: int) -> Num:
    """The largest file size the information flow graph allows: sum_(i<k) min(alpha, (d-i) beta)."""
    return sum((min(alpha, (d - i) * beta) for i in range(k)), Fraction(0))


def msr_point(b: Num, k: int, d: int) -> Tuple[Num, Num]:
    """(alpha, beta) at minimum storage: alpha = B/k, beta = B/(k(d-k+1))."""
    return Fraction(b) / k, Fraction(b) / (k * (d - k + 1))


def mbr_point(b: Num, k: int, d: int) -> Tuple[Num, Num]:
    """(alpha, beta) at minimum bandwidth: beta = 2B/(k(2d-k+1)), alpha = d beta."""
    beta = Fraction(2 * b, k * (2 * d - k + 1))
    return d * beta, beta


def min_alpha(b: Num, beta: Num, k: int, d: int) -> Optional[Num]:
    """The least alpha with cut_set(alpha, beta) >= B, or None if no alpha is enough."""
    if cut_set(Fraction(10 ** 9), beta, k, d) < b:
        return None
    # cut_set is piecewise linear and increasing in alpha; search between breakpoints
    points = sorted({Fraction(0)} | {(d - i) * beta for i in range(k)})
    for lo, hi in zip(points, points[1:]):
        if cut_set(hi, beta, k, d) >= b:
            f_lo, f_hi = cut_set(lo, beta, k, d), cut_set(hi, beta, k, d)
            return lo + (hi - lo) * (Fraction(b) - f_lo) / (f_hi - f_lo)
    return None


# ---------- linear algebra over GF(p) ----------

def mat_mul(a: List[List[int]], b: List[List[int]], p: int) -> List[List[int]]:
    return [[sum(x * y for x, y in zip(row, col)) % p for col in zip(*b)] for row in a]


def mat_inv(a: List[List[int]], p: int) -> List[List[int]]:
    n = len(a)
    m = [list(row) + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        r = next(i for i in range(c, n) if m[i][c] % p)
        m[c], m[r] = m[r], m[c]
        f = pow(m[c][c], p - 2, p)
        m[c] = [v * f % p for v in m[c]]
        for i in range(n):
            if i != c and m[i][c]:
                g = m[i][c]
                m[i] = [(v - g * w) % p for v, w in zip(m[i], m[c])]
    return [row[n:] for row in m]


def transpose(a: List[List[int]]) -> List[List[int]]:
    return [list(c) for c in zip(*a)]


# ---------- product-matrix MBR code ----------

class ProductMatrixMBR:
    """beta = 1, alpha = d, B = k(2d-k+1)/2. Node i stores psi_i^T M, M symmetric d x d."""

    def __init__(self, n: int, k: int, d: int, p: int):
        assert k <= d <= n - 1 and n < p
        self.n, self.k, self.d, self.p = n, k, d, p
        self.size = k * (2 * d - k + 1) // 2
        # Vandermonde rows (1, x, x^2, ..., x^(d-1)) at x = 1..n: any d rows are independent,
        # and any k rows of the first k columns are independent
        self.psi = [[pow(x, j, p) for j in range(d)] for x in range(1, n + 1)]

    def message_matrix(self, data: Sequence[int]) -> List[List[int]]:
        """M = [[S, T], [T^T, 0]] with S symmetric k x k and T of size k x (d-k)."""
        k, d = self.k, self.d
        assert len(data) == self.size
        m = [[0] * d for _ in range(d)]
        it = iter(data)
        for i in range(k):
            for j in range(i, k):
                m[i][j] = m[j][i] = next(it) % self.p
        for i in range(k):
            for j in range(k, d):
                m[i][j] = m[j][i] = next(it) % self.p
        return m

    def encode(self, data: Sequence[int]) -> List[List[int]]:
        return mat_mul(self.psi, self.message_matrix(data), self.p)

    def helper_symbol(self, stored: Sequence[int], failed: int) -> int:
        """Helper j sends one symbol: psi_j^T M psi_f."""
        return sum(s * v for s, v in zip(stored, self.psi[failed])) % self.p

    def repair(self, failed: int, helpers: Sequence[int], symbols: Sequence[int]) -> List[int]:
        """From d symbols psi_j^T M psi_f, solve for M psi_f; by symmetry it is the lost row."""
        rep = [self.psi[j] for j in helpers]
        col = mat_mul(mat_inv(rep, self.p), [[s] for s in symbols], self.p)
        return [c[0] for c in col]

    def reconstruct(self, nodes: Sequence[int], stored: Sequence[Sequence[int]]) -> List[int]:
        """From any k nodes: Psi_DC M = [Phi S + Delta T^T, Phi T]."""
        k, d, p = self.k, self.d, self.p
        phi = [[self.psi[i][j] for j in range(k)] for i in nodes]
        delta = [[self.psi[i][j] for j in range(k, d)] for i in nodes]
        phi_inv = mat_inv(phi, p)
        right = [[row[j] for j in range(k, d)] for row in stored]
        t = mat_mul(phi_inv, right, p)                      # k x (d-k)
        left = [[row[j] for j in range(k)] for row in stored]
        dt = mat_mul(delta, transpose(t), p) if d > k else [[0] * k for _ in range(k)]
        s = mat_mul(phi_inv, [[(a - b) % p for a, b in zip(r1, r2)] for r1, r2 in zip(left, dt)], p)
        data = [s[i][j] for i in range(k) for j in range(i, k)]
        data += [t[i][j - k] for i in range(k) for j in range(k, d)]
        return data


# ---------- the Reed-Solomon baseline ----------

class ReedSolomonStorage:
    """An [n, k] MDS code over GF(p) on `stripes` independent stripes: alpha = stripes,
    B = k * stripes. Repair of one node reads alpha symbols from each of k nodes."""

    def __init__(self, n: int, k: int, stripes: int, p: int):
        self.n, self.k, self.stripes, self.p = n, k, stripes, p
        self.gen = [[pow(x, j, p) for j in range(k)] for x in range(1, n + 1)]

    def encode(self, data: Sequence[int]) -> List[List[int]]:
        k, p = self.k, self.p
        stripes = [data[s * k:(s + 1) * k] for s in range(self.stripes)]
        return [[sum(g * v for g, v in zip(row, st)) % p for st in stripes] for row in self.gen]

    def repair(self, failed: int, helpers: Sequence[int],
               stored: Dict[int, Sequence[int]]) -> Tuple[List[int], int]:
        """Returns (rebuilt contents, number of symbols downloaded)."""
        sub = [self.gen[j] for j in helpers]
        inv = mat_inv(sub, self.p)
        out, downloaded = [], 0
        for s in range(self.stripes):
            vals = [[stored[j][s]] for j in helpers]
            downloaded += len(helpers)
            msg = mat_mul(inv, vals, self.p)
            out.append(sum(g * v[0] for g, v in zip(self.gen[failed], msg)) % self.p)
        return out, downloaded
