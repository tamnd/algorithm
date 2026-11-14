# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymptotic-waveform-evaluation/. The authors are listed in prov/5A3DBS.jsonl.

import cmath
from fractions import Fraction
from typing import NamedTuple, Sequence


class AweModel(NamedTuple):
    moments: list      # m_0 .. m_{2q-1}, exact
    numerator: list    # a_0 .. a_{q-1} of P(s), exact
    denominator: list  # b_0 = 1, b_1 .. b_q of Q(s), exact
    poles: list        # roots of Q, complex floats
    residues: list     # P(p) / Q'(p) for each pole, complex floats


def lu_factor(A: Sequence[Sequence]) -> tuple:
    """LU factorization with row pivoting on the first non-zero entry (exact for Fractions)."""
    n = len(A)
    M = [[Fraction(x) for x in row] for row in A]
    perm = list(range(n))
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            raise ValueError("singular matrix")
        M[c], M[p] = M[p], M[c]
        perm[c], perm[p] = perm[p], perm[c]
        for r in range(c + 1, n):
            if M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r][c] = f
                for k in range(c + 1, n):
                    M[r][k] -= f * M[c][k]
    return M, perm


def lu_solve(factor: tuple, rhs: Sequence) -> list:
    M, perm = factor
    n = len(M)
    y = [Fraction(rhs[perm[i]]) for i in range(n)]
    for i in range(n):
        for k in range(i):
            y[i] -= M[i][k] * y[k]
    for i in range(n - 1, -1, -1):
        for k in range(i + 1, n):
            y[i] -= M[i][k] * y[k]
        y[i] /= M[i][i]
    return y


def polyval(c: Sequence, s):
    """c[k] is the coefficient of s^k."""
    v = 0
    for x in reversed(c):
        v = v * s + x
    return v


def durand_kerner(c: Sequence, iterations: int = 2000) -> list:
    """All complex roots of the polynomial with coefficients c (c[k] of s^k)."""
    c = [complex(x) for x in c]
    while c and c[-1] == 0:
        c.pop()
    deg = len(c) - 1
    if deg < 1:
        return []
    monic = [x / c[-1] for x in c]
    radius = 1.0 + max(abs(x) for x in monic[:-1])  # Cauchy bound on the roots
    z = [radius * (0.4 + 0.9j) ** k for k in range(deg)]
    for _ in range(iterations):
        change = 0.0
        for i in range(deg):
            den = 1.0
            for j in range(deg):
                if j != i:
                    den *= z[i] - z[j]
            step = polyval(monic, z[i]) / den
            z[i] -= step
            change = max(change, abs(step))
        if change <= 1e-15 * radius:
            break
    return z


def moments(G, C, b, l, count: int) -> list:
    """m_k = l^T (-G^{-1} C)^k G^{-1} b for k = 0 .. count-1, exactly."""
    n = len(G)
    factor = lu_factor(G)
    x = lu_solve(factor, b)  # @line L1
    out = [sum(Fraction(l[i]) * x[i] for i in range(n))]  # @line L3
    for _ in range(count - 1):
        cx = [-sum(Fraction(C[i][j]) * x[j] for j in range(n)) for i in range(n)]
        x = lu_solve(factor, cx)  # @line L2
        out.append(sum(Fraction(l[i]) * x[i] for i in range(n)))  # @line L3
    return out


def asymptotic_waveform_evaluation(G, C, b, l, q: int) -> AweModel:
    """The q-pole AWE model of H(s) = l^T (G + sC)^{-1} b.

    G, C are n x n matrices and b, l vectors of ints or Fractions. The model
    P(s)/Q(s) with deg P <= q-1 and deg Q <= q matches the moments m_0 ..
    m_{2q-1}. Raises ValueError if the Hankel matrix of the moments is singular.
    """
    if q < 1:
        raise ValueError("q must be at least 1")
    m = moments(G, C, b, l, 2 * q)
    hankel = [[m[k - j] for j in range(1, q + 1)] for k in range(q, 2 * q)]
    rhs = [-m[k] for k in range(q, 2 * q)]
    den = [Fraction(1)] + lu_solve(lu_factor(hankel), rhs)  # @line L4
    num = [sum(den[j] * m[k - j] for j in range(k + 1)) for k in range(q)]  # @line L5
    poles = durand_kerner(den)  # @line L6
    dden = [k * den[k] for k in range(1, len(den))]
    residues = [polyval(num, p) / polyval(dden, p) for p in poles]  # @line L7
    return AweModel(m, num, den, poles, residues)  # @line L8


def is_stable(den: Sequence) -> bool:
    """Exact Routh test: True if and only if every root of Q lies in the open left half-plane."""
    c = [Fraction(x) for x in den]
    while c and c[-1] == 0:
        c.pop()
    if len(c) <= 1:
        return True
    hi = c[::-1]  # coefficients from the highest power down
    rows = [hi[0::2], hi[1::2]]
    while len(rows[-1]) > 0 and any(x != 0 for x in rows[-1]):
        a, b = rows[-2], rows[-1]
        if b[0] == 0:
            return False  # a zero pivot: some root is on or right of the imaginary axis
        nxt = []
        for j in range(len(a) - 1):
            right = b[j + 1] if j + 1 < len(b) else 0
            nxt.append((b[0] * a[j + 1] - a[0] * right) / b[0])
        rows.append(nxt)
    rows = [r for r in rows if r]
    if len(rows) != len(c):
        return False  # a row of zeros: roots symmetric about the origin
    first = [r[0] for r in rows]
    return all(x != 0 for x in first) and all((x > 0) == (first[0] > 0) for x in first)


def step_response(model: AweModel, t: float) -> float:
    """y(t) = m_0 + sum_i (k_i / p_i) exp(p_i t), the response to a unit step at t = 0."""
    y = complex(model.moments[0])
    for p, k in zip(model.poles, model.residues):
        y += k / p * cmath.exp(p * t)
    return y.real
