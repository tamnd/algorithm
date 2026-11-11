# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-prefix-code/. The authors are listed in prov/8V9YWA.jsonl.

"""The optimal prefix code problem, solved by brute force and by Huffman's
algorithm, and the minimax variant of Golumbic (1976).

A code is given by its list of codeword lengths. By the Kraft inequality,
a prefix code with lengths l_1, ..., l_n exists if and only if
sum 2^(-l_i) <= 1, so the problem is to choose such lengths and minimize
sum w_i l_i.
"""

import heapq
from fractions import Fraction
from itertools import combinations_with_replacement
from typing import Sequence


def kraft_sum(lengths: Sequence[int]) -> Fraction:
    return sum((Fraction(1, 2**l) for l in lengths), Fraction(0))


def cost(weights: Sequence[float], lengths: Sequence[int]) -> float:
    return sum(w * l for w, l in zip(weights, lengths))


def brute_force_lengths(weights: Sequence[float]) -> list[int]:
    """Try all length lists that satisfy the Kraft inequality.

    In an optimal code a heavier symbol never has a longer codeword, so it
    is enough to try non-decreasing length lists, given to the symbols in
    order of non-increasing weight. A length above n - 1 is never needed.
    The work grows fast with n; use it for n <= 9 or so.
    """
    n = len(weights)
    if n == 1:
        return [0]
    order = sorted(range(n), key=lambda i: -weights[i])
    best, best_cost = None, None
    for ls in combinations_with_replacement(range(1, n), n):
        if kraft_sum(ls) > 1:
            continue
        c = sum(weights[order[k]] * ls[k] for k in range(n))
        if best_cost is None or c < best_cost:
            best, best_cost = ls, c
    lengths = [0] * n
    for k, i in enumerate(order):
        lengths[i] = best[k]
    return lengths


def huffman_lengths(weights: Sequence[float]) -> list[int]:
    """Code lengths of a Huffman code, by the heap method."""
    n = len(weights)
    if n == 1:
        return [0]
    heap = [(w, i, [i]) for i, w in enumerate(weights)]
    heapq.heapify(heap)
    lengths = [0] * n
    age = n
    while len(heap) > 1:
        w1, _, a = heapq.heappop(heap)
        w2, _, b = heapq.heappop(heap)
        for s in a + b:
            lengths[s] += 1
        heapq.heappush(heap, (w1 + w2, age, a + b))
        age += 1
    return lengths


def minimax_lengths(weights: Sequence[int]) -> list[int]:
    """Minimize max_i (w_i + l_i) over prefix codes (Golumbic 1976).

    The greedy method merges the two smallest items into one item of
    value max(a, b) + 1, which is Huffman's method with max in place of
    the sum.
    """
    n = len(weights)
    if n == 1:
        return [0]
    heap = [(w, i, [i]) for i, w in enumerate(weights)]
    heapq.heapify(heap)
    lengths = [0] * n
    age = n
    while len(heap) > 1:
        w1, _, a = heapq.heappop(heap)
        w2, _, b = heapq.heappop(heap)
        for s in a + b:
            lengths[s] += 1
        heapq.heappush(heap, (max(w1, w2) + 1, age, a + b))
        age += 1
    return lengths


def brute_force_minimax(weights: Sequence[int]) -> int:
    """The smallest value of max_i (w_i + l_i), by trying all length lists."""
    n = len(weights)
    if n == 1:
        return weights[0]
    order = sorted(range(n), key=lambda i: -weights[i])
    best = None
    for ls in combinations_with_replacement(range(1, n), n):
        if kraft_sum(ls) > 1:
            continue
        v = max(weights[order[k]] + ls[k] for k in range(n))
        best = v if best is None else min(best, v)
    return best
