# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regev-encryption/. The authors are listed in prov/EKXD4J.jsonl.
"""Regev's public-key encryption of one bit from LWE (2005).

Key generation: A is a uniform m x n matrix over Z_q, s is uniform in Z_q^n,
e has m small error entries, and b = A s + e. The public key is (A, b).
Encryption of a bit mu: pick a random subset of the m rows (x in {0,1}^m),
send u = x^T A and v = x^T b + mu * floor(q/2). Decryption: d = v - <u, s>
= x^T e + mu * floor(q/2) mod q; output 1 when d is closer to q/2 than to 0.
Decryption is correct whenever |x^T e| < q/4.

The error is a rounded Gaussian, as in the paper. For study only: the
parameters in the tests are tiny, the code is not constant time, and it
must not be used to protect real data.
"""

import random


class Regev:
    def __init__(self, n, m, q, sigma):
        self.n, self.m, self.q, self.sigma = n, m, q, sigma

    def keygen(self, rng=None):
        rng = rng or random.SystemRandom()
        n, m, q = self.n, self.m, self.q
        a = [[rng.randrange(q) for _ in range(n)] for _ in range(m)]  # @line L1
        s = [rng.randrange(q) for _ in range(n)]
        e = [round(rng.gauss(0, self.sigma)) for _ in range(m)]  # @line L2
        b = [(sum(x * y for x, y in zip(row, s)) + ei) % q for row, ei in zip(a, e)]  # @line L3
        return (a, b), s  # @line L4

    def encrypt(self, pk, bit, rng=None):
        rng = rng or random.SystemRandom()
        a, b = pk
        q = self.q
        rows = [i for i in range(self.m) if rng.getrandbits(1)]  # @line L5
        u = [sum(a[i][j] for i in rows) % q for j in range(self.n)]  # @line L6
        v = (sum(b[i] for i in rows) + bit * (q // 2)) % q  # @line L7
        return u, v  # @line L8

    def decrypt(self, s, ct):
        u, v = ct
        q = self.q
        d = (v - sum(x * y for x, y in zip(u, s))) % q  # @line L9
        return 1 if q // 4 < d < q - q // 4 else 0  # @line L10
