# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/positional-burrows-wheeler-transform/. The authors are listed in prov/39NYBT.jsonl.
"""The positional Burrows-Wheeler transform (PBWT) of Durbin (2014).

X is a list of M binary haplotypes, each of length N. For k = 0..N:

  a_k  is the permutation of 0..M-1 that sorts the haplotypes by their
       reversed prefixes x[0..k-1] (read from site k-1 back to site 0),
       with ties broken by index.
  d_k  is the divergence array: d_k[i] is the smallest s such that the
       haplotypes a_k[i] and a_k[i-1] agree on sites s..k-1. d_k[0] = k.

a_{k+1} and d_{k+1} come from a_k, d_k and column k in one stable pass
(Durbin's Algorithm 2), so the whole transform costs O(NM). From the
arrays one can list all long matches (Algorithm 3) and all set-maximal
matches (Algorithm 4).

A match between haplotypes i and j is an interval [s, e) of sites on
which they agree. It is maximal if it cannot be extended to the left or to
the right. For haplotype i, a maximal match [s, e) to j is set-maximal if
no other match of i to any haplotype covers [s, e) and is longer.
"""

from __future__ import annotations

from typing import Sequence


def check_haplotypes(x: Sequence[Sequence[int]]) -> tuple[int, int]:
    m = len(x)
    if m == 0:
        raise ValueError("need at least one haplotype")
    n = len(x[0])
    for h in x:
        if len(h) != n or any(v not in (0, 1) for v in h):
            raise ValueError("haplotypes must be 0/1 rows of equal length")
    return m, n


def step(a: list[int], d: list[int], column: Sequence[int], k: int) -> tuple[list[int], list[int]]:
    """Durbin's Algorithm 2: from (a_k, d_k) and column k, compute (a_{k+1}, d_{k+1})."""
    a0, d0, a1, d1 = [], [], [], []
    p = q = k + 1  # @line L3
    for idx, div in zip(a, d):  # @line L4
        if div > p:  # @line L5
            p = div
        if div > q:
            q = div
        if column[idx] == 0:  # @line L6
            a0.append(idx)
            d0.append(p)
            p = 0
        else:  # @line L7
            a1.append(idx)
            d1.append(q)
            q = 0
    return a0 + a1, d0 + d1  # @line L8


def build(x: Sequence[Sequence[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """All arrays a_0..a_N and d_0..d_N. Keeping them all costs O(NM) space;
    a streaming use keeps only the current pair, in O(M) space."""
    m, n = check_haplotypes(x)
    a = list(range(m))  # @line L1
    d = [0] * m
    arrays_a, arrays_d = [a], [d]
    for k in range(n):  # @line L2
        column = [h[k] for h in x]
        a, d = step(a, d, column, k)
        arrays_a.append(a)
        arrays_d.append(d)
    return arrays_a, arrays_d  # @line L9


def _start(d: list[int], lo: int, hi: int) -> int:
    """Start of the match between positions lo < hi of the sort order: max of d[lo+1..hi]."""
    return max(d[lo + 1:hi + 1])


def long_matches(x: Sequence[Sequence[int]], length: int) -> set[tuple[int, int, int, int]]:
    """All maximal matches of at least `length` sites, as (i, j, s, e) with i < j (Algorithm 3)."""
    if length < 1:
        raise ValueError("length must be at least 1")
    m, n = check_haplotypes(x)
    arrays_a, arrays_d = build(x)
    out = set()
    for k in range(n + 1):
        a, d = arrays_a[k], arrays_d[k]
        block: list[int] = []  # positions in the sort order

        def flush():
            for u in range(len(block)):
                for v in range(u + 1, len(block)):
                    pu, pv = block[u], block[v]
                    i, j = a[pu], a[pv]
                    if k < n and x[i][k] == x[j][k]:
                        continue  # the match goes on past k
                    s = _start(d, pu, pv)
                    if k - s >= length:
                        out.add((min(i, j), max(i, j), s, k))

        for pos in range(m):
            if d[pos] > k - length:
                flush()
                block = []
            block.append(pos)
        flush()
    return out


def set_maximal_matches(x: Sequence[Sequence[int]]) -> set[tuple[int, int, int, int]]:
    """All set-maximal matches, as (i, j, s, e): a match of haplotype i to j on [s, e) (Algorithm 4)."""
    m, n = check_haplotypes(x)
    arrays_a, arrays_d = build(x)
    out = set()
    for k in range(n + 1):
        a = arrays_a[k]
        d = arrays_d[k] + [k + 1]  # sentinel below the last row; d[0] = k already blocks the top
        d[0] = k + 1

        def same(i: int, j: int) -> bool:
            return k < n and x[i][k] == x[j][k]

        for pos in range(m):
            top, bottom = pos - 1, pos + 1
            s = min(d[pos], d[pos + 1])  # start of the longest match ending at k
            if s >= k:
                continue  # no match of positive length ends here
            extends = False
            if d[pos] <= d[pos + 1]:
                while d[top + 1] <= d[pos]:
                    if same(a[top], a[pos]):
                        extends = True
                        break
                    top -= 1
            if not extends and d[pos] >= d[pos + 1]:
                while d[bottom] <= d[pos + 1]:
                    if same(a[bottom], a[pos]):
                        extends = True
                        break
                    bottom += 1
            if extends:
                continue
            i = a[pos]
            for t in range(top + 1, pos):
                out.add((i, a[t], d[pos], k))
            for t in range(pos + 1, bottom):
                out.add((i, a[t], d[pos + 1], k))
    return out


# Reference versions by brute force, for the tests.

def naive_sort(x: Sequence[Sequence[int]], k: int) -> list[int]:
    return sorted(range(len(x)), key=lambda i: (list(reversed(x[i][:k])), i))


def naive_divergence(x: Sequence[Sequence[int]], order: list[int], k: int) -> list[int]:
    out = [k]
    for pos in range(1, len(order)):
        i, j = order[pos], order[pos - 1]
        s = k
        while s > 0 and x[i][s - 1] == x[j][s - 1]:
            s -= 1
        out.append(s)
    return out


def naive_maximal_matches(x: Sequence[Sequence[int]]) -> set[tuple[int, int, int, int]]:
    """All maximal matches of positive length, as (i, j, s, e) with i != j (both orders)."""
    m, n = check_haplotypes(x)
    out = set()
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            s = 0
            while s < n:
                if x[i][s] != x[j][s]:
                    s += 1
                    continue
                e = s
                while e < n and x[i][e] == x[j][e]:
                    e += 1
                out.add((i, j, s, e))
                s = e
    return out


def naive_set_maximal(x: Sequence[Sequence[int]]) -> set[tuple[int, int, int, int]]:
    matches = naive_maximal_matches(x)
    by_i: dict[int, list[tuple[int, int, int]]] = {}
    for i, j, s, e in matches:
        by_i.setdefault(i, []).append((j, s, e))
    out = set()
    for i, lst in by_i.items():
        for j, s, e in lst:
            covered = any(s2 <= s and e <= e2 and e2 - s2 > e - s for _, s2, e2 in lst)
            if not covered:
                out.add((i, j, s, e))
    return out
