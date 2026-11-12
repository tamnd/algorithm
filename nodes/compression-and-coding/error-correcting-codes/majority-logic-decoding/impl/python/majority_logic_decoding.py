# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/majority-logic-decoding/. The authors are listed in prov/PD1H78.jsonl.

"""Majority-logic decoding.

* reed_decode: Reed's multi-step majority-logic decoder for the Reed-Muller code RM(r, m).
  It recovers the polynomial coefficients from the top degree down, by majority votes over
  2^(m - l) disjoint check sums per coefficient of degree l.
* one_step_decode: one-step majority-logic decoding (Massey) of a cyclic code from J parity
  checks orthogonal on the last position.

Positions of RM(r, m) are the points p of GF(2)^m, p in range(2^m), bit i of p = x_i.
A polynomial is a set of monomials; a monomial is a frozenset S of variable indices.
"""

from itertools import combinations


def monomials_of_degree(l: int, m: int) -> list[tuple[int, ...]]:
    return list(combinations(range(m), l))


def submasks(mask: int) -> list[int]:
    """All sub = subsets of the bit set mask, the points of V_S = span{e_i : i in S}."""
    out, sub = [], mask
    while True:
        out.append(sub)
        if sub == 0:
            return out
        sub = (sub - 1) & mask


def monomial_table(s: tuple[int, ...], m: int) -> list[int]:
    mask = sum(1 << i for i in s)
    return [1 if p & mask == mask else 0 for p in range(1 << m)]


def rm_encode(poly: set[tuple[int, ...]], m: int) -> list[int]:
    """Value table of the polynomial sum_{S in poly} x_S."""
    word = [0] * (1 << m)
    for s in poly:
        for p, v in enumerate(monomial_table(s, m)):
            word[p] ^= v
    return word


def reed_decode(y: list[int], r: int, m: int) -> set[tuple[int, ...]]:
    """Reed's decoder. y is a received word of RM(r, m). Returns the decoded polynomial.
    It is the transmitted one whenever at most 2^(m - r - 1) - 1 positions are in error."""
    n = 1 << m
    y = list(y)
    f: set[tuple[int, ...]] = set()  # @line L1
    for l in range(r, -1, -1):  # @line L2
        found = []
        for s in monomials_of_degree(l, m):  # @line L3
            mask = sum(1 << i for i in s)
            ones = 0  # @line L4
            for base in range(n):  # @line L5
                if base & mask:
                    continue  # base runs over the coset representatives: points with x_S = 0
                ones += sum(y[base | sub] for sub in submasks(mask)) & 1  # @line L6
            if 2 * ones > n >> l:  # @line L7
                found.append(s)
        for s in found:  # @line L8
            for p, v in enumerate(monomial_table(s, m)):
                y[p] ^= v
        f.update(found)  # @line L9
    return f  # @line L10


# ------------------------------------------------------------------ one-step decoding

def cyclic_generator_rows(g: int, n: int) -> list[int]:
    """Rows x^i g(x), i < n - deg g, of a cyclic code. Words are ints, bit j = position j."""
    k = n - (g.bit_length() - 1)
    return [g << i for i in range(k)]


def span(rows: list[int]) -> list[int]:
    words = [0]
    for row in rows:
        words += [w ^ row for w in words]
    return words


def dual_words(rows: list[int], n: int) -> list[int]:
    """All u with u . c = 0 for every generator row c."""
    return [u for u in range(1 << n) if all(((u & c).bit_count() & 1) == 0 for c in rows)]


def orthogonal_checks(dual: list[int], pos: int, j: int) -> list[int] | None:
    """Find j dual codewords that all contain pos and pairwise share no other position."""
    cands = sorted((u for u in dual if (u >> pos) & 1), key=lambda u: (u.bit_count(), u))
    bit = 1 << pos

    def search(start: int, chosen: list[int], used: int) -> list[int] | None:
        if len(chosen) == j:
            return chosen
        for i in range(start, len(cands)):
            u = cands[i]
            if (u & ~bit) & used == 0:
                got = search(i + 1, chosen + [u], used | (u & ~bit))
                if got:
                    return got
        return None

    return search(0, [], 0)


def rotate(word: int, k: int, n: int) -> int:
    """Cyclic shift by k positions: bit j moves to position (j + k) mod n."""
    k %= n
    return ((word << k) | (word >> (n - k))) & ((1 << n) - 1)


def one_step_decode(r: int, checks: list[int], n: int) -> int:
    """One-step majority-logic decoding of a cyclic code of length n.

    checks are J parity checks orthogonal on position n - 1. For position i the rotated
    checks are orthogonal on i, and bit i is flipped when more than J/2 of them fail.
    Every pattern of at most floor(J/2) errors is corrected."""
    j = len(checks)
    out = r
    for i in range(n):
        fails = sum((r & rotate(c, i - (n - 1), n)).bit_count() & 1 for c in checks)
        if 2 * fails > j:
            out ^= 1 << i
    return out
