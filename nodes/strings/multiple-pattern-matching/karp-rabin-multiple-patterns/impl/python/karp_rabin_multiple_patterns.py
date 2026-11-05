# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-rabin-multiple-patterns/. The authors are listed in prov/HKXC4R.jsonl.

import random
from collections.abc import Sequence

MERSENNE_61 = (1 << 61) - 1


def codes(x: str | Sequence[int]) -> tuple[int, ...]:
    """Character codes from 1: ord(ch) + 1 for a str, value + 1 for a sequence of non-negative ints."""
    if isinstance(x, str):
        return tuple(ord(ch) + 1 for ch in x)
    return tuple(v + 1 for v in x)


def poly_hash(x: Sequence[int], r: int, p: int) -> int:
    """Horner's rule: sum of x[i] * r^(len(x) - 1 - i) modulo p."""
    v = 0
    for c in x:
        v = (v * r + c) % p
    return v


def karp_rabin_set(
    text: str | Sequence[int],
    patterns: Sequence[str | Sequence[int]],
    *,
    p: int = MERSENNE_61,
    base: int | None = None,
    verify: bool = True,
    stats: dict[str, int] | None = None,
) -> list[tuple[int, int]]:
    """Return all pairs (s, j) such that patterns[j] occurs in text at the 0-based position s.

    Occurrences may overlap, a pattern listed twice is reported once for each index, and
    an empty pattern occurs at every s in 0..len(text). The list is sorted. p must be a prime
    larger than every character code. With verify=False, every hash match is reported (a
    Monte Carlo answer that may contain false pairs). If stats is a dict, the numbers of
    verifications and of failed verifications are stored in it.
    """
    t = codes(text)
    n = len(t)
    if any(v >= p for v in t):
        raise ValueError("every character code must be below p")
    by_length: dict[int, dict[tuple[int, ...], list[int]]] = {}
    for j, pat in enumerate(patterns):
        q = codes(pat)
        if any(v >= p for v in q):
            raise ValueError("every character code must be below p")
        by_length.setdefault(len(q), {}).setdefault(q, []).append(j)
    checks = failed = 0
    out: list[tuple[int, int]] = []
    r = random.randrange(p) if base is None else base % p  # @line L1
    for ell, group in by_length.items():  # @line L2
        table: dict[int, list[tuple[tuple[int, ...], list[int]]]] = {}  # @line L3
        for q, idx in group.items():  # @line L4
            table.setdefault(poly_hash(q, r, p), []).append((q, idx))
        if ell == 0:  # @line L5
            out.extend((s, j) for s in range(n + 1) for j in group[()])
            continue
        if ell > n:  # @line L6
            continue
        big_r = pow(r, ell - 1, p)  # @line L7
        ht = poly_hash(t[:ell], r, p)
        for s in range(n - ell + 1):  # @line L8
            for q, idx in table.get(ht, ()):  # @line L9
                checks += 1
                if not verify or t[s : s + ell] == q:  # @line L10
                    out.extend((s, j) for j in idx)
                else:
                    failed += 1
            if s < n - ell:  # @line L11
                ht = ((ht - t[s] * big_r) * r + t[s + ell]) % p
    if stats is not None:
        stats["checks"] = checks
        stats["failed"] = failed
    out.sort()
    return out
