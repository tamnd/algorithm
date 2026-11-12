# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chien-search/. The authors are listed in prov/GDVWFM.jsonl.
"""Arithmetic in GF(2^m) with log and antilog tables, and polynomials over it.

A field element is an int in [0, 2^m) whose bit i is the coefficient of
alpha^i in the polynomial basis, where alpha is a root of the primitive
polynomial `prim`. `prim` is given with its x^m term, for example 0x13 for
x^4 + x + 1, or 0x11D for x^8 + x^4 + x^3 + x^2 + 1 (QR codes).

A polynomial is a list of field elements, lowest degree first:
[a0, a1, a2] is a0 + a1 x + a2 x^2. The zero polynomial is [].
"""


class GF2m:
    """The field GF(2^m) built from a primitive polynomial of degree m."""

    def __init__(self, m: int, prim: int) -> None:
        if prim >> m != 1:
            raise ValueError("prim must have degree m")
        self.m = m
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
        """Return alpha^i for any integer i (negative i is allowed)."""
        return self.exp[i % self.n]

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError("0 has no inverse")
        return self.exp[(self.n - self.log[a]) % self.n]

    @staticmethod
    def trim(p: list[int]) -> list[int]:
        p = list(p)
        while p and p[-1] == 0:
            p.pop()
        return p

    def pmul(self, p: list[int], r: list[int]) -> list[int]:
        if not p or not r:
            return []
        out = [0] * (len(p) + len(r) - 1)
        for i, a in enumerate(p):
            if a:
                for j, b in enumerate(r):
                    if b:
                        out[i + j] ^= self.mul(a, b)
        return self.trim(out)

    def peval(self, p: list[int], x: int) -> int:
        """Horner's rule."""
        y = 0
        for c in reversed(p):
            y = self.mul(y, x) ^ c
        return y
