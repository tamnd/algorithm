# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paillier-cryptosystem/. The authors are listed in prov/97TJVN.jsonl.
#
# The Paillier cryptosystem (Paillier, Eurocrypt 1999) with g = N + 1.
# For study only. This code is not constant time, it has no protection against
# side channels, and it must not protect real data. Use a maintained library
# (for example python-paillier "phe" or the Paillier code of a vetted MPC framework)
# with keys of at least 3072 bits.

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
    """A random prime with exactly `bits` binary digits."""
    while True:
        n = rng.getrandbits(bits) | (1 << (bits - 1)) | (1 << (bits - 2)) | 1
        if is_probable_prime(n, rng):
            return n


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def keygen_from_primes(p: int, q: int):
    """Keys from two primes. Returns (public key N, private key (N, lam, mu))."""
    if p == q or gcd(p * q, (p - 1) * (q - 1)) != 1:  # @line L1
        raise ValueError("need distinct primes with gcd(pq, (p-1)(q-1)) = 1")
    n, lam = p * q, lcm(p - 1, q - 1)  # @line L2
    # With g = N + 1, L(g^lam mod N^2) = lam mod N, so mu = lam^(-1) mod N.
    mu = pow(lam, -1, n)  # @line L3
    return n, (n, lam, mu)  # @line L4


def keygen(bits: int, rng: random.Random):
    """Keys with an N of `bits` binary digits (two primes of bits/2 digits each)."""
    while True:
        p = random_prime(bits // 2, rng)
        q = random_prime(bits // 2, rng)
        if p != q and (p * q).bit_length() == bits:
            return keygen_from_primes(p, q)


def L(x: int, n: int) -> int:
    """L(x) = (x - 1) / N, for x = 1 (mod N)."""
    return (x - 1) // n


def encrypt(n: int, m: int, rng: random.Random, r: int = 0) -> int:
    """c = g^m r^N mod N^2 with g = N + 1, so g^m = 1 + mN (mod N^2)."""
    if not 0 <= m < n:
        raise ValueError("the message must be in Z_N")
    n2 = n * n
    while r == 0 or gcd(r, n) != 1:  # @line L5
        r = rng.randrange(1, n)
    c = (1 + m * n) * pow(r, n, n2) % n2  # @line L6
    return c  # @line L7


def decrypt(sk, c: int) -> int:
    n, lam, mu = sk
    n2 = n * n
    if not 0 < c < n2 or gcd(c, n) != 1:  # @line L8
        raise ValueError("not a ciphertext")
    u = pow(c, lam, n2)  # @line L9
    return L(u, n) * mu % n  # @line L10


def add(n: int, c1: int, c2: int) -> int:
    """An encryption of m1 + m2 mod N."""
    return c1 * c2 % (n * n)


def add_plain(n: int, c: int, k: int) -> int:
    """An encryption of m + k mod N, without fresh randomness."""
    n2 = n * n
    return c * (1 + (k % n) * n) % n2


def mul_plain(n: int, c: int, k: int) -> int:
    """An encryption of k * m mod N."""
    return pow(c, k % n, n * n)


def rerandomize(n: int, c: int, rng: random.Random) -> int:
    """Multiply by a fresh encryption of 0, so the result does not link to c."""
    return add(n, c, encrypt(n, 0, rng))
