# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-network-pruning/. The authors are listed in prov/8KRCTK.jsonl.

"""Pruning by magnitude, by optimal brain damage and by optimal brain surgeon.

The loss near a trained minimum w* is the quadratic

    L(w) = L(w*) + (1/2) (w - w*)^T H (w - w*),

with H symmetric positive definite. On this loss the second order analysis of
LeCun, Denker and Solla (1990) and of Hassibi and Stork (1993) is exact. The
functions work with Fractions as well as floats, so tests can check identities
exactly.
"""

from fractions import Fraction
from typing import List, Sequence, Tuple

Matrix = List[List]


def quad_loss(h: Sequence[Sequence], w_star: Sequence, w: Sequence, base=0):
    """L(w) = base + (1/2) (w - w*)^T H (w - w*)."""
    d = [a - b for a, b in zip(w, w_star)]
    n = len(d)
    s = sum(d[i] * h[i][j] * d[j] for i in range(n) for j in range(n))
    return base + Fraction(1, 2) * s if not isinstance(s, float) else base + 0.5 * s


def inverse(a: Sequence[Sequence]) -> Matrix:
    """Gauss-Jordan inverse with partial pivoting; exact on Fractions."""
    n = len(a)
    m = [list(a[i]) + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [v / piv for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def magnitude_saliency(w: Sequence) -> List:
    """|w_q|: the rule of magnitude pruning."""
    return [abs(t) for t in w]


def obd_saliency(h: Sequence[Sequence], w: Sequence) -> List:
    """Optimal brain damage: s_q = h_qq w_q^2 / 2 (diagonal Hessian, no update)."""
    return [h[q][q] * w[q] * w[q] / 2 for q in range(len(w))]


def obs_saliency(hinv: Sequence[Sequence], w: Sequence) -> List:
    """Optimal brain surgeon: L_q = w_q^2 / (2 [H^-1]_qq)."""
    return [w[q] * w[q] / (2 * hinv[q][q]) for q in range(len(w))]


def obs_update(hinv: Sequence[Sequence], w: Sequence, q: int) -> List:
    """delta w = -(w_q / [H^-1]_qq) H^-1 e_q; the new w_q is exactly 0."""
    c = w[q] / hinv[q][q]
    return [-c * hinv[i][q] for i in range(len(w))]


def remove_from_inverse(hinv: Sequence[Sequence], q: int) -> Matrix:
    """The inverse of H with row and column q deleted, from H^-1.

    (H_RR)^-1 = (H^-1)_RR - (H^-1)_Rq (H^-1)_qR / (H^-1)_qq, with R the other
    indices. The result keeps size n, with row and column q set to 0, so that
    indices stay the same.
    """
    n = len(hinv)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        if i == q:
            continue
        for j in range(n):
            if j == q:
                continue
            out[i][j] = hinv[i][j] - hinv[i][q] * hinv[q][j] / hinv[q][q]
    return out


def obs_prune(h: Sequence[Sequence], w: Sequence, k: int) -> Tuple[List, List[int], List]:
    """Prune k weights one at a time with optimal brain surgeon.

    At each step, take the remaining weight with the smallest saliency
    w_q^2 / (2 [H^-1]_qq) on the remaining weights, apply the update, and
    restrict the inverse Hessian to the weights that are left. Returns the
    new weights, the pruned indices in order, and the predicted loss increase
    of each step.
    """
    w = list(w)
    hinv = inverse(h)
    alive = list(range(len(w)))
    pruned, gains = [], []
    for _ in range(k):
        sal = {i: w[i] * w[i] / (2 * hinv[i][i]) for i in alive}
        q = min(alive, key=lambda i: (sal[i], i))
        dw = obs_update(hinv, w, q)
        w = [a + b if i in alive else a for i, (a, b) in enumerate(zip(w, dw))]
        w[q] = 0 * w[q]
        gains.append(sal[q])
        pruned.append(q)
        alive.remove(q)
        hinv = remove_from_inverse(hinv, q)
    return w, pruned, gains


def constrained_minimizer(h: Sequence[Sequence], w_star: Sequence, zero: Sequence[int]) -> List:
    """argmin of the quadratic loss subject to w_S = 0, by solving H_RR d_R = H_RS w*_S.

    With d = w - w*, the optimality condition on R is H_RR d_R + H_RS d_S = 0
    and d_S = -w*_S.
    """
    n = len(w_star)
    s = list(zero)
    r = [i for i in range(n) if i not in s]
    hrr = [[h[i][j] for j in r] for i in r]
    rhs = [sum(h[i][j] * w_star[j] for j in s) for i in r]
    dr = [sum(a * b for a, b in zip(row, rhs)) for row in inverse(hrr)]
    w = [0 * t for t in w_star]
    for idx, i in enumerate(r):
        w[i] = w_star[i] + dr[idx]
    return w


def magnitude_mask(w: Sequence, fraction) -> List[int]:
    """Global magnitude pruning: a 0/1 mask that removes the given fraction of weights."""
    n = len(w)
    k = int(fraction * n)
    order = sorted(range(n), key=lambda i: (abs(w[i]), i))
    mask = [1] * n
    for i in order[:k]:
        mask[i] = 0
    return mask
