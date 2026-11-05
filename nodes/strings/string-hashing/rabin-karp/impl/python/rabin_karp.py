# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-karp/. The authors are listed in prov/1B6QTQ.jsonl.

import random
from collections.abc import Sequence

MERSENNE_61 = (1 << 61) - 1


def codes(x: str | Sequence[int]) -> list[int]:
    """Character codes from 1: ord(ch) + 1 for a str, value + 1 for a sequence of non-negative ints."""
    if isinstance(x, str):
        return [ord(ch) + 1 for ch in x]
    return [v + 1 for v in x]


def rabin_karp(
    text: str | Sequence[int],
    pattern: str | Sequence[int],
    *,
    p: int = MERSENNE_61,
    base: int | None = None,
    verify: bool = True,
    stats: dict[str, int] | None = None,
) -> list[int]:
    """Return the 0-based start positions of all (possibly overlapping) occurrences of pattern in text.

    p must be a prime larger than every character code. The base is drawn uniformly
    from {0, ..., p - 1} unless it is given. With verify=False the result is the list of
    hash hits (a Monte Carlo answer that may contain false matches). If stats is a dict,
    the numbers of hash hits and of spurious hits are stored in it.
    """
    t, q = codes(text), codes(pattern)
    n, m = len(t), len(q)
    if any(v >= p for v in t) or any(v >= p for v in q):
        raise ValueError("every character code must be below p")
    hits = spurious = 0
    out: list[int] = []
    if m == 0:  # @line L1
        out = list(range(n + 1))
    elif m <= n:  # @line L2
        r = random.randrange(p) if base is None else base % p  # @line L3
        big_r = pow(r, m - 1, p)  # @line L4
        hp = ht = 0  # @line L5
        for i in range(m):  # @line L6
            hp = (hp * r + q[i]) % p
            ht = (ht * r + t[i]) % p
        for s in range(n - m + 1):  # @line L7
            if hp == ht:  # @line L8
                hits += 1
                if not verify:
                    out.append(s)
                elif t[s : s + m] == q:  # @line L9
                    out.append(s)
                else:
                    spurious += 1
            if s < n - m:  # @line L10
                ht = ((ht - t[s] * big_r) * r + t[s + m]) % p  # @line L11
    if stats is not None:
        stats["hits"] = hits
        stats["spurious"] = spurious
    return out
