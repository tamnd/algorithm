# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-sum-two-pointer-scan/. The authors are listed in prov/V2066X.jsonl.


def three_sum_two_pointer_scan(values: list[int], t: int = 0) -> list[tuple[int, int, int]]:
    """Return every distinct value triple (x, y, z), x <= y <= z, that is drawn
    from three different positions of values and has x + y + z == t.

    The triples come out in lexicographic order. The input list is not changed.
    Cost: O(n log n) for the sort plus O(n^2) for the scans; O(n) extra space
    for the sorted copy (O(1) more if the caller may sort in place).
    """
    a = sorted(values)  # @line L1
    n = len(a)
    out: list[tuple[int, int, int]] = []
    for i in range(n - 2):  # @line L2
        if i > 0 and a[i] == a[i - 1]:  # @line L3
            continue
        lo, hi = i + 1, n - 1  # @line L4
        while lo < hi:  # @line L5
            s = a[i] + a[lo] + a[hi]  # @line L6
            if s < t:  # @line L7
                lo += 1
            elif s > t:  # @line L8
                hi -= 1
            else:
                out.append((a[i], a[lo], a[hi]))  # @line L9
                lo += 1  # @line L10
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
                hi -= 1  # @line L11
                while lo < hi and a[hi] == a[hi + 1]:
                    hi -= 1
    return out  # @line L12
