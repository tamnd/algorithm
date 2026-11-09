# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kung-algorithm/. The authors are listed in prov/R32A7X.jsonl.

"""Kung, Luccio and Preparata (1975): the nondominated points of a finite set.

All objectives are minimized. The input is a list of n vectors of the same
length p >= 1. The output is the sorted list of the indices of the vectors that
no other vector dominates; equal vectors do not dominate each other, so all
copies of a nondominated vector are returned.

Each set in the recursion is kept as one list of point ids per coordinate,
sorted by that coordinate, so no call sorts again. The time is O(n log n) for
p = 2 and p = 3 and O(n log^(p-2) n) for p >= 4, after one O(p n log n) sort,
with O(p n) extra space per level of recursion.
"""

from typing import Dict, List, Sequence, Tuple

Vector = Sequence


def kung(points: Sequence[Vector]) -> List[int]:
    """Return the indices of the nondominated vectors, in increasing order."""
    n = len(points)
    if n == 0:
        return []
    p = len(points[0])
    # Remove copies. Equal vectors share the fate of their representative.
    rep: Dict[Tuple, int] = {}
    for i, v in enumerate(points):
        rep.setdefault(tuple(v), i)
    ids = list(rep.values())
    P = {i: tuple(points[i]) for i in ids}
    dead = {i: False for i in ids}
    low = {i: False for i in ids}

    def split(lists: List[List[int]], lower: List[int]):
        for i in lower:
            low[i] = True
        lo = [[i for i in lst if low[i]] for lst in lists]
        hi = [[i for i in lst if not low[i]] for lst in lists]
        for i in lower:
            low[i] = False
        return lo, hi

    def alive(lists: List[List[int]]) -> List[List[int]]:
        return [[i for i in lst if not dead[i]] for lst in lists]

    def filt(A: List[List[int]], B: List[List[int]], k: int) -> List[List[int]]:
        """Mark dead each b in B that some a in A weakly dominates in the
        coordinates k..p-1, and return the rest of B. A[j - k] and B[j - k]
        are sorted by coordinate j."""
        if not A or not A[0] or not B[0]:  # @line L6
            return B  # @line L6
        if k == p - 1:  # @line L7
            m = P[A[0][0]][k]  # @line L7
            for b in B[0]:  # @line L7
                if P[b][k] >= m:  # @line L7
                    dead[b] = True  # @line L7
            return alive(B)  # @line L7
        # The order by (x_k, A before B), by a merge of two sorted lists.
        a_list, b_list = A[0], B[0]
        merged: List[Tuple[int, int]] = []
        i = j = 0
        while i < len(a_list) or j < len(b_list):
            if j == len(b_list) or (
                i < len(a_list) and P[a_list[i]][k] <= P[b_list[j]][k]
            ):
                merged.append((a_list[i], 0))
                i += 1
            else:
                merged.append((b_list[j], 1))
                j += 1
        if k == p - 2:  # @line L8
            m = None  # @line L9
            for v, side in merged:  # @line L9
                y = P[v][k + 1]
                if side == 0:  # @line L9
                    if m is None or y < m:  # @line L9
                        m = y  # @line L9
                elif m is not None and m <= y:  # @line L10
                    dead[v] = True  # @line L10
            return alive(B)  # @line L10
        half = len(merged) // 2  # @line L11
        lower = [v for v, _ in merged[:half]]  # @line L11
        A_lo, A_hi = split(A, lower)  # @line L11
        B_lo, B_hi = split(B, lower)  # @line L11
        filt(A_lo, B_lo, k)  # @line L12
        B_hi = filt(A_hi, B_hi, k)  # @line L13
        filt(A_lo[1:], B_hi[1:], k + 1)  # @line L14
        return alive(B)  # @line L14

    def front(S: List[List[int]]) -> List[List[int]]:
        """S[0] is sorted lexicographically, S[j] by coordinate j for j >= 1.
        Mark dead the vectors of S that another vector of S dominates."""
        if len(S[0]) == 1:  # @line L2
            return S  # @line L2
        half = len(S[0]) // 2  # @line L3
        T, B = split(S, S[0][:half])  # @line L3
        R_T = front(T)  # @line L4
        R_B = front(B)  # @line L4
        if p == 1:
            for b in R_B[0]:
                dead[b] = True
        else:
            filt(R_T[1:], R_B[1:], 1)  # @line L5
        return alive(S)  # @line L5

    S = [sorted(ids, key=lambda i: P[i])]  # @line L1
    S += [sorted(ids, key=lambda i: P[i][j]) for j in range(1, p)]  # @line L1
    front(S)  # @line L1
    return [i for i, v in enumerate(points) if not dead[rep[tuple(v)]]]
