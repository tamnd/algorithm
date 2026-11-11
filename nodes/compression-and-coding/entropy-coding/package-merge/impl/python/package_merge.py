# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/package-merge/. The authors are listed in prov/Y4RNV8.jsonl.

"""Package-merge (Larmore and Hirschberg 1990): optimal length-limited
prefix code lengths in O(nL) time.

Coin view: each symbol i has one coin for each depth d = 1..L, of face
value 2^-d and cost w_i. Choose coins of total face value n - 1 at least
cost; symbol i then gets length l_i = the number of its coins chosen.

The list Q[k] holds the items of face value 2^-(L-k+1): the coins of
that value (leaves) and the packages made by pairing items of Q[k - 1].
Only the order of leaves and packages in each list is kept, which is
enough to expand the solution, so the time and space are O(nL).
"""

from typing import Sequence


def package_merge(weights: Sequence[float], limit: int) -> list[int]:
    """Return lengths l_i <= limit of a least-cost prefix code."""
    n = len(weights)
    if n < 2:
        raise ValueError("need at least two symbols")
    if 2**limit < n:
        raise ValueError("no prefix code of n symbols has all lengths <= limit")
    order = sorted(range(n), key=lambda i: weights[i])  # non-decreasing
    w = [weights[i] for i in order]

    # kinds[k][j] is True if item j of Q[k] is a leaf, False if a package.
    kinds = []
    q = list(w)  # @line L1  Q[1]: the coins of the smallest value
    kinds.append([True] * n)
    for _ in range(2, limit + 1):  # @line L2
        packages = [q[2 * j] + q[2 * j + 1] for j in range(len(q) // 2)]  # @line L3
        merged, kind = [], []  # @line L4  merge the leaves and the packages
        a = b = 0
        while a < n or b < len(packages):
            if b == len(packages) or (a < n and w[a] <= packages[b]):
                merged.append(w[a])
                kind.append(True)
                a += 1
            else:
                merged.append(packages[b])
                kind.append(False)
                b += 1
        q = merged
        kinds.append(kind)

    lengths = [0] * n
    r = 2 * n - 2  # @line L5  take the 2n - 2 cheapest items of Q[L]
    for k in range(limit - 1, -1, -1):  # @line L6
        c = sum(kinds[k][:r])  # @line L7  leaves among the first r items
        for j in range(c):  # @line L8  they are the c lightest symbols
            lengths[order[j]] += 1
        r = 2 * (r - c)  # @line L9  each package taken holds 2 items of Q[k - 1]
    return lengths  # @line L10


def cost(weights: Sequence[float], lengths: Sequence[int]) -> float:
    return sum(x * l for x, l in zip(weights, lengths))
