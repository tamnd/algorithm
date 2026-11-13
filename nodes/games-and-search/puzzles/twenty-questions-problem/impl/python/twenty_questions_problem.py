# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/twenty-questions-problem/. The authors are listed in prov/ZFP8QP.jsonl.
"""Twenty questions: find a hidden object among n with yes-or-no questions.

Costs here are numbers of questions. With weights, the cost of a strategy is
the expected number of questions, sum of p_i times the depth of object i.
"""

import heapq
import math
from functools import lru_cache


def worst_case(n):
    """Least worst-case number of questions for n objects: ceil(log2 n)."""
    return (n - 1).bit_length()


def huffman_cost(weights):
    """Least expected number of questions with arbitrary subset questions (Huffman)."""
    if len(weights) <= 1:
        return 0
    heap = list(weights)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total


def subset_cost(weights):
    """Brute force over every question tree: split the set of live objects in all ways."""
    n = len(weights)
    mass = [0] * (1 << n)
    for s in range(1, 1 << n):
        low = s & -s
        mass[s] = mass[s ^ low] + weights[low.bit_length() - 1]

    @lru_cache(maxsize=None)
    def cost(s):
        if s & (s - 1) == 0:
            return 0
        best = None
        sub = (s - 1) & s
        while sub:
            if sub < s ^ sub:  # each split once
                c = cost(sub) + cost(s ^ sub)
                if best is None or c < best:
                    best = c
            sub = (sub - 1) & s
        return mass[s] + best

    return cost((1 << n) - 1)


def alphabetic_cost(weights):
    """Least expected number of questions of the form 'is it before position t?'.

    Objects are in a fixed order and every question splits them into a prefix
    and a suffix: the optimal alphabetic tree, by interval dynamic programming.
    """
    n = len(weights)
    pre = [0]
    for x in weights:
        pre.append(pre[-1] + x)
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length
            cost[i][j] = pre[j] - pre[i] + min(cost[i][t] + cost[t][j] for t in range(i + 1, j))
    return cost[0][n]


def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)


@lru_cache(maxsize=None)
def wins_with_one_lie(a, b, q):
    """Ulam's game with at most one lie: can q questions always find the object?

    a objects are consistent with every answer so far; b objects are consistent
    with all answers but one. A question is any set; it holds a1 of the a and
    b1 of the b objects.
    """
    if a + b <= 1:
        return True
    if q == 0 or a * (q + 1) + b > 2 ** q:
        return False
    for a1 in range(a // 2 + 1):
        for b1 in range(b + 1):
            if 2 * a1 == a and 2 * b1 > b:
                break
            yes = (a1, a - a1 + b1)
            no = (a - a1, a1 + b - b1)
            if wins_with_one_lie(*yes, q - 1) and wins_with_one_lie(*no, q - 1):
                return True
    return False


def one_lie_search(n):
    """Least number of questions for n objects and at most one lie, by search."""
    q = 0
    while not wins_with_one_lie(n, 0, q):
        q += 1
    return q


def one_lie_pelc(n):
    """Pelc (1987): least q with n(q+1) <= 2^q for even n, n(q+1) + (q-1) <= 2^q for odd n."""
    q = 0
    while True:
        need = n * (q + 1) + (q - 1 if n % 2 else 0)
        if need <= 2 ** q:
            return q
        q += 1
