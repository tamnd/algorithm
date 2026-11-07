# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial-multiplication/. The authors are listed in prov/YHNK2G.jsonl.
"""Johnson's heap-based multiplication of sparse polynomials.

A sparse polynomial is a list of (exponent, coefficient) pairs with strictly
increasing exponents and nonzero coefficients; the zero polynomial is [].
Coefficients may be of any type with +, * and == 0 that models a commutative
ring, for example int, Fraction or a class for Z/pZ.
"""

from __future__ import annotations

import heapq
from typing import Any, Sequence

Term = tuple[int, Any]


def heap_multiply(a: Sequence[Term], b: Sequence[Term]) -> list[Term]:
    """The product of two sparse polynomials, produced in increasing order of exponent.

    Precondition: a and b are normalized (sorted exponents, no zero
    coefficient). Cost, for s = min(len(a), len(b)) and t = max(len(a), len(b)):
    s t ring multiplications, at most s t ring additions, and s t heap pops and
    pushes on a heap of at most s entries, so O(s t log s) exponent
    comparisons. Extra space O(s) besides the output.
    """
    if len(a) > len(b):
        a, b = b, a
    s, t = len(a), len(b)
    if s == 0:  # @line L1
        return []
    heap = [(a[i][0] + b[0][0], i, 0) for i in range(s)]  # @line L2
    heapq.heapify(heap)
    c: list[list[Any]] = []  # @line L3
    while heap:  # @line L4
        k, i, j = heapq.heappop(heap)  # @line L5
        u = a[i][1] * b[j][1]  # @line L6
        if c and c[-1][0] == k:  # @line L7
            c[-1][1] = c[-1][1] + u
        else:  # @line L8
            c.append([k, u])
        if j + 1 < t:  # @line L9
            heapq.heappush(heap, (a[i][0] + b[j + 1][0], i, j + 1))
    return [(k, v) for k, v in c if v != 0]  # @line L10
