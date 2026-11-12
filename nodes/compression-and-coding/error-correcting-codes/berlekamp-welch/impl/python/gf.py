# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berlekamp-welch/. The authors are listed in prov/7100GD.jsonl.
"""Arithmetic in GF(2^m) with log and antilog tables, and GF(p) for a prime p.

A GF(2^m) element is an int in [0, 2^m) whose bit i is the coefficient of
alpha^i in the polynomial basis, where alpha is a root of the primitive
polynomial `prim`, given with its x^m term: 0x13 is x^4 + x + 1, 0x11D is
x^8 + x^4 + x^3 + x^2 + 1 (QR codes), 0x187 is x^8 + x^7 + x^2 + x + 1
(CCSDS 131.0-B, conventional basis).

Both classes have the same methods: add, sub, mul, inv, pow and alpha, and
the attribute q, the number of elements. Elements are the ints 0 .. q - 1.
"""


class GF2m:
    """The field GF(2^m) built from a primitive polynomial of degree m."""

    def __init__(self, m: int, prim: int) -> None:
        if prim >> m != 1:
            raise ValueError("prim must have degree m")
        self.q = 1 << m
        self.n = self.q - 1  # the order of alpha
        self.exp = [0] * (2 * self.n)
        self.log = [-1] * self.q
        x = 1
        for i in range(self.n):
            if self.log[x] != -1:
                raise ValueError("the polynomial is not primitive")
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & self.q:
                x ^= prim
        if x != 1:
            raise ValueError("the polynomial is not primitive")
        for i in range(self.n, 2 * self.n):
            self.exp[i] = self.exp[i - self.n]

    def alpha(self, i: int) -> int:
        return self.exp[i % self.n]

    @staticmethod
    def add(a: int, b: int) -> int:
        return a ^ b

    @staticmethod
    def sub(a: int, b: int) -> int:
        return a ^ b

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError("0 has no inverse")
        return self.exp[(self.n - self.log[a]) % self.n]

    def pow(self, a: int, e: int) -> int:
        if a == 0:
            if e <= 0:
                raise ZeroDivisionError("0 to a power <= 0")
            return 0
        return self.exp[(self.log[a] * e) % self.n]


class GFp:
    """The field GF(p) for a prime p."""

    def __init__(self, p: int) -> None:
        if p < 2 or any(p % d == 0 for d in range(2, int(p ** 0.5) + 1)):
            raise ValueError("p must be a prime")
        self.p = p
        self.q = p
        self.n = p - 1

    def add(self, a: int, b: int) -> int:
        return (a + b) % self.p

    def sub(self, a: int, b: int) -> int:
        return (a - b) % self.p

    def mul(self, a: int, b: int) -> int:
        return a * b % self.p

    def inv(self, a: int) -> int:
        if a % self.p == 0:
            raise ZeroDivisionError("0 has no inverse")
        return pow(a, self.p - 2, self.p)

    def pow(self, a: int, e: int) -> int:
        if a % self.p == 0:
            if e <= 0:
                raise ZeroDivisionError("0 to a power <= 0")
            return 0
        return pow(a, e % self.n, self.p)
