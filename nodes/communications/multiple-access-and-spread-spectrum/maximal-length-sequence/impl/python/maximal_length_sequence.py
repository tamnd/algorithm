# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-length-sequence/. The authors are listed in prov/09SJJW.jsonl.

"""Maximal-length sequences (m-sequences) from a binary linear recurrence.

A polynomial f(x) = x^n + ... + 1 over GF(2) is given by the list of its
exponents, for example [3, 1, 0] for x^3 + x + 1. The sequence satisfies
the recurrence sum over i of f_i s[k + i] = 0 (mod 2), that is

    s[k + n] = XOR over the exponents i < n of s[k + i].

If f is primitive, every nonzero start state gives a sequence of period
2^n - 1, which is an m-sequence. All arithmetic is on Python integers.
"""


def lfsr_bits(exps: list[int], state: list[int], count: int) -> list[int]:
    """The first count terms s[0], s[1], ... of the recurrence of f, from s[0..n-1] = state."""
    n = max(exps)
    if len(state) != n or 0 not in exps:
        raise ValueError("need n start bits and a polynomial with constant term 1")
    taps = [i for i in exps if i < n]
    s = [b & 1 for b in state]  # @line L1
    while len(s) < count:
        k = len(s) - n
        bit = 0
        for i in taps:  # @line L2
            bit ^= s[k + i]
        s.append(bit)  # @line L3
    return s[:count]


def mseq(exps: list[int], state: list[int] | None = None) -> list[int]:
    """One period (2^n - 1 terms) of the sequence of f, from the start state 1, 0, ..., 0 by default."""
    n = max(exps)
    if state is None:
        state = [1] + [0] * (n - 1)
    return lfsr_bits(exps, state, (1 << n) - 1)


def period(exps: list[int], state: list[int] | None = None) -> int:
    """The least period of the recurrence of f from a start state, found by running the state machine."""
    n = max(exps)
    if state is None:
        state = [1] + [0] * (n - 1)
    taps = [i for i in exps if i < n]
    start = tuple(state)
    cur = list(state)
    for p in range(1, 1 << n):
        bit = 0
        for i in taps:
            bit ^= cur[i]
        cur = cur[1:] + [bit]
        if tuple(cur) == start:
            return p
    return 0


def is_primitive(exps: list[int]) -> bool:
    """True if the recurrence of f has period 2^n - 1 from the state 1, 0, ..., 0 (f has constant term 1)."""
    n = max(exps)
    return 0 in exps and period(exps) == (1 << n) - 1


def to_pm(bits: list[int]) -> list[int]:
    """Map 0 to +1 and 1 to -1."""
    return [1 - 2 * b for b in bits]  # @line L4


def periodic_xcorr(a: list[int], b: list[int], shift: int) -> int:
    """sum over k of a[k] b[(k + shift) mod N], for two +1/-1 sequences of length N."""
    n = len(a)
    if len(b) != n:
        raise ValueError("lengths differ")
    return sum(a[k] * b[(k + shift) % n] for k in range(n))  # @line L5


def autocorrelation(a: list[int]) -> list[int]:
    """The periodic autocorrelation of a +1/-1 sequence at every shift 0, ..., N-1."""
    return [periodic_xcorr(a, a, t) for t in range(len(a))]


def runs(bits: list[int]) -> dict[tuple[int, int], int]:
    """Counts of the runs in one period, read cyclically: (bit, length) -> count."""
    n = len(bits)
    if n == 0 or all(b == bits[0] for b in bits):
        return {(bits[0], n): 1} if bits else {}
    start = next(i for i in range(n) if bits[i] != bits[i - 1])
    out: dict[tuple[int, int], int] = {}
    i = 0
    while i < n:
        b = bits[(start + i) % n]
        j = i
        while j < n and bits[(start + j) % n] == b:
            j += 1
        out[(b, j - i)] = out.get((b, j - i), 0) + 1
        i = j
    return out
