# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/galil-seiferas/. The authors are listed in prov/7W7A4V.jsonl.

"""Galil-Seiferas string matching: linear time with a constant number of integer variables."""

from collections.abc import Sequence


def factorize(
    pattern: Sequence, k: int = 4, stats: dict | None = None
) -> tuple[int, int, int]:
    """Return (s, p1, q1) for the perfect factorization u v of a nonempty pattern.

    u = pattern[:s], v = pattern[s:]; v has at most one prefix period, and if
    it has one its length is p1; v[0 .. p1 + q1 - 1] is the longest prefix of v
    with period p1, and p1 is its smallest period. The loops follow the three
    procedures newP1, newP2 and parse of the code of Charras and Lecroq. If
    stats is a dict, stats["exit"] receives the line that returned.
    """
    x = pattern
    m = len(x)
    s, p1, q1 = 0, 1, 0  # @line L10
    while True:  # @line L11
        while s + p1 + q1 < m and x[s + q1] == x[s + p1 + q1]:  # @line L12
            q1 += 1
        if p1 + q1 < k * p1:  # @line L13
            if s + p1 + q1 == m:  # @line L14
                if stats is not None:
                    stats["exit"] = "L14"
                return s, p1, q1
            p1, q1 = p1 + q1 // k + 1, 0  # @line L15
            continue
        # p1 is the shortest prefix period of x[s:]  # @line L16
        p2, q2 = q1, 0  # @line L17
        while True:  # @line L18
            while (  # @line L19
                p2 + q2 < k * p2 and s + p2 + q2 < m and x[s + q2] == x[s + p2 + q2]
            ):
                q2 += 1
            if p2 + q2 == k * p2:  # @line L20
                break
            if s + p2 + q2 == m:  # @line L21
                if stats is not None:
                    stats["exit"] = "L21"
                return s, p1, q1
            if q2 == p1 + q1:  # @line L22
                p2, q2 = p2 + p1, q2 - p1
            else:
                p2, q2 = p2 + q2 // k + 1, 0  # @line L23
        while True:  # @line L24
            while s + p1 + q1 < m and x[s + q1] == x[s + p1 + q1]:  # @line L25
                q1 += 1
            while p1 + q1 >= k * p1:  # @line L26
                s, q1 = s + p1, q1 - p1
            if s + p1 + q1 == m:  # @line L27
                if stats is not None:
                    stats["exit"] = "L27"
                return s, p1, q1
            p1, q1 = p1 + q1 // k + 1, 0  # @line L28
            if p1 >= p2:  # @line L29
                break


def galil_seiferas(
    text: Sequence, pattern: Sequence, k: int = 4, stats: dict | None = None
) -> list[int]:
    """Return every shift s with text[s:s+len(pattern)] == pattern, in increasing order.

    Characters are compared only for equality. k >= 3 is the constant of the
    algorithm. If stats is a dict, stats["comparisons"] receives the number of
    text character comparisons made by the search phase.
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        return list(range(n + 1))
    out: list[int] = []
    comparisons = 0
    if m <= n:
        x, y = pattern, text
        s, p1, q1 = factorize(x, k)  # @line L3
        p, q = 0, 0  # @line L4
        while p <= n - m:  # @line L5
            while s + q < m:  # @line L6
                comparisons += 1
                if x[s + q] != y[p + s + q]:
                    break
                q += 1
            if q == m - s:  # @line L7
                i = 0
                while i < s:
                    comparisons += 1
                    if x[i] != y[p + i]:
                        break
                    i += 1
                if i == s:
                    out.append(p)
            if q == p1 + q1:  # @line L8
                p, q = p + p1, q - p1
            else:
                p, q = p + q // k + 1, 0  # @line L9
    if stats is not None:
        stats["comparisons"] = comparisons
    return out
