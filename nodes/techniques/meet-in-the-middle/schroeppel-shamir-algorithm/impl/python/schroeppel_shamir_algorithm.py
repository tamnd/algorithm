# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schroeppel-shamir-algorithm/. The authors are listed in prov/9AEYS5.jsonl.

import heapq


def _subset_sums(a: list[int], lo: int, hi: int) -> list[tuple[int, int]]:
    """Return (sum, mask) for each of the 2^(hi - lo) subsets of positions lo .. hi - 1."""
    sums = [(0, 0)]
    for p in range(lo, hi):
        sums += [(s + a[p], m | (1 << p)) for s, m in sums]
    return sums


def schroeppel_shamir(a: list[int], t: int) -> list[int] | None:
    """Return the sorted positions of a subset of a with sum t, or None if there is none.

    The items are integers of any sign. The four quarter lists and the two
    heaps hold O(2^(n/4)) entries; the walk does O(2^(n/2)) heap operations of
    O(n) comparisons each, so the time is O(n 2^(n/2)).
    """
    n = len(a)
    q = [k * n // 4 for k in range(5)]
    la = _subset_sums(a, q[0], q[1])  # @line L1
    lb = _subset_sums(a, q[1], q[2])
    lc = _subset_sums(a, q[2], q[3])
    ld = _subset_sums(a, q[3], q[4])
    lb.sort()  # @line L2
    ld.sort()
    h1 = [(la[i][0] + lb[0][0], i, 0) for i in range(len(la))]  # @line L3
    heapq.heapify(h1)
    last = len(ld) - 1
    h2 = [(-(lc[k][0] + ld[last][0]), k, last) for k in range(len(lc))]  # @line L4
    heapq.heapify(h2)
    while h1 and h2:  # @line L5
        s1, i, j = h1[0]  # @line L6
        s2, k, l = -h2[0][0], h2[0][1], h2[0][2]
        if s1 + s2 == t:  # @line L7
            mask = la[i][1] | lb[j][1] | lc[k][1] | ld[l][1]
            return [p for p in range(n) if mask >> p & 1]
        if s1 + s2 < t:  # @line L8
            heapq.heappop(h1)
            if j + 1 < len(lb):
                heapq.heappush(h1, (la[i][0] + lb[j + 1][0], i, j + 1))
        else:  # @line L9
            heapq.heappop(h2)
            if l > 0:
                heapq.heappush(h2, (-(lc[k][0] + ld[l - 1][0]), k, l - 1))
    return None  # @line L10
