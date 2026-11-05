# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/galil-park-algorithm/. The authors are listed in prov/0F6W2E.jsonl.

"""The Galil-Park algorithm for approximate string matching with k differences.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of end
positions j in 0..len(text) such that some substring text[h:j] has edit
distance at most k to the pattern.

The furthest rows L[d][e] of the diagonals are computed in order of the
anti-diagonals c = d + e. A pattern-text extension is derived from a table of
pattern-pattern extensions and a reference triple (q, y, f), which records that
text[q:q+f] equals pattern[y:y+f] and that the match cannot be extended. The
text is never indexed by a suffix structure.
"""

NONE = -(10**18)  # stands for "no cell of the diagonal has a value <= e"


def pattern_extensions(pattern: str) -> list[list[int]]:
    """Return pp with pp[a][b] = length of the longest common prefix of
    pattern[a:] and pattern[b:], for 0 <= a, b <= m. Cost: Theta(m^2)."""
    m = len(pattern)
    pp = [[0] * (m + 1) for _ in range(m + 1)]
    for a in range(m - 1, -1, -1):
        row, below = pp[a], pp[a + 1]
        for b in range(m - 1, -1, -1):
            if pattern[a] == pattern[b]:
                row[b] = below[b + 1] + 1
    return pp


def galil_park(pattern: str, text: str, k: int) -> list[int]:
    """Return the end positions of the approximate matches of pattern in text.

    Precondition: k >= 0. Uses Theta(m^2) space for the pattern table and
    O(k) space for the furthest rows and the reference triples.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    m, n = len(pattern), len(text)
    pp = pattern_extensions(pattern)  # @line L1
    ref: list[tuple[int, int, int] | None] = [None] * (k + 1)  # @line L2
    front = 0  # text positions below front have been read
    rows = [[NONE] * (k + 1) for _ in range(3)]  # rows[c % 3][e] = L[c - e][e]
    ends = []
    for c in range(n + k + 1):  # @line L3
        cur, p1, p2 = rows[c % 3], rows[(c - 1) % 3], rows[(c - 2) % 3]
        for e in range(k + 1):  # @line L4
            d = c - e
            if d > n or d < -m:
                cur[e] = NONE
                continue
            r = max(0, -d)  # @line L5
            if e > 0:
                if c >= 1 and p1[e - 1] != NONE:
                    r = max(r, p1[e - 1] + 1)  # L[d][e-1] + 1
                if c >= 2 and p2[e - 1] != NONE:
                    r = max(r, p2[e - 1])  # L[d-1][e-1]
                if cur[e - 1] != NONE:
                    r = max(r, cur[e - 1] + 1)  # L[d+1][e-1] + 1
            r = min(r, m, n - d)
            r0, x = r, r + d  # @line L6
            while r < m and x < n:  # @line L7
                if x >= front:  # @line L8
                    if pattern[r] != text[x]:
                        front = x + 1
                        break
                    r, x = r + 1, x + 1
                    front = x
                    continue
                best = None
                for t in ref:  # @line L9
                    if t is not None and t[0] <= x < t[0] + t[2]:
                        if best is None or t[0] + t[2] > best[0] + best[2]:
                            best = t
                if best is not None:
                    q, y, f = best
                    g, h = pp[r][y + x - q], q + f - x
                    if g != h:  # @line L10
                        r += min(g, h)
                        break
                    r, x = r + g, x + g
                elif pattern[r] == text[x]:  # @line L11
                    r, x = r + 1, x + 1
                else:
                    break
            cur[e] = r  # @line L12
            if r > r0:
                old = ref[e]
                if old is None or r + d > old[0] + old[2]:
                    ref[e] = (r0 + d, r0, r - r0)
            if e == k and r == m:  # @line L13
                ends.append(m + d)
    return ends
