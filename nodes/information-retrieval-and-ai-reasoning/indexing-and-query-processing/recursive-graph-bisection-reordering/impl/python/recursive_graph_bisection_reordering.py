# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-graph-bisection-reordering/. The authors are listed in prov/7XKMDW.jsonl.

import math
from collections.abc import Hashable, Iterable, Sequence


def move_cost(a: int, b: int, n_a: int, n_b: int) -> float:
    """The estimated log-gap bits of one term with a documents in a side of n_a and b in a side of n_b."""
    cost = 0.0
    if a:
        cost += a * math.log2(n_a / (a + 1))
    if b:
        cost += b * math.log2(n_b / (b + 1))
    return cost


def bisect_order(
    docs: Sequence[Iterable[Hashable]],
    iters: int = 20,
    leaf_size: int = 1,
    max_depth: int | None = None,
) -> list[int]:
    """Order documents 0..n-1 by recursive graph bisection. Returns order, with order[p] the document at position p.

    docs[d] holds the terms of document d. This is a heuristic: the result has
    no approximation guarantee, and it can be worse than the input order.
    """
    terms = [frozenset(t) for t in docs]
    if leaf_size < 1 or iters < 0:
        raise ValueError("leaf_size must be at least 1 and iters at least 0")
    limit = max_depth if max_depth is not None else math.inf
    return _bp(list(range(len(terms))), terms, 0, iters, leaf_size, limit)


def _bp(d: list[int], terms: list[frozenset], depth: int, iters: int, leaf: int, limit: float) -> list[int]:
    if len(d) <= leaf or depth >= limit:  # @line L1
        return d
    half = (len(d) + 1) // 2
    a, b = d[:half], d[half:]  # @line L2
    n_a, n_b = len(a), len(b)
    for _ in range(iters):  # @line L3
        deg_a: dict = {}
        deg_b: dict = {}
        for v in a:  # @line L4
            for t in terms[v]:
                deg_a[t] = deg_a.get(t, 0) + 1
        for v in b:
            for t in terms[v]:
                deg_b[t] = deg_b.get(t, 0) + 1

        def gain(v: int, to_b: bool) -> float:
            parts = []
            for t in terms[v]:
                x, y = deg_a.get(t, 0), deg_b.get(t, 0)
                nx, ny = (x - 1, y + 1) if to_b else (x + 1, y - 1)
                parts.append(move_cost(x, y, n_a, n_b) - move_cost(nx, ny, n_a, n_b))
            # fsum is exact up to one rounding, so the gain does not depend on the order of the set
            return math.fsum(parts)

        ga = {v: gain(v, True) for v in a}  # @line L5
        gb = {v: gain(v, False) for v in b}  # @line L6
        a.sort(key=lambda v: (-ga[v], v))  # @line L7
        b.sort(key=lambda v: (-gb[v], v))
        k = 0  # @line L8
        while k < min(n_a, n_b) and ga[a[k]] + gb[b[k]] > 1e-12:
            k += 1
        if k == 0:  # @line L9
            break
        a[:k], b[:k] = b[:k], a[:k]  # @line L10
    return _bp(a, terms, depth + 1, iters, leaf, limit) + _bp(b, terms, depth + 1, iters, leaf, limit)  # @line L11


def log_gap_cost(docs: Sequence[Iterable[Hashable]], order: Sequence[int]) -> int:
    """Bits of the gaps of all posting lists when document order[p] gets id p + 1.

    Each gap g, the first id included, costs its binary length floor(log2 g) + 1.
    """
    new_id = {d: p + 1 for p, d in enumerate(order)}
    postings: dict = {}
    for d in sorted(new_id, key=new_id.get):
        for t in set(docs[d]):
            postings.setdefault(t, []).append(new_id[d])
    total = 0
    for ids in postings.values():
        prev = 0
        for i in ids:
            total += (i - prev).bit_length()
            prev = i
    return total
