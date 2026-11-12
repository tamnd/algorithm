# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-shortest-common-superstring/. The authors are listed in prov/D91MJT.jsonl.

from typing import List, Optional, Sequence

_SEP = object()


def _prefix_function(t: Sequence[object]) -> List[int]:
    pi = [0] * len(t)
    for q in range(1, len(t)):
        k = pi[q - 1]
        while k > 0 and t[q] != t[k]:
            k = pi[k - 1]
        if t[q] == t[k]:
            k += 1
        pi[q] = k
    return pi


def overlap(a: str, b: str) -> int:
    """Length of the longest proper suffix of a that is a proper prefix of b.

    Precondition: none. Cost: O(|a| + |b|) time with the prefix function of b, a separator, then a.
    """
    if not a or not b:
        return 0
    t: List[object] = list(b)
    t.append(_SEP)
    t.extend(a)
    pi = _prefix_function(t)
    k = pi[-1]
    limit = min(len(a), len(b))
    while k >= limit:
        k = pi[k - 1]
    return k


def occurs(p: str, t: str) -> bool:
    """True when p is a contiguous substring of t. Cost: O(|p| + |t|) time."""
    if not p:
        return True
    u: List[object] = list(p)
    u.append(_SEP)
    u.extend(t)
    return any(v == len(p) for v in _prefix_function(u))


def reduce_reads(reads: Sequence[str]) -> List[str]:
    """Drop empty reads, repeated reads (keep the first copy) and reads inside other reads.

    The kept reads stay in input order. Cost: O(m * n) time for m reads of total length n.
    """
    distinct: List[str] = []
    seen = set()
    for r in reads:
        if r and r not in seen:
            seen.add(r)
            distinct.append(r)
    kept: List[str] = []
    for i, r in enumerate(distinct):
        if not any(j != i and len(t) > len(r) and occurs(r, t) for j, t in enumerate(distinct)):
            kept.append(r)
    return kept


def greedy_assemble(reads: Sequence[str], tau: int = 0) -> List[str]:
    """Greedy merging of reads by largest overlap while that overlap is at least tau.

    Returns the contigs, ordered by the input position of their first read. With tau = 0
    and at least one nonempty read, the result is one common superstring of all reads.
    Ties go to the pair with the smaller first read, then the smaller second read, in the
    order of the reduced list. Cost: O(m * n + m^2 log m) time and O(n + m^2) space.
    """
    # @line L1
    s = reduce_reads(reads)
    m = len(s)
    # @line L2
    pairs = [(overlap(s[i], s[j]), i, j) for i in range(m) for j in range(m) if i != j]
    pairs.sort(key=lambda e: (-e[0], e[1], e[2]))
    nxt: List[Optional[int]] = [None] * m
    prv: List[Optional[int]] = [None] * m
    weight = [0] * m
    head_of = list(range(m))  # head_of[t]: head of the contig whose last read is t
    tail_of = list(range(m))  # tail_of[h]: last read of the contig whose first read is h
    merges = 0
    # @line L3
    for w, i, j in pairs:
        if merges == m - 1:
            break
        # @line L4
        if nxt[i] is not None or prv[j] is not None or head_of[i] == j:
            continue
        # @line L5
        if w < tau:
            break
        # @line L6
        nxt[i] = j
        prv[j] = i
        weight[i] = w
        merges += 1
        # @line L7
        h, t = head_of[i], tail_of[j]
        head_of[t] = h
        tail_of[h] = t
    contigs: List[str] = []
    # @line L8
    for h in range(m):
        if prv[h] is not None:
            continue
        parts = [s[h]]
        cur = h
        while nxt[cur] is not None:
            j = nxt[cur]
            assert j is not None
            parts.append(s[j][weight[cur]:])
            cur = j
        contigs.append("".join(parts))
    return contigs


def greedy_superstring(reads: Sequence[str]) -> str:
    """One common superstring of the reads by greedy merging; the empty string for no reads.

    Cost: the cost of greedy_assemble with tau = 0.
    """
    contigs = greedy_assemble(reads, 0)
    return contigs[0] if contigs else ""
