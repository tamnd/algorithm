# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longest-previous-factor/. The authors are listed in prov/H8NZFT.jsonl.

"""The longest previous factor (LPF) array, from the suffix array and the LCP array.

LPF[i] is the length of the longest prefix of t[i ..] that also starts at
some position j < i (the two occurrences may overlap). PrevOcc[i] is such a
j, or -1 when LPF[i] = 0.

The method is the one of Crochemore and Ilie (2008): for the suffix of rank
r, the best earlier suffix is one of its two nearest neighbours in suffix
array order with a smaller start, and one stack pass over the ranks finds
both neighbours and both common prefix lengths. The suffix array is built
by prefix doubling and the LCP array by Kasai's method, so the whole run
takes O(n log^2 n) time here; with a linear suffix array it is O(n).
"""


def suffix_array(t) -> list[int]:
    """Prefix doubling: sort the suffixes by their first 2^k symbols for k = 0, 1, ..."""
    n = len(t)
    sa = list(range(n))
    rank = list(t)
    k = 1
    while True:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rank = new
        if n == 0 or rank[sa[-1]] == n - 1:
            return sa
        k *= 2


def lcp_array(t, sa: list[int]) -> list[int]:
    """Kasai et al.: lcp[r] = lcp of the suffixes of rank r - 1 and r; lcp[0] = 0."""
    n = len(t)
    rank = [0] * n
    for r, i in enumerate(sa):
        rank[i] = r
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and t[i + h] == t[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


def lpf_array(t) -> tuple[list[int], list[int]]:
    """Return (LPF, PrevOcc) in O(n) time after the suffix and LCP arrays."""
    n = len(t)
    sa = suffix_array(t) + [-1]  # @line L1
    lcp = lcp_array(t, sa[:n]) + [0]
    lpf, prev = [0] * n, [-1] * n
    stack: list[tuple[int, int]] = []  # (rank, lcp with the rank below it)  # @line L2
    for r in range(n + 1):  # @line L3
        h = lcp[r]  # @line L4
        while stack and sa[stack[-1][0]] > sa[r]:  # @line L5
            q, left = stack.pop()  # @line L6
            i = sa[q]
            if left >= h:  # @line L7
                lpf[i] = left
                prev[i] = sa[stack[-1][0]] if left else -1
            else:
                lpf[i], prev[i] = h, sa[r]
            h = min(left, h)  # @line L8
        if r < n:
            stack.append((r, h if stack else 0))  # @line L9
    return lpf, prev  # @line L10


def lpf_brute(t) -> list[int]:
    """O(n^3) oracle: try every earlier start."""
    n = len(t)
    out = [0] * n
    for i in range(n):
        for j in range(i):
            k = 0
            while i + k < n and t[j + k] == t[i + k]:
                k += 1
            out[i] = max(out[i], k)
    return out


def lz_factorization(t) -> list[tuple[int, int]]:
    """Factors as (length, source): source -1 means a new symbol of length 1."""
    lpf, prev = lpf_array(t)
    out, i = [], 0
    while i < len(t):
        if lpf[i] == 0:
            out.append((1, -1))
            i += 1
        else:
            out.append((lpf[i], prev[i]))
            i += lpf[i]
    return out


def decode_factors(factors: list[tuple[int, int]], new_symbols) -> list:
    """Rebuild the text; new_symbols gives the symbols of the factors with source -1."""
    out, it = [], iter(new_symbols)
    for length, src in factors:
        if src < 0:
            out.append(next(it))
        else:
            for k in range(length):
                out.append(out[src + k])
    return out
