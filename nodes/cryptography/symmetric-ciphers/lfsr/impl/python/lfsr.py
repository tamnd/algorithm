# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfsr/. The authors are listed in prov/5N3GKG.jsonl.

"""Linear feedback shift registers over GF(2), Berlekamp-Massey, and the Geffe
generator with Siegenthaler's correlation attack, for study only.

An LFSR is not a cipher. This code is not constant time and must not protect
real data. Use a vetted cipher from libsodium or a FIPS 140 validated module.

Conventions. A connection polynomial C(x) = 1 + c1 x + ... + cL x^L is the list
[1, c1, ..., cL]. A sequence s satisfies it when, for each t >= L,
s[t] = c1 s[t-1] + ... + cL s[t-L] (mod 2).
"""


def fibonacci_lfsr(c: list[int], state: list[int], n: int) -> list[int]:
    """Return n output bits of the Fibonacci LFSR with connection polynomial c.

    state[0] is the next output bit, state[L-1] the newest bit.
    Precondition: len(c) == len(state) + 1, c[0] == 1, bits are 0 or 1.
    Cost: Theta(n L) bit operations.
    """
    big_l = len(state)
    s = list(state)
    out = []
    for _ in range(n):
        out.append(s[0])  # @line L1
        new = 0
        for i in range(1, big_l + 1):  # @line L2
            new ^= c[i] & s[big_l - i]
        s = s[1:] + [new]  # @line L3
    return out  # @line L4


def galois_lfsr(c: list[int], state: int, n: int) -> list[int]:
    """Return n output bits of the Galois LFSR for the same polynomial.

    The state is a polynomial a(x) of degree < L, bit i = coefficient of x^i,
    in GF(2)[x] / f(x), where f(x) = x^L C(1/x) = x^L + c1 x^(L-1) + ... + cL.
    Each step outputs the coefficient of x^(L-1), then sets a <- x a mod f.
    Precondition: c[0] == 1 and 0 <= state < 2**L. Cost: Theta(n) word operations.
    """
    big_l = len(c) - 1
    low = 0  # f(x) - x^L, as a bit mask
    for i in range(1, big_l + 1):
        if c[i]:
            low |= 1 << (big_l - i)
    mask = (1 << big_l) - 1
    a = state
    out = []
    for _ in range(n):
        top = (a >> (big_l - 1)) & 1  # @line L5
        out.append(top)
        a = (a << 1) & mask  # @line L6
        if top:
            a ^= low  # @line L7
    return out  # @line L8


def berlekamp_massey(s: list[int]) -> tuple[int, list[int]]:
    """Return (L, C): the linear complexity of s and a shortest connection polynomial.

    Precondition: s is a list of bits. Cost: Theta(N^2) bit operations for N = len(s).
    """
    c, b = [1], [1]  # @line L9
    big_l, m = 0, 1
    for n in range(len(s)):  # @line L10
        c += [0] * (big_l + 1 - len(c))
        d = s[n]  # @line L11
        for i in range(1, big_l + 1):
            d ^= c[i] & s[n - i]
        if d == 0:  # @line L12
            m += 1
            continue
        t = list(c)
        c += [0] * (len(b) + m - len(c))
        for i, bit in enumerate(b):  # C <- C + x^m B
            c[i + m] ^= bit
        if 2 * big_l <= n:  # @line L13
            big_l, b, m = n + 1 - big_l, t, 1
        else:  # @line L14
            m += 1
    c = (c + [0] * (big_l + 1))[: big_l + 1]
    return big_l, c  # @line L15


def period(c: list[int], state: list[int]) -> int:
    """Return the period of the Fibonacci LFSR state sequence from a nonzero state.

    Precondition: c[L] == 1 (so the step is invertible) and state is not all zero.
    Cost: Theta(T L) for the period T.
    """
    big_l = len(state)
    start = tuple(state)
    s = list(state)
    t = 0
    while True:
        new = 0
        for i in range(1, big_l + 1):
            new ^= c[i] & s[big_l - i]
        s = s[1:] + [new]
        t += 1
        if tuple(s) == start:
            return t


def geffe(x1: list[int], x2: list[int], x3: list[int]) -> list[int]:
    """Return the Geffe combiner output z = x1 x2 XOR (not x1) x3, bit by bit."""
    return [(a & b) ^ ((1 ^ a) & d) for a, b, d in zip(x1, x2, x3)]


def correlation_attack(c: list[int], z: list[int]) -> list[int]:
    """Return the initial state of the LFSR with polynomial c that agrees best with z.

    Siegenthaler's divide and conquer step: try each of the 2^L - 1 nonzero
    states, and keep the one whose output agrees with z most often.
    Cost: Theta(2^L N L) for N = len(z).
    """
    big_l = len(c) - 1
    best, best_score = [], -1
    for v in range(1, 1 << big_l):
        st = [(v >> i) & 1 for i in range(big_l)]
        out = fibonacci_lfsr(c, st, len(z))
        score = sum(1 for p, q in zip(out, z) if p == q)
        if score > best_score:
            best, best_score = st, score
    return best
