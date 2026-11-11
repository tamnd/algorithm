# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naccache-stern-cryptosystem/. The authors are listed in prov/B6YRKD.jsonl.
#
# The Naccache-Stern higher residue cryptosystem (ACM CCS 1998), and at the end a toy of the
# different Naccache-Stern knapsack cryptosystem (Eurocrypt 1997).
# For study only. This code is not constant time, it has no protection against side
# channels, and it must not protect real data. Use an IND-CCA2 scheme from a vetted
# library (for example HPKE, RFC 9180) instead.

import random
from math import gcd, prod

_SMALL = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)


def is_probable_prime(n: int, rng: random.Random, rounds: int = 32) -> bool:
    """Miller-Rabin test with random bases."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for sp in _SMALL:
        if n % sp == 0:
            return n == sp
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
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


def small_odd_primes(count: int):
    out, n = [], 3
    while len(out) < count:
        if all(n % d for d in range(3, int(n ** 0.5) + 1, 2)):
            out.append(n)
        n += 2
    return out


def crt(residues, moduli):
    """The x modulo prod(moduli) with x = r_i (mod m_i), for pairwise coprime moduli."""
    M = prod(moduli)
    x = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        x += r * Mi * pow(Mi, -1, m)
    return x % M


def keygen_from(small_primes, a: int, b: int, rng: random.Random):
    """Keys from the small primes p_i and the primes a and b of p = 2au + 1 and q = 2bv + 1."""
    t = len(small_primes) // 2
    u, v = prod(small_primes[:t]), prod(small_primes[t:])  # @line L1
    sigma = u * v
    p, q = 2 * a * u + 1, 2 * b * v + 1  # @line L2
    if not (is_probable_prime(p, rng) and is_probable_prime(q, rng)):  # @line L3
        raise ValueError("p or q is not prime")
    n, phi = p * q, (p - 1) * (q - 1)  # @line L4
    order = phi // 4
    s = 2
    while True:
        g = s * s % n  # @line L5
        if gcd(g, n) == 1 and all(pow(g, order // f, n) != 1 for f in list(small_primes) + [a, b]):
            break
        s += 1
    tables = []
    for pi in small_primes:
        gi = pow(g, phi // pi, n)
        tables.append({pow(gi, j, n): j for j in range(pi)})
    return (sigma, n, g), (phi, tuple(small_primes), tables)  # @line L6


def keygen(count: int, abits: int, rng: random.Random):
    """count small odd primes (an even number), and random primes a and b of abits binary digits."""
    small = small_odd_primes(count)
    t = count // 2
    u, v = prod(small[:t]), prod(small[t:])

    def find(w):
        while True:
            a = rng.getrandbits(abits) | (1 << (abits - 1)) | 1
            if is_probable_prime(a, rng) and is_probable_prime(2 * a * w + 1, rng):
                return a

    a = find(u)
    b = find(v)
    while b == a:
        b = find(v)
    return keygen_from(small, a, b, rng)


def encrypt(pk, m: int, rng: random.Random, x: int = 0) -> int:
    sigma, n, g = pk
    if not 0 <= m < sigma:
        raise ValueError("the message must be in Z_sigma")
    while x == 0 or gcd(x, n) != 1:  # @line L7
        x = rng.randrange(2, n)
    return pow(g, m, n) * pow(x, sigma, n) % n  # @line L8


def encrypt_deterministic(pk, m: int) -> int:
    """The deterministic variant c = g^m mod N of the paper. It is not IND-CPA."""
    sigma, n, g = pk
    return pow(g, m % sigma, n)


def decrypt(pk, sk, c: int) -> int:
    sigma, n, g = pk
    phi, small, tables = sk
    residues = []
    for pi, table in zip(small, tables):  # @line L9
        ci = pow(c, phi // pi, n)  # @line L10
        if ci not in table:
            raise ValueError("not a ciphertext")
        residues.append(table[ci])  # @line L11
    return crt(residues, small)  # @line L12


def add(pk, c1: int, c2: int) -> int:
    """An encryption of m1 + m2 mod sigma."""
    return c1 * c2 % pk[1]


def mul_plain(pk, c: int, k: int) -> int:
    """An encryption of k * m mod sigma."""
    return pow(c, k % pk[0], pk[1])


# ---- the 1997 knapsack scheme, a different cryptosystem with the same authors ----


def knapsack_keygen(P: int, s: int, count: int):
    """Public v_i = p_i^(1/s) mod P for the first `count` primes p_i; needs prod(p_i) < P."""
    primes = [2] + small_odd_primes(count - 1)
    if prod(primes) >= P or gcd(s, P - 1) != 1:
        raise ValueError("bad parameters")
    d = pow(s, -1, P - 1)
    return [pow(pi, d, P) for pi in primes], (P, s, primes)


def knapsack_encrypt(P: int, vs, bits) -> int:
    return prod(v for v, bit in zip(vs, bits) if bit) % P


def knapsack_decrypt(sk, c: int):
    P, s, primes = sk
    w = pow(c, s, P)  # the product of the p_i with m_i = 1, as an integer below P
    return [1 if w % pi == 0 else 0 for pi in primes]
