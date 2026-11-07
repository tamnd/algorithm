# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winograd-fourier-transform/. The authors are listed in prov/XCA95E.jsonl.

"""Winograd Fourier transform algorithm (WFTA).

Each short DFT of length q in {2, 3, 4, 5, 7, 8} is written as C diag(mu) A,
where A (pre-additions) and C (post-additions) use only additions and
subtractions and mu is a vector of constants. For n = q_1 ... q_d with pairwise
coprime factors, the Good-Thomas index maps turn the DFT of length n into a
d-dimensional DFT, which is the Kronecker product of the short ones; nesting
gives (C_1 x ... x C_d) diag(mu_1 x ... x mu_d) (A_1 x ... x A_d), so all
multiplications happen in one pointwise product of size m_1 ... m_d.
X_k = sum_j x_j w**(j*k); over C, w = exp(-2*pi*i/n); the inverse divides by n.
"""

from __future__ import annotations

import cmath
import math
from typing import Callable, Sequence


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * math.pi * r / n)


class Field:
    """C (p is None, w = exp(-2 pi i/n)) or Z/pZ with a given root w of order n."""

    def __init__(self, n: int, w: int | None = None, p: int | None = None, sign: int = -1) -> None:
        self.n, self.p, self.w, self.sign = n, p, w, sign
        if p is not None:
            if pow(w, n, p) != 1 or any(pow(w, n // r, p) == 1 for r in range(2, n + 1) if n % r == 0 and _is_prime(r)):
                raise ValueError("w must have order exactly n modulo p")

    def root(self, e: int):
        """w**e."""
        if self.p is None:
            return _unit(self.sign * e, self.n)
        return pow(self.w, e % self.n, self.p)

    def div(self, a, b: int):
        if self.p is None:
            return a / b
        return a * pow(b, -1, self.p) % self.p

    def inv(self, a):
        if self.p is None:
            return 1 / a
        return pow(a, -1, self.p)

    def red(self, a):
        return a % self.p if self.p is not None else a


def _is_prime(r: int) -> bool:
    return r > 1 and all(r % q for q in range(2, int(r**0.5) + 1))


# ---------------------------------------------------------------- short modules
# pre(x) -> list of length m, post(m) -> list of length q; constants(F, w) where
# w is a root of order q. C(e) = (w^e + w^-e)/2 and S(e) = (w^e - w^-e)/2.


def _pre2(x):
    return [x[0] + x[1], x[0] - x[1]]


def _post2(m):
    return [m[0], m[1]]


def _mu2(F, w):
    return [1, 1]


def _pre3(x):
    p, q = x[1] + x[2], x[1] - x[2]
    return [x[0] + p, p, q]


def _post3(m):
    b = m[0] + m[1]
    return [m[0], b + m[2], b - m[2]]


def _mu3(F, w):
    w2 = F.red(w * w)
    C1, S1 = F.div(w + w2, 2), F.div(w - w2, 2)
    return [1, C1 - 1, S1]


def _pre4(x):
    t1, t2, t3, t4 = x[0] + x[2], x[0] - x[2], x[1] + x[3], x[1] - x[3]
    return [t1 + t3, t1 - t3, t2, t4]


def _post4(m):
    return [m[0], m[2] + m[3], m[1], m[2] - m[3]]


def _mu4(F, w):
    return [1, 1, 1, w]


def _pre5(x):
    t0, t1, q0, q1 = x[1] + x[4], x[2] + x[3], x[1] - x[4], x[2] - x[3]
    s = t0 + t1
    return [x[0] + s, s, t0 - t1, q0 + q1, q0, q1]


def _post5(m):
    base = m[0] + m[1]
    r0, r1 = base + m[2], base - m[2]
    i0, i1 = m[3] + m[4], m[3] + m[5]
    return [m[0], r0 + i0, r1 + i1, r1 - i1, r0 - i0]


def _mu5(F, w):
    pw = [F.red(w**e) if F.p is not None else w**e for e in range(5)]
    C = lambda e: F.div(pw[e % 5] + pw[-e % 5], 2)
    S = lambda e: F.div(pw[e % 5] - pw[-e % 5], 2)
    c0, c1, s0, s1 = C(1), C(2), S(1), S(2)
    return [1, F.div(c0 + c1, 2) - 1, F.div(c0 - c1, 2), s1, s0 - s1, -(s0 + s1)]


def _pre7(x):
    p1, q1 = x[1] + x[6], x[1] - x[6]
    p3, q3 = x[3] + x[4], x[3] - x[4]
    p2, q2 = x[2] + x[5], x[2] - x[5]
    s = p1 + p2 + p3  # real part: cyclic convolution of (p1, p2, p3)
    d0, d1, e = p1 - p2, p2 - p3, p1 - p3
    s2 = q1 + q2 - q3  # imaginary part: (q1, q2, -q3) after the sign change
    f0, f1, f2 = q1 - q2, q2 + q3, q1 + q3
    return [x[0] + s, s, d0, d1, e, s2, f0, f1, f2]


def _post7(m):
    base = m[0] + m[1]
    w0, w1, w2 = m[2] - m[3], m[4] - m[2], m[3] - m[4]
    r0, r1, r2 = base + w0, base + w1, base + w2
    v0, v1, v2 = m[6] - m[7], m[8] - m[6], m[7] - m[8]
    u0, u1, u2 = m[5] + v0, m[5] + v1, m[5] + v2
    return [m[0], r0 + u0, r2 + u2, r1 - u1, r1 + u1, r2 - u2, r0 - u0]


def _mu7(F, w):
    pw = [F.red(w**e) if F.p is not None else w**e for e in range(7)]
    C = lambda e: F.div(pw[e % 7] + pw[-e % 7], 2)
    S = lambda e: F.div(pw[e % 7] - pw[-e % 7], 2)
    c = [C(1), C(3), C(2)]  # C(g^e) with g = 3
    t = [S(1), -S(3), S(2)]  # S(g^e) times the signs (1, -1, 1)
    H, T = sum(c), sum(t)
    g = [ce - F.div(H, 3) for ce in c]
    h = [te - F.div(T, 3) for te in t]
    return [1, F.div(H, 3) - 1, g[0], g[1], g[0] + g[1], F.div(T, 3), h[0], h[1], h[0] + h[1]]


def _pre8(x):
    s = [x[j] + x[j + 4] for j in range(4)]
    d = [x[j] - x[j + 4] for j in range(4)]
    t1, t2, t3, t4 = s[0] + s[2], s[0] - s[2], s[1] + s[3], s[1] - s[3]
    return [t1 + t3, t1 - t3, t2, t4, d[0], d[2], d[1] - d[3], d[1] + d[3]]


def _post8(m):
    a, b = m[4] + m[5], m[4] - m[5]
    P, Q = m[6] + m[7], m[7] - m[6]
    return [m[0], a + P, m[2] + m[3], b + Q, m[1], a - P, m[2] - m[3], b - Q]


def _mu8(F, w):
    J = F.red(w * w)
    c = F.red(w * F.inv(1 + J))  # a square root of 1/2
    return [1, 1, 1, J, 1, J, c, F.red(c * J)]


MODULES: dict[int, tuple[Callable, Callable, Callable]] = {
    2: (_pre2, _mu2, _post2),
    3: (_pre3, _mu3, _post3),
    4: (_pre4, _mu4, _post4),
    5: (_pre5, _mu5, _post5),
    7: (_pre7, _mu7, _post7),
    8: (_pre8, _mu8, _post8),
}


def module_constants(q: int, F: Field, wq) -> list:
    return [F.red(v) for v in MODULES[q][1](F, wq)]


# ---------------------------------------------------------------- nesting


def _along(a: list, shape: list[int], axis: int, fn: Callable, new: int) -> list:
    """Apply fn to every line of the row-major array a along axis; that axis gets length new."""
    inner = math.prod(shape[axis + 1 :])
    outer = math.prod(shape[:axis])
    L = shape[axis]
    out = [None] * (outer * new * inner)
    for o in range(outer):
        for i in range(inner):
            base_in, base_out = o * L * inner + i, o * new * inner + i
            y = fn([a[base_in + t * inner] for t in range(L)])
            for t in range(new):
                out[base_out + t * inner] = y[t]
    shape[axis] = new
    return out


def wfta(
    x: Sequence,
    factors: Sequence[int],
    w: int | None = None,
    p: int | None = None,
    inverse: bool = False,
) -> list:
    """DFT of x, len(x) = prod(factors), the factors pairwise coprime and in MODULES."""
    factors = list(factors)
    n = math.prod(factors)
    if len(x) != n:
        raise ValueError("len(x) must be the product of the factors")
    for a in range(len(factors)):
        if factors[a] not in MODULES:
            raise ValueError(f"no short module of length {factors[a]}")
        for b in range(a + 1, len(factors)):
            if math.gcd(factors[a], factors[b]) != 1:
                raise ValueError("the factors must be pairwise coprime")
    if inverse:
        F = Field(n, None if p is None else pow(w, -1, p), p, sign=+1)
    else:
        F = Field(n, w, p)
    if n == 1:
        return [F.red(x[0])]
    d = len(factors)
    shape = list(factors)
    a = []  # @line L1
    for flat in range(n):  # Ruritanian input map, j = sum_i j_i (n/q_i) mod n
        rest, j = flat, 0
        for i in range(d - 1, -1, -1):
            rest, ji = divmod(rest, factors[i])
            j += ji * (n // factors[i])
        a.append(x[j % n])
    mus = [module_constants(q, F, F.root(n // q)) for q in factors]  # @line L2
    ones = [[c == 1 for c in mu] for mu in mus]
    sizes = [len(mu) for mu in mus]
    for i, q in enumerate(factors):  # @line L3
        a = _along(a, shape, i, MODULES[q][0], sizes[i])
    for flat in range(len(a)):  # @line L4
        rest, c, triv = flat, 1, True
        for i in range(d - 1, -1, -1):
            rest, t = divmod(rest, sizes[i])
            c = F.red(c * mus[i][t])
            triv = triv and ones[i][t]
        if not triv:  # products of ones only are skipped
            a[flat] = F.red(a[flat] * c)
    for i in range(d - 1, -1, -1):  # @line L5
        post = MODULES[factors[i]][2]
        a = _along(a, shape, i, post, factors[i])
    a = [F.red(v) for v in a]
    X = []  # @line L6
    for k in range(n):
        flat = 0
        for q in factors:
            flat = flat * q + k % q
        X.append(a[flat])
    if inverse:
        X = [F.div(v, n) for v in X]
    return X


def counts(factors: Sequence[int]) -> tuple[int, int]:
    """(additions, multiplications) of wfta for this order of the factors."""
    A = {2: 2, 3: 6, 4: 8, 5: 17, 7: 36, 8: 26}
    M = {2: 2, 3: 3, 4: 4, 5: 6, 7: 9, 8: 8}
    U = {2: 2, 3: 1, 4: 3, 5: 1, 7: 1, 8: 4}  # constants equal to 1
    adds = 0
    for i, q in enumerate(factors):
        adds += A[q] * math.prod(M[r] for r in factors[:i]) * math.prod(factors[i + 1 :])
    mults = math.prod(M[q] for q in factors) - math.prod(U[q] for q in factors)
    return adds, mults
