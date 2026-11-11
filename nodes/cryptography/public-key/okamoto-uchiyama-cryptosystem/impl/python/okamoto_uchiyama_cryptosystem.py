# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/okamoto-uchiyama-cryptosystem/. The authors are listed in prov/4VE7MR.jsonl.
#
# The Okamoto-Uchiyama cryptosystem (Eurocrypt 1998) with N = p^2 q.
# For study only. This code is not constant time, it has no protection against
# side channels, and it must not protect real data: plain Okamoto-Uchiyama falls
# to a chosen ciphertext attack that factors N (see the tests). Use a vetted library
# and an IND-CCA2 scheme such as RSA-OAEP or HPKE (RFC 9180) instead.

import random
from math import gcd

_SMALL_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)


def is_probable_prime(n: int, rng: random.Random, rounds: int = 32) -> bool:
    """Miller-Rabin test with random bases."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for sp in _SMALL_PRIMES:
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


def random_prime(bits: int, rng: random.Random) -> int:
    while True:
        n = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(n, rng):
            return n


def L(x: int, p: int) -> int:
    """L(x) = (x - 1) / p for x = 1 (mod p)."""
    return (x - 1) // p


def keygen_from_primes(p: int, q: int, rng: random.Random, g: int = 0):
    """Public key (N, g, h, k) and private key (p, q, g_p, L(g_p)^(-1) mod p)."""
    k = p.bit_length()
    if p == q:  # @line L1
        raise ValueError("need two distinct primes")
    n = p * p * q  # @line L2
    p2 = p * p
    while True:
        if g == 0:
            g = rng.randrange(2, n)  # @line L3
        gp = pow(g, p - 1, p2)
        if gcd(g, n) == 1 and gp != 1:  # @line L4
            break
        g = 0
    h = pow(g, n, n)  # @line L5
    inv = pow(L(gp, p), -1, p)
    return (n, g, h, k), (p, q, gp, inv)  # @line L6


def keygen(k: int, rng: random.Random):
    """Two primes of k binary digits each, so N has about 3k binary digits."""
    while True:
        p, q = random_prime(k, rng), random_prime(k, rng)
        if p != q:
            return keygen_from_primes(p, q, rng)


def encrypt(pk, m: int, rng: random.Random, r: int = -1) -> int:
    n, g, h, k = pk
    if not 0 <= m < (1 << (k - 1)):  # messages below 2^(k-1) < p
        raise ValueError("the message must be below 2^(k-1)")
    if r < 0:
        r = rng.randrange(1, n)  # @line L7
    return pow(g, m, n) * pow(h, r, n) % n  # @line L8


def decrypt(sk, c: int) -> int:
    p, q, gp, inv = sk
    cp = pow(c, p - 1, p * p)  # @line L9
    return L(cp, p) * inv % p  # @line L10


def add(pk, c1: int, c2: int) -> int:
    """An encryption of m1 + m2, correct while the sum stays below p."""
    return c1 * c2 % pk[0]


def raw_encrypt(pk, m: int, r: int) -> int:
    """g^m h^r mod N for any integer m >= 0: the attack in the tests uses it with m > p."""
    n, g, h, _ = pk
    return pow(g, m, n) * pow(h, r, n) % n
