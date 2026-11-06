# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/menezes-okamoto-vanstone-reduction/. The authors are listed in prov/HWKGB7.jsonl.

import random
from math import isqrt

Point = tuple[int, int] | None  # affine (x, y), or None for the point at infinity
F2 = tuple[int, int]  # a + b i in F_p[i]/(i^2 + 1)


def ec_add(P: Point, Q: Point, p: int) -> Point:
    """Sum of two points on y^2 = x^3 + x over F_p."""
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        lam = (3 * x1 * x1 + 1) * pow(2 * y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    return x3, (lam * (x1 - x3) - y1) % p


def ec_mul(k: int, P: Point, p: int) -> Point:
    """k P by double and add, for k >= 0."""
    R: Point = None
    while k:
        if k & 1:
            R = ec_add(R, P, p)
        P = ec_add(P, P, p)
        k >>= 1
    return R


def _fmul(u: F2, v: F2, p: int) -> F2:
    return (u[0] * v[0] - u[1] * v[1]) % p, (u[0] * v[1] + u[1] * v[0]) % p


def _fpow(u: F2, e: int, p: int) -> F2:
    r: F2 = (1, 0)
    while e:
        if e & 1:
            r = _fmul(r, u, p)
        u = _fmul(u, u, p)
        e >>= 1
    return r


def _prime_factors(m: int) -> list[int]:
    out, d = [], 2
    while d * d <= m:
        if m % d == 0:
            out.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def _order(Q: Point, n: int, p: int) -> int:
    """Exact order of a point Q with n Q = O."""
    d = n
    for r in _prime_factors(n):
        while d % r == 0 and ec_mul(d // r, Q, p) is None:
            d //= r
    return d


def tate(T0: Point, R: tuple[F2, F2], m: int, p: int) -> F2:
    """Reduced Tate pairing f_{m,T0}(R)^((p^2 - 1)/m) by Miller's algorithm.

    T0 is in E(F_p) of odd order m with m | p + 1, and R = (x_R, y_R) is a point
    of E(F_{p^2}) with x_R in F_p and y_R not in F_p, so that vertical lines,
    whose values lie in F_p^*, are killed by the final exponentiation.
    """
    (xr, _), yr = R[0], R[1]
    f: F2 = (1, 0)  # @line L9
    T = T0
    for bit in bin(m)[3:]:  # @line L10
        x, y = T
        lam = (3 * x * x + 1) * pow(2 * y, -1, p) % p
        line = ((yr[0] - y - lam * (xr - x)) % p, yr[1])  # tangent at T, evaluated at R
        f = _fmul(_fmul(f, f, p), line, p)  # @line L11
        T = ec_add(T, T, p)
        if bit == "1":  # @line L12
            x, y = T
            x0, y0 = T0
            if x != x0:  # otherwise T = -T0 and the line is vertical
                lam = (y0 - y) * pow(x0 - x, -1, p) % p
                line = ((yr[0] - y - lam * (xr - x)) % p, yr[1])
                f = _fmul(f, line, p)
            T = ec_add(T, T0, p)
    return _fpow(f, (p * p - 1) // m, p)  # @line L13


def _log_mu(alpha: F2, beta: F2, n: int, p: int) -> int | None:
    """Baby-step giant-step for alpha^x = beta in F_{p^2}, alpha of order n."""
    m = isqrt(n) + 1
    table: dict[F2, int] = {}
    e: F2 = (1, 0)
    for j in range(m):
        table.setdefault(e, j)
        e = _fmul(e, alpha, p)
    giant = _fpow(alpha, n - m % n, p)  # alpha^(-m)
    y = beta
    for i in range(m + 1):
        if y in table:
            return (i * m + table[y]) % n
        y = _fmul(y, giant, p)
    return None


def mov_reduction(P: Point, Q: Point, n: int, p: int, seed: int = 0) -> int | None:
    """MOV reduction on the supersingular curve y^2 = x^3 + x over F_p, p = 3 mod 4.

    Return the x in [0, n) with x P = Q, or None if Q is not a multiple of P.
    The problem is moved by the reduced Tate pairing with the distortion map
    psi(x, y) = (-x, i y) into the order n subgroup of F_{p^2}^*, where it is
    solved here by baby-step giant-step.
    Precondition: p is prime, p = 3 (mod 4), P and Q lie on the curve, and
    P has exact order n, which must be odd (so the embedding degree is 2).
    Raises ValueError if p % 4 != 3 or n is even.
    Cost: O(log n) operations in F_{p^2} per pairing (Miller's algorithm and
    the final exponentiation), an expected n / phi(n) pairings to find a good
    R, and O(n^(1/2)) multiplications in F_{p^2} for the transferred logarithm.
    """
    if p % 4 != 3 or n % 2 == 0:
        raise ValueError("need p = 3 (mod 4) and odd n")
    if ec_mul(n, Q, p) is not None:  # @line L1
        return None
    if Q is None:  # @line L2
        return 0
    rng = random.Random(seed)
    primes = _prime_factors(n)
    d = _order(Q, n, p)
    while True:  # @line L3
        x0 = rng.randrange(p)  # @line L4
        rhs = (x0 * x0 * x0 + x0) % p
        y0 = pow(rhs, (p + 1) // 4, p)
        if rhs == 0 or y0 * y0 % p != rhs:
            continue
        if rng.randrange(2):
            y0 = p - y0
        R = ((-x0 % p, 0), (0, y0))  # psi(x0, y0) = (-x0, i y0)
        alpha = tate(P, R, n, p)  # @line L5
        if any(_fpow(alpha, n // r, p) == (1, 0) for r in primes):
            continue
        beta = tate(Q, R, d, p)  # @line L6
        x = _log_mu(alpha, beta, n, p)  # @line L7
        assert x is not None and ec_mul(x, P, p) == Q
        return x  # @line L8
