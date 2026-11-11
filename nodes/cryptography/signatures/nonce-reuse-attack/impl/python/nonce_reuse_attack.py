# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonce-reuse-attack/. The authors are listed in prov/A3D86P.jsonl.
"""Two attacks on ECDSA and DSA nonces, run against local simulated signers.

1. Nonce reuse on secp256k1: two signatures with the same k give k and then
   the secret key d with two divisions mod n.
2. Partly known nonces on a toy DSA group with a 40-binary-digit q: the top
   binary digits of each k are known (as from a timing leak), and a lattice
   attack on the hidden number problem finds d. The LLL reduction here is a
   compact exact version (rational Gram-Schmidt data, as in Cohen's book).

For study only. This code is not constant time, the DSA group is tiny, and
the attacks run only against signers simulated in this file.
"""

import hashlib
import random
from fractions import Fraction

# ------------------------------------------------- 1. reuse on secp256k1
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)


def point_add(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    if a == b:
        lam = 3 * a[0] * a[0] * pow(2 * a[1], -1, P) % P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x3 = (lam * lam - a[0] - b[0]) % P
    return x3, (lam * (a[0] - x3) - a[1]) % P


def point_mul(a, k: int):
    result = None
    while k:
        if k & 1:
            result = point_add(result, a)
        a = point_add(a, a)
        k >>= 1
    return result


def z_of(msg: bytes) -> int:
    return int.from_bytes(hashlib.sha256(msg).digest(), "big")


def ecdsa_sign(d: int, msg: bytes, k: int) -> tuple[int, int]:
    r = point_mul(G, k)[0] % N
    return r, pow(k, -1, N) * (z_of(msg) + r * d) % N


def ecdsa_verify(q_pt, msg: bytes, r: int, s: int) -> bool:
    if not (1 <= r < N and 1 <= s < N):
        return False
    w = pow(s, -1, N)
    x_pt = point_add(point_mul(G, z_of(msg) * w % N), point_mul(q_pt, r * w % N))
    return x_pt is not None and x_pt[0] % N == r


def recover_from_reuse(m1: bytes, sig1: tuple[int, int], m2: bytes, sig2: tuple[int, int]) -> tuple[int, int]:
    """Same r means same k: k = (z1 - z2)/(s1 - s2), then d = (s1 k - z1)/r, all mod n."""
    (r1, s1), (r2, s2) = sig1, sig2
    assert r1 == r2, "the nonces differ"
    z1, z2 = z_of(m1), z_of(m2)
    k = (z1 - z2) * pow(s1 - s2, -1, N) % N
    d = (s1 * k - z1) * pow(r1, -1, N) % N
    return k, d


# ------------------------------------- 2. known top digits, toy DSA + LLL
def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in small:  # these bases are exact for n < 3.3 * 10^24
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def toy_dsa_group(qbits: int = 40, pbits: int = 72) -> tuple[int, int, int]:
    """Deterministic toy DSA parameters (p, q, g) with q | p - 1. Not secure."""
    q = (1 << (qbits - 1)) + 1
    while not is_probable_prime(q):
        q += 2
    c = (1 << (pbits - qbits)) // 2 * 2
    while not is_probable_prime(q * c + 1):
        c += 2
    p = q * c + 1
    h = 2
    while pow(h, c, p) == 1:
        h += 1
    return p, q, pow(h, c, p)


def dsa_sign(p: int, q: int, g: int, x: int, msg: bytes, k: int) -> tuple[int, int]:
    r = pow(g, k, p) % q
    return r, pow(k, -1, q) * (z_of(msg) % q + x * r) % q


def lll(basis: list[list[int]], delta: Fraction = Fraction(99, 100)) -> list[list[int]]:
    """LLL with exact rational Gram-Schmidt data, updated at each swap."""
    b = [row[:] for row in basis]
    n = len(b)
    mu = [[Fraction(0)] * n for _ in range(n)]
    bb: list[Fraction] = []
    star: list[list[Fraction]] = []
    for i in range(n):
        v = [Fraction(x) for x in b[i]]
        for j in range(i):
            mu[i][j] = sum(x * y for x, y in zip(b[i], star[j])) / bb[j]
            v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
        star.append(v)
        bb.append(sum(x * x for x in v))

    def size_reduce(k: int, j: int) -> None:
        r = round(mu[k][j])
        if r:
            b[k] = [x - r * y for x, y in zip(b[k], b[j])]
            for i in range(j):
                mu[k][i] -= r * mu[j][i]
            mu[k][j] -= r

    k = 1
    while k < n:
        size_reduce(k, k - 1)
        if delta * bb[k - 1] > bb[k] + mu[k][k - 1] ** 2 * bb[k - 1]:
            u = mu[k][k - 1]
            new_prev = bb[k] + u * u * bb[k - 1]
            mu[k][k - 1] = u * bb[k - 1] / new_prev
            bb[k] = bb[k - 1] * bb[k] / new_prev
            bb[k - 1] = new_prev
            b[k - 1], b[k] = b[k], b[k - 1]
            for j in range(k - 1):
                mu[k - 1][j], mu[k][j] = mu[k][j], mu[k - 1][j]
            for i in range(k + 1, n):
                t = mu[i][k]
                mu[i][k] = mu[i][k - 1] - u * t
                mu[i][k - 1] = t + mu[k][k - 1] * mu[i][k]
            k = max(1, k - 1)
        else:
            for j in range(k - 2, -1, -1):
                size_reduce(k, j)
            k += 1
    return b


def hnp_attack(q: int, sigs: list[tuple[bytes, int, int, int]], unknown_bits: int) -> list[int]:
    """Candidates for x from DSA signatures (msg, r, s, a) where a is k with its
    low `unknown_bits` binary digits set to 0, so k = a + b with 0 <= b < 2^unknown_bits.

    From s k = z + x r: b = t x + u (mod q) with t = r/s and u = z/s - a.
    The lattice holds (q (b_i - B/2), x B, q B), a short vector when B = 2^unknown_bits
    is small next to q (the embedding of Boneh-Venkatesan and Nguyen-Shparlinski).
    """
    m = len(sigs)
    big_b = 1 << unknown_bits
    ts, us = [], []
    for msg, r, s, a in sigs:
        sinv = pow(s, -1, q)
        ts.append(r * sinv % q)
        us.append((z_of(msg) % q * sinv - a - big_b // 2) % q)
    rows = []
    for i in range(m):
        row = [0] * (m + 2)
        row[i] = q * q
        rows.append(row)
    rows.append([q * t for t in ts] + [big_b, 0])
    rows.append([q * u for u in us] + [0, q * big_b])
    cands = []
    for row in lll(rows):
        if abs(row[-1]) == q * big_b and row[-2] % big_b == 0:
            sign = 1 if row[-1] > 0 else -1
            cands.append(sign * row[-2] // big_b % q)
    return cands


def leaky_signatures(seed: int, count: int, unknown_bits: int):
    """A local simulated DSA signer whose nonces leak their top binary digits."""
    p, q, g = toy_dsa_group()
    rng = random.Random(seed)
    x = rng.randrange(1, q)
    sigs = []
    for i in range(count):
        msg = b"leaky message %d" % i
        k = rng.randrange(1, q)
        r, s = dsa_sign(p, q, g, x, msg, k)
        a = k >> unknown_bits << unknown_bits  # the leak: all but the low digits
        sigs.append((msg, r, s, a))
    return (p, q, g, pow(g, x, p)), x, sigs
