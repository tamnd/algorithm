# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peeling-decoding/. The authors are listed in prov/W86NJM.jsonl.
"""The peeling decoder for sparse XOR systems: repeatedly solve a check with one unknown.

A check c is a set C[c] of unknown variables and a value val[c], the XOR of those unknowns.
Values are Python ints, so a value can be one bit or a whole packet seen as a big integer.
The decoder runs in time linear in the number of edges (variable, check). It stops when the
unknowns left form a stopping set: a set in which each check that touches it touches it at
least twice.
"""

from typing import Dict, List, Optional, Sequence, Set, Tuple


def peel(n: int, checks: Sequence[Sequence[int]], values: Sequence[int]) -> List[Optional[int]]:
    """Variables 0..n-1. Returns x with x[v] = None for each variable left unresolved."""
    cs: List[Set[int]] = [set(c) for c in checks]
    val = list(values)
    adj: List[List[int]] = [[] for _ in range(n)]
    for c, vs in enumerate(cs):
        for v in vs:
            adj[v].append(c)
    x: List[Optional[int]] = [None] * n  # @line L1
    queue = [c for c in range(len(cs)) if len(cs[c]) == 1]  # @line L2
    while queue:  # @line L3
        c = queue.pop()  # @line L4
        if len(cs[c]) != 1:  # @line L5
            continue
        v = next(iter(cs[c]))  # @line L6
        x[v] = val[c]  # @line L7
        for c2 in adj[v]:  # @line L8
            cs[c2].discard(v)  # @line L9
            val[c2] ^= x[v]
            if len(cs[c2]) == 1:  # @line L10
                queue.append(c2)
    return x  # @line L11


def checks_from_parity_check(h: Sequence[Sequence[int]], y: Sequence[Optional[int]]
                             ) -> Tuple[List[List[int]], List[int]]:
    """Turn H c^T = 0 over GF(2) and a word y with erasures (None) into peeling checks.

    The unknowns are the erased positions, with their own indices; known symbols move to
    the value side."""
    checks, values = [], []
    for row in h:
        unknown = [j for j, b in enumerate(row) if b and y[j] is None]
        v = 0
        for j, b in enumerate(row):
            if b and y[j] is not None:
                v ^= y[j]
        checks.append(unknown)
        values.append(v)
    return checks, values


def peel_word(h: Sequence[Sequence[int]], y: Sequence[Optional[int]]) -> List[Optional[int]]:
    """Fill the erasures of y that peeling can reach; others stay None."""
    checks, values = checks_from_parity_check(h, y)
    x = peel(len(y), checks, values)
    return [y[j] if y[j] is not None else x[j] for j in range(len(y))]


def is_stopping_set(h: Sequence[Sequence[int]], s: Set[int]) -> bool:
    """Each row of H that meets s meets it at least twice."""
    return all(sum(1 for j in s if row[j]) != 1 for row in h)


def max_stopping_set(h: Sequence[Sequence[int]], erased: Set[int]) -> Set[int]:
    """The largest stopping set inside `erased`, by brute force over all subsets."""
    items = sorted(erased)
    best: Set[int] = set()
    for mask in range(1 << len(items)):
        s = {items[i] for i in range(len(items)) if mask >> i & 1}
        if is_stopping_set(h, s):
            best |= s  # a union of stopping sets is a stopping set
    return best


def bp_bec(h: Sequence[Sequence[int]], y: Sequence[Optional[int]], rounds: int = 100
           ) -> List[Optional[int]]:
    """Belief propagation on the BEC with flooding messages: a message is a bit or None."""
    n = len(y)
    edges = [(i, j) for i, row in enumerate(h) for j in range(n) if row[j]]
    v2c: Dict[Tuple[int, int], Optional[int]] = {e: y[e[1]] for e in edges}
    c2v: Dict[Tuple[int, int], Optional[int]] = {e: None for e in edges}
    for _ in range(rounds):
        for i, j in edges:
            others = [v2c[(i, k)] for k in range(n) if h[i][k] and k != j]
            c2v[(i, j)] = None if any(m is None for m in others) else sum(others) % 2
        for i, j in edges:
            if y[j] is not None:
                continue
            known = [c2v[(k, j)] for k in range(len(h)) if h[k][j] and k != i]
            known = [m for m in known if m is not None]
            v2c[(i, j)] = known[0] if known else None
    out = list(y)
    for j in range(n):
        if out[j] is None:
            got = [c2v[(i, j)] for i in range(len(h)) if h[i][j] and c2v[(i, j)] is not None]
            out[j] = got[0] if got else None
    return out
