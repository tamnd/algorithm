# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfsr-synthesis/. The authors are listed in prov/FQKAS9.jsonl.
"""Shortest LFSR synthesis over a prime field GF(p), three ways.

An LFSR (L, C) has length L and connection polynomial
C(x) = 1 + c_1 x + ... + c_L x^L, given as the list [1, c_1, ..., c_L]
(c_L may be 0). It generates s_0 .. s_{N-1} if, for L <= j < N,
s_j + c_1 s_{j-1} + ... + c_L s_{j-L} = 0  (mod p).

- shortest_lfsr_brute_force: the definition, for tiny inputs (the test oracle).
- shortest_lfsr_linear_algebra: for L = 0, 1, ..., solve the Hankel system
  by Gaussian elimination; O(N^4) operations in the worst case.
- shortest_lfsr_euclid: the extended Euclidean algorithm on x^N and the
  reversed sequence (the Pade or continued fraction method); O(N^2).

The Berlekamp-Massey algorithm, the usual O(N^2) method, has its own page.
"""

import itertools

Poly = list[int]  # lowest degree first, coefficients in 0 .. p - 1


def generates(s: list[int], L: int, c: Poly, p: int) -> bool:
    for j in range(L, len(s)):
        acc = s[j]
        for i in range(1, L + 1):
            acc += c[i] * s[j - i]
        if acc % p:
            return False
    return True


def shortest_lfsr_brute_force(s: list[int], p: int) -> tuple[int, list[Poly]]:
    """(L, all connection polynomials of length L that generate s), L least."""
    for L in range(len(s) + 1):
        found = [[1, *t] for t in itertools.product(range(p), repeat=L) if generates(s, L, [1, *t], p)]
        if found:
            return L, found
    raise AssertionError("an LFSR of length len(s) always works")


def _solve_mod_p(rows: list[list[int]], rhs: list[int], nvars: int, p: int) -> list[int] | None:
    """One solution of rows * x = rhs over GF(p), or None. Gaussian elimination."""
    a = [row[:] + [b] for row, b in zip(rows, rhs)]
    where = [-1] * nvars
    r = 0
    for col in range(nvars):
        piv = next((i for i in range(r, len(a)) if a[i][col] % p), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        inv = pow(a[r][col], p - 2, p)
        a[r] = [x * inv % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                f = a[i][col]
                a[i] = [(x - f * y) % p for x, y in zip(a[i], a[r])]
        where[col] = r
        r += 1
    if any(row[nvars] % p for row in a[r:]):
        return None
    return [a[where[c]][nvars] if where[c] >= 0 else 0 for c in range(nvars)]


def shortest_lfsr_linear_algebra(s: list[int], p: int) -> tuple[int, Poly]:
    """Least L whose system sum_{i=1}^{L} c_i s_{j-i} = -s_j (L <= j < N) has a solution."""
    n = len(s)
    for L in range(n + 1):
        rows = [[s[j - i] for i in range(1, L + 1)] for j in range(L, n)]
        rhs = [(-s[j]) % p for j in range(L, n)]
        sol = _solve_mod_p(rows, rhs, L, p)
        if sol is not None:
            return L, [1, *sol]
    raise AssertionError("L = len(s) always works")


# ---- polynomials over GF(p) for the Euclidean method
def _trim(a: Poly) -> Poly:
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def _deg(a: Poly) -> int:
    return len(_trim(a)) - 1  # -1 for the zero polynomial


def _sub(a: Poly, b: Poly, p: int) -> Poly:
    out = a + [0] * max(0, len(b) - len(a))
    for i, x in enumerate(b):
        out[i] = (out[i] - x) % p
    return _trim(out)


def _mul(a: Poly, b: Poly, p: int) -> Poly:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % p
    return _trim(out)


def _divmod(a: Poly, b: Poly, p: int) -> tuple[Poly, Poly]:
    a, b = _trim(a), _trim(b)
    inv = pow(b[-1], p - 2, p)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        c = a[-1] * inv % p
        shift = len(a) - len(b)
        q[shift] = c
        a = _sub(a, [0] * shift + [x * c % p for x in b], p)
    return _trim(q), a


def shortest_lfsr_euclid(s: list[int], p: int) -> tuple[int, Poly]:
    """Shortest LFSR from the extended Euclidean algorithm.

    Let A(x) = sum_k s_k x^(N-1-k). Run Euclid on r_(-1) = x^N, r_0 = A with
    v_(-1) = 0, v_0 = 1, keeping v_i A = r_i (mod x^N). At the first i with
    deg r_i < deg v_i, L = deg v_i and f = v_i / lc(v_i) is a monic
    characteristic polynomial of degree L; C(x) = x^L f(1/x).
    Cost: O(N^2) operations in GF(p).
    """
    n = len(s)
    r_prev, r = [0] * n + [1], _trim([s[n - 1 - e] % p for e in range(n)])
    v_prev, v = [], [1]
    while _deg(r) >= _deg(v):
        q, rem = _divmod(r_prev, r, p)
        r_prev, r = r, rem
        v_prev, v = v, _sub(v_prev, _mul(q, v, p), p)
    L = _deg(v)
    inv = pow(v[-1], p - 2, p)
    f = [x * inv % p for x in v]  # monic, degree L
    return L, list(reversed(f))  # C(x) = x^L f(1/x): c_i = f_(L-i)


def linear_complexity_profile(s: list[int], p: int) -> list[int]:
    """[L_1, ..., L_N] by the Euclidean method on each prefix."""
    return [shortest_lfsr_euclid(s[: r + 1], p)[0] for r in range(len(s))]
