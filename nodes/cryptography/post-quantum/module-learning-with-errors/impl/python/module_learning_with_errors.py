# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/module-learning-with-errors/. The authors are listed in prov/4H2DFX.jsonl.
"""Module-LWE over R_q = Z_3329[x]/(x^256 + 1) with the NTT of FIPS 203.

ntt(), ntt_inv(), multiply_ntts() and base_case_multiply() follow FIPS 203
(ML-KEM), Algorithms 9, 10, 11 and 12: a 7-layer NTT with zeta = 17, a
primitive 256-th root of unity mod 3329, so x^256 + 1 splits only into 128
factors x^2 - gamma and the product in the NTT domain multiplies pairs of
coefficients (degree-1 polynomials) modulo x^2 - gamma.
sample_poly_cbd() is FIPS 203 Algorithm 8 (centered binomial distribution)
on bytes from a caller-given source (here random.Random, not SHAKE).
sample_module_lwe() returns (A, t = A s + e) with A a k x k matrix over R_q.

For study only. This is not ML-KEM: there is no SHAKE-based sampling, no
encoding and no compression. The code is not constant time. Use a FIPS 140
validated ML-KEM module for real data.
"""

import random
from typing import List, Sequence, Tuple

Q = 3329
N = 256
ZETA = 17
Poly = List[int]
PolyVec = List[Poly]


def bit_rev7(i: int) -> int:
    """Reverse the 7 low bits of i (FIPS 203, BitRev7)."""
    r = 0
    for _ in range(7):
        r = (r << 1) | (i & 1)
        i >>= 1
    return r


ZETAS = [pow(ZETA, bit_rev7(i), Q) for i in range(128)]  # FIPS 203 Appendix A, first table
GAMMAS = [pow(ZETA, 2 * bit_rev7(i) + 1, Q) for i in range(128)]  # second table


def ntt(f: Sequence[int]) -> Poly:
    """FIPS 203 Algorithm 9, NTT(f). Cost: 7 layers of 128 butterflies."""
    f = [x % Q for x in f]
    i = 1
    length = 128
    while length >= 2:
        for start in range(0, N, 2 * length):
            zeta = ZETAS[i]
            i += 1
            for j in range(start, start + length):
                t = zeta * f[j + length] % Q
                f[j + length] = (f[j] - t) % Q
                f[j] = (f[j] + t) % Q
        length //= 2
    return f


def ntt_inv(f_hat: Sequence[int]) -> Poly:
    """FIPS 203 Algorithm 10, NTT^-1. The final factor 3303 is 128^-1 mod 3329."""
    f = list(f_hat)
    i = 127
    length = 2
    while length <= 128:
        for start in range(0, N, 2 * length):
            zeta = ZETAS[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (t + f[j + length]) % Q
                f[j + length] = zeta * (f[j + length] - t) % Q
        length *= 2
    return [x * 3303 % Q for x in f]


def base_case_multiply(a0: int, a1: int, b0: int, b1: int, gamma: int) -> Tuple[int, int]:
    """FIPS 203 Algorithm 12: (a0 + a1 X)(b0 + b1 X) mod (X^2 - gamma)."""
    c0 = (a0 * b0 + a1 * b1 * gamma) % Q
    c1 = (a0 * b1 + a1 * b0) % Q
    return c0, c1


def multiply_ntts(f_hat: Sequence[int], g_hat: Sequence[int]) -> Poly:
    """FIPS 203 Algorithm 11: the product of two polynomials in the NTT domain."""
    h = [0] * N
    for i in range(128):
        h[2 * i], h[2 * i + 1] = base_case_multiply(
            f_hat[2 * i], f_hat[2 * i + 1], g_hat[2 * i], g_hat[2 * i + 1], GAMMAS[i]
        )
    return h


def mul_schoolbook(a: Sequence[int], b: Sequence[int], q: int = Q) -> Poly:
    """a b in Z_q[x]/(x^n + 1) by the O(n^2) method, for testing."""
    n = len(a)
    c = [0] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n):
            if i + j < n:
                c[i + j] += a[i] * b[j]
            else:
                c[i + j - n] -= a[i] * b[j]
    return [x % q for x in c]


def sample_poly_cbd(data: bytes, eta: int) -> Poly:
    """FIPS 203 Algorithm 8, SamplePolyCBD_eta, on 64 eta bytes.

    Coefficient i is the sum of eta bits minus the sum of the next eta bits.
    """
    assert len(data) == 64 * eta
    bits = [(byte >> k) & 1 for byte in data for k in range(8)]  # BytesToBits, little-endian
    f = []
    for i in range(N):
        x = sum(bits[2 * i * eta + j] for j in range(eta))
        y = sum(bits[2 * i * eta + eta + j] for j in range(eta))
        f.append((x - y) % Q)
    return f


def add(a: Sequence[int], b: Sequence[int]) -> Poly:
    return [(x + y) % Q for x, y in zip(a, b)]


def sample_module_lwe(
    k: int, eta1: int, eta2: int, rng: random.Random
) -> Tuple[List[PolyVec], PolyVec, PolyVec, PolyVec, PolyVec]:
    """One Module-LWE instance of rank k in the style of ML-KEM key generation.

    A_hat is uniform in the NTT domain (ML-KEM samples it with SHAKE128 by
    rejection; here the random module stands in for it). s and e are CBD.
    Returns (A_hat, t, t_hat, s, e) with t = NTT^-1(A_hat o NTT(s)) + e.
    """
    A_hat = [[[rng.randrange(Q) for _ in range(N)] for _ in range(k)] for _ in range(k)]
    s = [sample_poly_cbd(rng.randbytes(64 * eta1), eta1) for _ in range(k)]
    e = [sample_poly_cbd(rng.randbytes(64 * eta2), eta2) for _ in range(k)]
    s_hat = [ntt(p) for p in s]
    t_hat = []
    for i in range(k):
        acc = [0] * N
        for j in range(k):
            acc = add(acc, multiply_ntts(A_hat[i][j], s_hat[j]))
        t_hat.append(add(acc, ntt(e[i])))
    t = [ntt_inv(p) for p in t_hat]
    return A_hat, t, t_hat, s, e


def centered(x: int, q: int = Q) -> int:
    x %= q
    return x - q if x > q // 2 else x
