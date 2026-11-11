# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/length-limited-prefix-code/. The authors are listed in prov/D5F6KM.jsonl.

"""The length-limited prefix code problem: an exact dynamic program, a
brute force check, and the heuristic of the JPEG standard.

All functions return a list of code lengths, one for each weight. The
limit L must satisfy 2^L >= n, or no code exists.
"""

import heapq
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
from typing import Sequence


def kraft_sum(lengths: Sequence[int]) -> Fraction:
    return sum((Fraction(1, 2**l) for l in lengths), Fraction(0))


def cost(weights: Sequence[float], lengths: Sequence[int]) -> float:
    return sum(w * l for w, l in zip(weights, lengths))


def _check(n: int, limit: int) -> None:
    if n < 2:
        raise ValueError("need at least two symbols")
    if 2**limit < n:
        raise ValueError("no prefix code of n symbols has all lengths <= limit")


def huffman_lengths(weights: Sequence[float]) -> list[int]:
    """Unrestricted Huffman code lengths; ties go to the older item."""
    n = len(weights)
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


def exact_lengths(weights: Sequence[float], limit: int) -> list[int]:
    """An optimal code with all lengths <= limit, by dynamic programming.

    Sort the weights in non-increasing order; some optimal code then has
    non-decreasing lengths. Build the tree level by level: with `a`
    free nodes at depth d and symbols i.. still to place, choose how many
    of the next symbols become leaves at depth d. The other free nodes
    become inner nodes with two children each. O(L n^3) time.
    """
    n = len(weights)
    _check(n, limit)
    order = sorted(range(n), key=lambda i: -weights[i])
    ws = [weights[i] for i in order]
    prefix = [0]
    for x in ws:
        prefix.append(prefix[-1] + x)
    inf = float("inf")

    @lru_cache(maxsize=None)
    def best(d: int, i: int, a: int):
        top = min(a, n - i)
        result = (inf, 0)
        for k in range(top + 1):
            here = d * (prefix[i + k] - prefix[i])
            if i + k == n:
                rest = 0
            elif d == limit:
                continue
            else:
                nxt = min(2 * (a - k), n - i - k)
                if nxt == 0:
                    continue
                rest = best(d + 1, i + k, nxt)[0]
            if here + rest < result[0]:
                result = (here + rest, k)
        return result

    lengths = [0] * n
    d, i, a = 0, 0, 1
    while i < n:
        k = best(d, i, a)[1]
        for j in range(i, i + k):
            lengths[order[j]] = d
        a = min(2 * (a - k), n - i - k)
        i += k
        d += 1
    best.cache_clear()
    return lengths


def brute_force_lengths(weights: Sequence[float], limit: int) -> list[int]:
    """Try all non-decreasing length lists with lengths <= limit."""
    n = len(weights)
    _check(n, limit)
    order = sorted(range(n), key=lambda i: -weights[i])
    best, best_cost = None, None
    for ls in combinations_with_replacement(range(1, limit + 1), n):
        if kraft_sum(ls) > 1:
            continue
        c = sum(weights[order[k]] * ls[k] for k in range(n))
        if best_cost is None or c < best_cost:
            best, best_cost = ls, c
    lengths = [0] * n
    for k, i in enumerate(order):
        lengths[i] = best[k]
    return lengths


def adjust_bits(bits: list[int], limit: int) -> list[int]:
    """The adjustment of JPEG (ITU-T T.81, Annex K, Clause K.2).

    bits[l] is the number of codewords of length l of a full code tree.
    While some length i > limit is in use, remove two symbols of length
    i: one takes the length i - 1 of their parent, and the other goes
    under a leaf of length j < i - 1, which becomes the parent of two
    codewords of length j + 1.
    """
    bits = list(bits)
    for i in range(len(bits) - 1, limit, -1):
        while bits[i] > 0:
            j = i - 2
            while bits[j] == 0:
                j -= 1
            bits[i] -= 2
            bits[i - 1] += 1
            bits[j + 1] += 2
            bits[j] -= 1
    return bits[: limit + 1]


def jpeg_lengths(weights: Sequence[float], limit: int = 16, reserve: bool = False) -> list[int]:
    """Huffman lengths, then the JPEG adjustment to the limit.

    The symbols keep their order by the Huffman length (then by index)
    and take the new lengths in that order. With reserve=True, a symbol
    of weight 1 is added first and its slot removed at the end, so that
    no codeword is all ones, as JPEG requires.
    """
    n = len(weights)
    _check(n + (1 if reserve else 0), limit)
    ws = list(weights) + ([1] if reserve else [])
    old = huffman_lengths(ws)
    bits = [0] * (max(old) + 1)
    for l in old:
        bits[l] += 1
    bits = adjust_bits(bits, limit)
    new = []
    for l, c in enumerate(bits):
        new += [l] * c
    if reserve:
        new.pop()  # the longest slot belongs to the reserved symbol
    rank = sorted(range(n), key=lambda i: (old[i], i))
    lengths = [0] * n
    for k, i in enumerate(rank):
        lengths[i] = new[k]
    return lengths
