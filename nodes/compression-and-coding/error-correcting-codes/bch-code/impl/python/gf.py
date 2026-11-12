# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bch-code/. The authors are listed in prov/RQPH9G.jsonl.
"""Arithmetic in GF(2^m) with log and antilog tables, and polynomials over it.

A field element is an int in [0, 2^m) whose bit i is the coefficient of
alpha^i in the polynomial basis, where alpha is a root of the primitive
polynomial `prim`. `prim` is given with its x^m term, for example 0x13 for
x^4 + x + 1, 0x25 for x^5 + x^2 + 1, or 0x11D for x^8 + x^4 + x^3 + x^2 + 1.

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

    # ---- elements
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

    def div(self, a: int, b: int) -> int:
        if b == 0:
            raise ZeroDivisionError("division by 0")
        if a == 0:
            return 0
        return self.exp[(self.log[a] - self.log[b]) % self.n]

    def pow(self, a: int, e: int) -> int:
        if a == 0:
            if e <= 0:
                raise ZeroDivisionError("0 to a power <= 0")
            return 0
        return self.exp[(self.log[a] * e) % self.n]

    # ---- polynomials, lowest degree first
    @staticmethod
    def trim(p: list[int]) -> list[int]:
        p = list(p)
        while p and p[-1] == 0:
            p.pop()
        return p

    def padd(self, p: list[int], r: list[int]) -> list[int]:
        out = [0] * max(len(p), len(r))
        for i, c in enumerate(p):
            out[i] ^= c
        for i, c in enumerate(r):
            out[i] ^= c
        return self.trim(out)

    def pscale(self, p: list[int], c: int) -> list[int]:
        return self.trim([self.mul(a, c) for a in p])

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

    def pdivmod(self, p: list[int], r: list[int]) -> tuple[list[int], list[int]]:
        r = self.trim(r)
        if not r:
            raise ZeroDivisionError("division by the zero polynomial")
        rem = self.trim(p)
        if len(rem) < len(r):
            return [], rem
        quo = [0] * (len(rem) - len(r) + 1)
        lead_inv = self.inv(r[-1])
        for i in range(len(rem) - len(r), -1, -1):
            c = self.mul(rem[i + len(r) - 1], lead_inv)
            quo[i] = c
            if c:
                for j, b in enumerate(r):
                    rem[i + j] ^= self.mul(c, b)
        return self.trim(quo), self.trim(rem[: len(r) - 1])

    def peval(self, p: list[int], x: int) -> int:
        """Horner's rule."""
        y = 0
        for c in reversed(p):
            y = self.mul(y, x) ^ c
        return y

    def pderiv(self, p: list[int]) -> list[int]:
        """Formal derivative. In characteristic 2, i * a_i is a_i for odd i and 0 for even i."""
        return self.trim([p[i] if i % 2 == 1 else 0 for i in range(1, len(p))])
