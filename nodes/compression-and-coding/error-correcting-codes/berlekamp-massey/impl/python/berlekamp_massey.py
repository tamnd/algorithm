# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berlekamp-massey/. The authors are listed in prov/VWBGTF.jsonl.
"""The Berlekamp-Massey algorithm over any field.

A field object has the attributes zero and one and the methods add, sub, mul
and inv. PrimeField below is GF(p); gf.GF2m is GF(2^m).

An LFSR (L, C) has length L and connection polynomial
C(x) = 1 + c_1 x + ... + c_L x^L (lowest degree first, c_0 = 1). It generates
s_0 .. s_{N-1} if s_j + c_1 s_{j-1} + ... + c_L s_{j-L} = 0 for L <= j < N.
"""

from typing import Protocol


class Field(Protocol):
    zero: int
    one: int

    def add(self, a: int, b: int) -> int: ...
    def sub(self, a: int, b: int) -> int: ...
    def mul(self, a: int, b: int) -> int: ...
    def inv(self, a: int) -> int: ...


class PrimeField:
    """GF(p) for a prime p, elements 0 .. p - 1."""

    zero = 0
    one = 1

    def __init__(self, p: int) -> None:
        if p < 2 or any(p % d == 0 for d in range(2, int(p ** 0.5) + 1)):
            raise ValueError("p must be a prime")
        self.p = p

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


def _minus_shifted(f: Field, c: list[int], coef: int, shift: int, b_poly: list[int]) -> list[int]:
    """Return C(x) - coef * x^shift * B(x)."""
    out = c + [f.zero] * max(0, shift + len(b_poly) - len(c))
    for i, bi in enumerate(b_poly):
        if bi != f.zero:
            out[shift + i] = f.sub(out[shift + i], f.mul(coef, bi))
    return out


def berlekamp_massey(s: list[int], f: Field) -> tuple[int, list[int]]:
    """Return (L, C) for a shortest LFSR that generates s_0 .. s_{N-1}.

    Precondition: the items of s are elements of the field f.
    Cost: O(N^2) field operations and O(N) space, N = len(s).
    C is returned with exactly L + 1 coefficients (c_0 = 1, c_L may be 0).
    """
    c, b_poly, L, m, b = [f.one], [f.one], 0, 1, f.one  # @line L1
    for r in range(len(s)):  # @line L2
        d = s[r]  # @line L3: the discrepancy
        for i in range(1, min(L, len(c) - 1) + 1):
            d = f.add(d, f.mul(c[i], s[r - i]))
        if d == f.zero:  # @line L4
            m += 1
        elif 2 * L <= r:  # @line L5
            t = c  # @line L6
            c = _minus_shifted(f, c, f.mul(d, f.inv(b)), m, b_poly)  # @line L7
            L, b_poly, b, m = r + 1 - L, t, d, 1  # @line L8
        else:  # @line L9
            c = _minus_shifted(f, c, f.mul(d, f.inv(b)), m, b_poly)  # @line L10
            m += 1  # @line L11
    c = (c + [f.zero] * (L + 1))[: L + 1]  # @line L12: deg C <= L
    return L, c


def linear_complexity_profile(s: list[int], f: Field) -> list[int]:
    """[L_1, ..., L_N]: the length of a shortest LFSR for each prefix s_0 .. s_{r}."""
    return [berlekamp_massey(s[: r + 1], f)[0] for r in range(len(s))]


def generates(s: list[int], L: int, c: list[int], f: Field) -> bool:
    """True when the LFSR (L, C) generates the whole of s."""
    for j in range(L, len(s)):
        acc = s[j]
        for i in range(1, L + 1):
            if i < len(c):
                acc = f.add(acc, f.mul(c[i], s[j - i]))
        if acc != f.zero:
            return False
    return True


def error_locator_from_syndromes(syn: list[int], f: Field) -> list[int]:
    """Lambda(x) for Reed-Solomon or BCH decoding, from S_b .. S_(b+2t-1).

    With S_j = sum_k Y_k X_k^j, the error locator Lambda(x) = prod_k (1 - X_k x)
    is the connection polynomial of the syndrome sequence when at most t errors
    occurred. The result is trimmed of zero top coefficients.
    """
    _, lam = berlekamp_massey(syn, f)
    while len(lam) > 1 and lam[-1] == f.zero:
        lam.pop()
    return lam
