# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fischer-paterson-algorithm/. The authors are listed in prov/PNQWEP.jsonl.

"""Hamming distances at all alignments by one convolution per symbol.

Edit model: Hamming distance (substitutions only). Indices are 0-based.
The result h has one entry per start position i in 0..len(text)-len(pattern):
h[i] is the number of q with pattern[q] != text[i + q]. An empty pattern
gives len(text) + 1 zeros, and a pattern longer than the text gives [].

The convolutions use a number-theoretic transform modulo the prime
998244353, which is exact because every count is at most len(pattern).
"""

MOD = 998244353
ROOT = 3  # a primitive root modulo MOD


def ntt(a: list[int], invert: bool) -> None:
    """Transform a in place; len(a) is a power of two that divides 2**23."""
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        w = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            w = pow(w, MOD - 2, MOD)
        half = length >> 1
        for start in range(0, n, length):
            wn = 1
            for k in range(start, start + half):
                u = a[k]
                v = a[k + half] * wn % MOD
                a[k] = (u + v) % MOD
                a[k + half] = (u - v) % MOD
                wn = wn * w % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def hamming_distances(pattern: str, text: str) -> list[int]:
    """Return h[0..n-m], the Hamming distance of pattern to each window.

    Cost: O(s * n * log m) time for s distinct pattern symbols and
    O(n + m) extra space, with text blocks of length 2m - 1.
    """
    m, n = len(pattern), len(text)
    if m == 0:
        return [0] * (n + 1)
    if m > n:
        return []
    agree = [0] * (n - m + 1)  # @line L1
    size = 1
    while size < 3 * m - 2:
        size <<= 1
    for c in sorted(set(pattern)):  # @line L2
        x = [0] * size
        for q in range(m):  # @line L3
            if pattern[m - 1 - q] == c:
                x[q] = 1
        ntt(x, False)
        for b in range(0, n - m + 1, m):  # @line L4
            seg = text[b:b + 2 * m - 1]
            y = [0] * size
            for j, t in enumerate(seg):  # @line L5
                if t == c:
                    y[j] = 1
            ntt(y, False)
            z = [u * v % MOD for u, v in zip(x, y)]  # @line L6
            ntt(z, True)
            for t in range(min(m, n - m + 1 - b)):  # @line L7
                agree[b + t] += z[t + m - 1]
    return [m - a for a in agree]  # @line L8


def k_mismatch_starts(pattern: str, text: str, k: int) -> list[int]:
    """Return the start positions with at most k mismatches (k >= 0)."""
    if k < 0:
        raise ValueError("k must be at least 0")
    return [i for i, d in enumerate(hamming_distances(pattern, text)) if d <= k]
