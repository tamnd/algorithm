# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horowitz-sahni-algorithm/. The authors are listed in prov/7817P3.jsonl.

Entry = tuple[int, int]  # (sum, bit mask of the indices)


def sorted_sums(a: list[int], lo: int, hi: int) -> list[Entry]:
    """Return (sum, mask) for each subset of the indices lo .. hi - 1 of a, sorted by sum.

    Bit k of mask is set when index k is in the subset. Each new item doubles
    the list by a merge, so the cost is Theta(2^(hi - lo)) time and space.
    """
    s: list[Entry] = [(0, 0)]  # @line L11
    for k in range(lo, hi):  # @line L12
        bit = 1 << k
        s2 = [(v + a[k], m | bit) for v, m in s]  # @line L13
        merged: list[Entry] = []  # @line L14
        i = j = 0
        while i < len(s) and j < len(s2):
            if s[i][0] <= s2[j][0]:
                merged.append(s[i])
                i += 1
            else:
                merged.append(s2[j])
                j += 1
        merged.extend(s[i:])
        merged.extend(s2[j:])
        s = merged
    return s  # @line L15


def horowitz_sahni_algorithm(a: list[int], t: int) -> list[int] | None:
    """Return sorted 0-based indices of a subset of a with sum t, or None if there is none.

    The numbers and t are any integers; the empty subset answers t == 0.
    Cost: Theta(2^(n/2)) time and space for n = len(a).
    """
    n = len(a)
    h = n // 2  # @line L1
    A = sorted_sums(a, 0, h)  # @line L2
    B = sorted_sums(a, h, n)  # @line L3
    i, j = 0, len(B) - 1  # @line L4
    while i < len(A) and j >= 0:  # @line L5
        s = A[i][0] + B[j][0]  # @line L6
        if s == t:  # @line L7
            mask = A[i][1] | B[j][1]
            return [k for k in range(n) if mask >> k & 1]
        elif s < t:  # @line L8
            i += 1
        else:  # @line L9
            j -= 1
    return None  # @line L10
