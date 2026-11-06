# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/garner-algorithm/. The authors are listed in prov/PHSQZC.jsonl.

"""Garner's algorithm: Chinese remaindering through mixed-radix digits.

Given pairwise coprime moduli m_1, ..., m_t and residues v_i modulo m_i, it
finds the unique x with 0 <= x < M = m_1 ... m_t and x = v_i (mod m_i). The
digits u_i of x in the mixed radix (m_1, ..., m_t),

    x = u_1 + u_2 m_1 + u_3 m_1 m_2 + ... + u_t m_1 ... m_(t-1),

are computed with operations modulo m_i only. The setup stores the t - 1
constants C_i = (m_1 ... m_(i-1))^(-1) mod m_i. Only the last step, which
evaluates x from its digits, works with numbers as large as M.
"""

from typing import List, NamedTuple, Sequence, Tuple


class Garner(NamedTuple):
    m: Tuple[int, ...]  # the moduli
    c: Tuple[int, ...]  # c[i] = (m[0] ... m[i-1])^(-1) mod m[i], c[0] = 0


def _inverse(a: int, n: int) -> Tuple[int, int]:
    """Return (g, u) with g = gcd(a, n) and u * a = g (mod n), by the
    extended Euclidean algorithm with a loop."""
    r0, r1 = n, a % n
    u0, u1 = 0, 1
    while r1 != 0:
        t = r0 // r1
        r0, r1 = r1, r0 - t * r1
        u0, u1 = u1, u0 - t * u1
    return r0, u0 % n


def garner_setup(moduli: Sequence[int]) -> Garner:
    """Precompute the constants C_i; raise ValueError if the moduli are not
    positive and pairwise coprime."""
    m = tuple(moduli)
    if any(mi < 1 for mi in m):
        raise ValueError("the moduli must be positive integers")
    c = [0] * len(m)
    for i in range(1, len(m)):  # @line L1
        p = 1
        for j in range(i):  # @line L2
            p = p * (m[j] % m[i]) % m[i]
        g, c[i] = _inverse(p, m[i])  # @line L3
        if g != 1:  # @line L4
            raise ValueError(f"modulus {m[i]} is not coprime to the earlier moduli")
    return Garner(m, tuple(c))


def garner_digits(residues: Sequence[int], ctx: Garner) -> List[int]:
    """Return the mixed-radix digits u_i, with 0 <= u_i < m_i."""
    m, c = ctx.m, ctx.c
    t = len(m)
    if len(residues) != t:
        raise ValueError("one residue per modulus is needed")
    if t == 0:
        return []
    u = [0] * t
    u[0] = residues[0] % m[0]  # @line L5
    for i in range(1, t):  # @line L6
        s = u[i - 1] % m[i]  # @line L7
        for j in range(i - 2, -1, -1):  # @line L8
            s = (s * m[j] + u[j]) % m[i]  # @line L9
        u[i] = (residues[i] - s) * c[i] % m[i]  # @line L10
    return u


def garner(residues: Sequence[int], ctx: Garner) -> int:
    """Return the unique x in [0, M) with x = residues[i] (mod m[i])."""
    u = garner_digits(residues, ctx)
    if not u:
        return 0  # M = 1, and x = 0 is the only value
    t = len(u)
    x = u[t - 1]  # @line L11
    for i in range(t - 2, -1, -1):  # @line L12
        x = x * ctx.m[i] + u[i]
    return x  # @line L13
